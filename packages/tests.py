from django.test import TestCase
from .models import PackageVersion, Package, PackageSet

# Create your tests here.
class PackageVersionTestCase(TestCase):
    def setUp(self):
        PackageSet.objects.create(slug="TestSet")
        Package.objects.create(slug="a", cached_article_preview="Hong Yi", publish_date="2018-5-8", package_set_id="TestSet")
    
    def test_PackageVersion_creation(self):
        packageA = Package.objects.get(slug="a")
        packageA.create_version()
        myPV = PackageVersion.objects.get(slug="a")

        # Check if new PackageVersion is added to database and latest_version of respective Package is updated
        self.assertEqual(myPV.article_data, "Hong Yi")
        self.assertEqual(packageA.latest_version, myPV.slug)      
        
        # Check if able to retrieve publish_date of latest PackageVersion
        getLatest = Package.objects.get(slug=myPV.slug)
        self.assertEqual(getLatest.publish_date, packageA.publish_date)