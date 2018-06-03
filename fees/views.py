from django.shortcuts import *
from django.contrib import messages
from django.views.generic import FormView,ListView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from .forms import InstallmentFeesForm
from .models import FeesInstallment
from students.models import Student
from django_filters.views import FilterView
from .filters import FeesInstallmentFilter


# Create your views here.

class CreateFeesInstallment(LoginRequiredMixin,FormView):
    template_name="fees/create_fees_installment.html"
    form_class = InstallmentFeesForm
    success_url = 'staff:fees:manage_fees_installment'
    login_url = reverse_lazy('staff:login')
    
    def form_valid(self, form,**kwargs):
        pk = self.kwargs.get('pk')
        
        student_id = Student.objects.get(id=pk)
        amount = form.cleaned_data['amount']
        day = form.cleaned_data['day']
        month = form.cleaned_data['month']
        year = form.cleaned_data['year']
        paid = form.cleaned_data['paid']
        
        FeesInstallment.objects.create(student_id = student_id,amount = amount,day=day,month=month,year=year,paid=paid)
        messages.add_message(self.request, messages.SUCCESS, 'Fees Installment Successfully Added!')
        
        return HttpResponseRedirect(self.get_success_url(pk))    

    def get_success_url(self,pk):
        return reverse(self.success_url, kwargs={'pk': pk})
    
    
class ManageFeesInstallment(LoginRequiredMixin,FilterView,ListView):
    model = FeesInstallment
    context_object_name = 'fees_model'
    template_name="fees/manage_fees_installment.html"
    paginate_by = 10
    filterset_class = FeesInstallmentFilter
    login_url = reverse_lazy('staff:login')
    mypk = None
    
    def get_queryset(self,**kwargs):
        pk = self.kwargs.get('pk')
        self.mypk = pk
        student_id = Student.objects.get(id=pk)
        self.queryset = FeesInstallment.objects.filter(student_id=student_id)
        return super(ManageFeesInstallment,self).get_queryset()
    
    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        context['mypk'] = self.mypk
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = context,
            **response_kwargs
        )
        

class DeleteFeesInstallment(LoginRequiredMixin,DeleteView):
    model = FeesInstallment
    template_name="fees/delete_fees_installment.html"
    success_url = 'staff:fees:manage_fees_installment'
    context_object_name = "form"
    pk_url_kwarg = 'pk'
    login_url=reverse_lazy('staff:login')
    
    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('id')
        self.object = self.get_object()
        self.object.delete()
        messages.add_message(self.request, messages.SUCCESS, 'Deleted Fees Installment Successfully!')
        return HttpResponseRedirect(self.get_success_url(pk))
    
    def get_success_url(self,pk):
        return reverse(self.success_url, kwargs={'pk': pk})
    
    
    
class EditFeesInstallment(LoginRequiredMixin,UpdateView):
    model = FeesInstallment
    template_name="fees/edit_fees_installment.html"
    success_url = 'staff:fees:manage_fees_installment'
    form_class = InstallmentFeesForm
    context_object_name = 'form'
    pk_url_kwarg = 'pk'
    login_url=reverse_lazy('staff:login')
    
    def form_valid(self, form,**kwargs):
        id = self.kwargs.get('id')
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Updated Fees Installment Successfully!')
        return HttpResponseRedirect(self.get_success_url(id))
    
    def get_success_url(self,id):
        return reverse(self.success_url, kwargs={'pk': id})
    
    
    
    
    
    
