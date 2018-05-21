from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import CharField
from django.db.models.fields.files import ImageFieldFile
import json


class UserModelSerializer(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ImageFieldFile):
            try:
                return obj.path
            except ValueError:
                return ''


def user_to_json(user_instance):
    USER_CHOICE_FIELDS = (
        'role',
    )
    user_profile = model_to_dict(user_instance.profile, exclude=('user'))
    for field in USER_CHOICE_FIELDS:
        user_profile[field] = {
            "id": user_profile[field],
            "val": getattr(user_instance.profile, 'get_{0}_display'.format(field))()
        }
    data = json.dumps((user_profile), cls=UserModelSerializer)

    return data
