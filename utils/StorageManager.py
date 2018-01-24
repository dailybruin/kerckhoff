from django.conf import settings
import boto3 as boto

class S3StorageManager():
    bucket = boto.resource('s3').Bucket(settings.S3_SITE_UPLOAD_BUCKET)
    bucket_name = settings.S3_SITE_UPLOAD_BUCKET

    def list_all_sites(self):
        # res = self.s3.list_objects_v2(Bucket=self.bucket_name, Delimiter='/')
        # if 'CommonPrefixes' in res:
        #     folders = [ prefix['Prefix'].split('/')[0] for prefix in res['CommonPrefixes'] ]
        #     return folders
        # else
        
        # Get folder keys
        res = self.bucket.meta.client.list_objects_v2(Bucket=self.bucket_name, Delimiter='/')
        if 'CommonPrefixes' in res:
            folders = [ prefix['Prefix'] for prefix in res['CommonPrefixes'] ]
            for folder in folders:
                # Only check the ACL of the first object, which is probably not a good idea
                first_obj_acl = list(self.bucket.objects.filter(Prefix=folder).all())[0].Acl()
                for grant in first_obj_acl.grants:
                    if grant['Grantee']['Type'].lower() == 'group' \
                        and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
                        print(grant)

            return folders
        else:
            return []