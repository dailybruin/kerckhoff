import hashlib
import imghdr
import logging
import pathlib
import re
import tempfile

import arrow
import boto3
from botocore.client import Config
from django.conf import settings
from PIL import Image
from requests_oauthlib import OAuth2Session

from .google_drive_actions import get_file
from kerckhoff.settings import S3_DOMAIN_OF_UPLOADED_IMAGES

IMAGE_REGEX = re.compile(r"!\[[^\]]+\]\(([^)]+)\)")
S3_BUCKET = settings.S3_ASSETS_UPLOAD_BUCKET

logger = logging.getLogger(settings.APP_NAME)
s3 = boto3.client('s3', 'us-west-2', config=Config(s3={'addressing_style': 'path'}))

def rewrite_image_url(package):
    def replace_url(fn):
        #print(fn.group(1).replace)
        if fn.group(1) in package.images["s3"]:
            return fn.group().replace(fn.group(1), package.images["s3"][fn.group(1)]["url"])
        else:
            return fn.group()
    text = IMAGE_REGEX.sub(replace_url,package.cached_article_preview)
    return text

def transfer_to_s3(session: OAuth2Session, package):
    if package.images.get("s3") is None:
        package.images["s3"] = {}

    for idx, image in enumerate(package.images["gdrive"]):
        # When the image was last modified on google drive
        last_modified_date = arrow.get(image['modifiedDate']).datetime
        if package.last_fetched_date is not None and package.last_fetched_date > last_modified_date:
            logger.info(f"{ image['title'] } has not been modified since last fetch.")
            continue
        else:
            logger.info(f"{ image['title'] } has been modified on Google Drive, updating.")

        req = get_file(session, image["id"], download=True)
        max_size = (1024, 1024)

        with tempfile.SpooledTemporaryFile(mode="w+b") as tf:
            print(image["title"] + " | Processing image %d ..." % idx)
            req.raw.decode_content = True
            header = req.raw.read(100)
            ext = imghdr.what(None, h=header)
            print(image["title"] + " | Found: {0}".format(ext))
            if ext == None:
                print("No image file found ... Continuing")
                continue

            tf.write(header + req.raw.read())
            im = Image.open(tf)
            image_hash = hashlib.md5(im.tobytes()).hexdigest()
            if image["title"] in package.images["s3"]:
                print("Old Hash found: " + package.images["s3"][image["title"]].get("hash"))
                print("Current Hash: " + image_hash)
                if package.images["s3"][image["title"]].get("hash") == image_hash:
                    print(image["title"] + " in package " + package.slug + " has not been edited. Ignoring.")
                    continue

            with tempfile.SpooledTemporaryFile(mode="w+b") as wtf:
                im.thumbnail(max_size, Image.ANTIALIAS)
                im.save(wtf, format=im.format, optimize=True, quality=85)
                original_fn = pathlib.Path(image["title"])
                fn = "images/{0}/{1}-{2}{3}".format(package.slug, original_fn.stem, image_hash, original_fn.suffix)
                wtf.seek(0)
                response = s3.put_object(
                    Bucket=S3_BUCKET,
                    Key=fn,
                    Body=wtf,
                    ACL='public-read'
                )

                package.images["s3"][image["title"]] = {
                    "url": "{0}/{1}".format(S3_DOMAIN_OF_UPLOADED_IMAGES, fn), 
                    "key": fn,
                    "hash": image_hash,
                    "s3_fields": response
                }
    return package