from django.test import TestCase
from .models import PackageVersion, Package, PackageSet

# Create your tests here.
class PackageVersionTestCase(TestCase):
    def setUp(self):
        PackageSet.objects.create(slug="TestSet")
        Package.objects.create(slug="a", cached_article_preview="Hong Yi", publish_date="2018-5-8", package_set_id="TestSet")
    
    def test_PackageVersion_creation(self):
        # Check if new PackageVersion is added to database and latest_version of respective Package is updated
        packageA = Package.objects.get(slug="a")
        packageA.create_version("This version uses Hong Yi")
        myPV = PackageVersion.objects.get(package=packageA)
        self.assertEqual(myPV.article_data, "Hong Yi")
        self.assertEqual(myPV.version_description, "This version uses Hong Yi")     
        self.assertEqual(packageA.latest_version, myPV.package)
        
        
        # Check handling of multiple PackageVersions 
        packageA.cached_article_preview = "HONG YEET"
        packageA.create_version("This version uses HONG YEET") # Now we should have 2 different versions of packageA (slug = "a")
        myPV = PackageVersion.objects.last()
        self.assertEqual(len(PackageVersion.objects.filter(package=packageA).all()), 2)
        self.assertEqual(myPV.article_data, "HONG YEET")
        self.assertEqual(myPV.version_description, "This version uses HONG YEET")

        # Check if able to retrieve publish_date of latest PackageVersion
        getLatest = packageA.latest_version
        self.assertEqual(getLatest.publish_date, packageA.publish_date)