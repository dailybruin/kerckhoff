import math
#from django.contrib.auth.models import User
from django.test import TestCase
from .models import PackageVersion, Package, PackageSet
from .paginator import Paginator
from django.core.paginator import Page



# Create your tests here.
class PackageVersionTestCase(TestCase):
    def setUp(self):
        PackageSet.objects.create(slug="TestSet")
        Package.objects.create(slug="a", cached_article_preview="Hong Yi", publish_date="2018-5-8", package_set_id="TestSet")
            
    def test_PackageVersion_creation(self):
        # Check if new PackageVersion is added to database and latest_version of respective Package is updated
        testUser = User(username='kimjongun', password='katyperry')
        testUser.save()
        packageA = Package.objects.get(slug="a")
        packageA.create_version(testUser, "This version uses Hong Yi")
        myPV = PackageVersion.objects.get(package=packageA)

        # Check if PV database is properly updated with new PV object instance
        self.assertEqual(myPV.version_description, "This version uses Hong Yi") 
        self.assertEqual(packageA.latest_version, myPV)
        
        # Check handling of multiple PackageVersions 
        packageA.cached_article_preview = "HONG YEET"
        packageA.create_version(testUser, "This version uses HONG YEET") # Now we should have 2 different versions of packageA
        myPV = PackageVersion.objects.last()
        self.assertEqual(len(PackageVersion.objects.filter(package=packageA).all()), 2)
        self.assertEqual(myPV.article_data, "HONG YEET")
        self.assertEqual(myPV.version_description, "This version uses HONG YEET")
        self.assertEqual(myPV.creator.get_username(), "kimjongun")     

        # Check if able to retrieve publish_date of latest PackageVersion
        latestPV = packageA.latest_version
        self.assertEqual(latestPV.article_data, "HONG YEET")

        packageDB = Package.objects
        packageSetDB = PackageSet.objects
        packageVersionDB = PackageVersion.objects
        
class PaginatorTestCase(TestCase):        
    def test_paginator_basic(self):
        array = [i for i in range(0, 200)]
        paginator1 = Paginator(array, 30)
        paginator2 = Paginator(array, 20)
        self.assertEqual(paginator1.count, 200)
        self.assertEqual(paginator2.count, 200)
        self.assertEqual(paginator1.num_pages, math.ceil(200/30))
        self.assertEqual(paginator2.num_pages, math.ceil(200/20))
        # check all elements in a page
        for i in range(0, 200):
            inside = False
            for j in range(0, paginator1.num_pages):
                inside |= array[i] in paginator1.get_page(j).object_list
                if inside:
                    break
            self.assertEquals(inside, True)
            inside = False
            for j in range(0, paginator2.num_pages):
                inside |= array[i] in paginator2.get_page(j).object_list
                if inside:
                    break
            self.assertEquals(inside, True)

        #check that only last page doesn't have max number elements
        for i in range(0, paginator1.num_pages):
            if(i < paginator1.num_pages - 1): # if not last page, make sure that it has 30 elements
                self.assertEqual(len(paginator1.get_page(i+1)), 30)
            else:
                self.assertEqual(len(paginator1.get_page(i+1)), 200%paginator1.per_page)
        for i in range(0, paginator2.num_pages):
            self.assertEqual(len(paginator2.get_page(i+1)), paginator2.per_page)
     

    def test_paginator_orphans(self):
        array = [i for i in range(0, 200)]
        paginator1 = Paginator(array, 30, orphans=15) # if orphan 20, then 6 pages, otherwise 7
        paginator2 = Paginator(array, 45, orphans=20)   # if orphan 20, then 4 pages, otherwise 5
        self.assertEqual(paginator1.count, 200)
        self.assertEqual(paginator2.count, 200)
        self.assertEqual(paginator1.num_pages, math.ceil(float(200 - paginator1.orphans)/paginator1.per_page))
        self.assertEqual(paginator2.num_pages, math.ceil(float(200 - paginator2.orphans)/paginator2.per_page))
        # check all elements in a page
        for i in range(0, 200):
            inside = False
            for j in range(0, paginator1.num_pages):
                inside |= array[i] in paginator1.get_page(j+1).object_list
                if inside:
                    break
            self.assertEquals(inside, True)
            inside = False
            for j in range(0, paginator2.num_pages):
                inside |= array[i] in paginator2.get_page(j+1).object_list
                if inside:
                    break
            self.assertEquals(inside, True)
        #check that only last page doesn't have max number elements
        for i in range(0, paginator1.num_pages):
            if(i < paginator1.num_pages - 1): # if not last page, make sure that it has 30 elements
                self.assertEqual(len(paginator1.get_page(i+1)), paginator1.per_page)
            else:         
                self.assertEqual(len(paginator1.get_page(i+1)), 
                                 (200%paginator1.per_page < paginator1.orphans)*paginator1.per_page + 200%paginator1.per_page)
        for i in range(0, paginator2.num_pages):
            if(i < paginator2.num_pages - 1): # if not last page, make sure that it has 45 elements
                self.assertEqual(len(paginator2.get_page(i+1)), paginator2.per_page)
            else:
                self.assertEqual(len(paginator2.get_page(i+1)), 65)


