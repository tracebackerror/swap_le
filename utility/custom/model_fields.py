from django.db import models
import ast

class ListField(models.TextField):
    '''
    class Dummy(models.Model):
        mylist = ListField()
        
    >>> from foo.models import Dummy, ListField
    >>> d = Dummy()
    >>> d.mylist
    []
    >>> d.mylist = [3,4,5,6,7,8]
    >>> d.mylist
    [3, 4, 5, 6, 7, 8]
    >>> f = ListField()
    >>> f.get_prep_value(d.numbers)
    u'[3, 4, 5, 6, 7, 8]'
    
    
    '''
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
