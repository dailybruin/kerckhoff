# Utils
def feature_img_url(instance, filename):
    return "{0}/{1}/img/{2}".format(instance.page.slug, instance.created_on.timestamp(), filename)


def upload_file_url(instance, filename):
    return "{0}/{1}/files/{2}".format(instance.page.slug, instance.created_on.timestamp(), filename)
