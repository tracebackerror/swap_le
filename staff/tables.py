import django_tables2 as tables
from .models import Staff
import itertools
from django.utils.html import format_html


class StaffTable(tables.Table):
    row_number = tables.Column(empty_values=())
    edit_staff = tables.TemplateColumn('<a href=" {% url "institutions:edit_institution_staff" username=record.staffuser  %} ">Edit</a>')
    delete_staff = tables.TemplateColumn('<a href=" {% url "institutions:delete_institution_staff" username=record.staffuser  %} ">Delete</a>')

    def __init__(self, *args, **kwargs):
        super(StaffTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return 'Row %d' % next(self.counter)



    class Meta:
        model = Staff
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        # fields = ('row_number', 'institute',)
        sequence = ('row_number', 'staffuser', 'institute', 'allowregistration', 'created', 'updated', 'user_type', 'deleted')
