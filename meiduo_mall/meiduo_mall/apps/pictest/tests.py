import os

from django.test import TestCase

# Create your tests here.


# =================================================================================================

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")
import django

django.setup()

from pictest.models import PicTest

pic = PicTest.objects.get(id=2)

print(pic.image)
# =================================================================================================
