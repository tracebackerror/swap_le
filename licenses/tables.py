import django_tables2 as tables
from .models import License
import itertools

class LicenseViewTable(tables.Table):

    def __init__(self, *args, **kwargs):
        super(StaffTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return 'Row %d' % next(self.counter)



    class Meta:
        model = License
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        # fields = ('row_number', 'institute',)
        sequence = ('row_number', 'staffuser', 'institute', 'allowregistration', 'created', 'updated', 'user_type', 'deleted')
