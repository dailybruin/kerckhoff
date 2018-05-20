from .es import init_es
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kerckhoff.settings")

es = init_es()