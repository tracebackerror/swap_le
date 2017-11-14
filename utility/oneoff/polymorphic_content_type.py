'''
Usage: Use for migrating the existing model to Polymorphic Model
django.contrib.contenttypes.models.DoesNotExist: ContentType matching query does not exist.

Steps:
Inherit your model from PolymorphicModel.
Create a Django migration file to create the polymorphic_ctype_id database column.
Make sure the proper ContentType value is filled in.
'''

from django.contrib.contenttypes.models import ContentType
from myapp.models import MyModel

new_ct = ContentType.objects.get_for_model(MyModel)
MyModel.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_ct)