import django_tables2 as tables
from .models import License
import itertools

class LicenseViewTable(tables.Table):

    def __init__(self, *args, **kwargs):
        super(StaffTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    


    class Meta:
        model = License
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        # fields = ( 'institute',)
        sequence = ( 'staffuser', 'institute', 'allowregistration', 'created', 'updated', 'user_type', 'deleted')
