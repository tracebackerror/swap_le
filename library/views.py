from django.shortcuts import *
from django.views.generic import FormView,ListView,DeleteView,UpdateView,DetailView
from .models import LibraryAsset,AssetHistory
from django.urls import reverse_lazy
from .forms import LibraryAssetForm,LibraryAssetEditForm,AddLibraryAssetHistoryForm
from staff.models import Staff
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import LibraryAssetFilter
from django_filters.views import FilterView
from students.models import Student
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

class CreateLibraryAsset(LoginRequiredMixin,FormView):
    model = LibraryAsset
    template_name="library/create_library_asset.html"
    success_url = reverse_lazy("staff:library:manage_library_asset")
    form_class = LibraryAssetForm
    context_object_name = "form"
    login_url=reverse_lazy('staff:login')
    
    def form_valid(self, form):
        if super().form_valid(form):
            staffuser=User.objects.get(username=self.request.user)
            StaffObj=Staff.objects.get(staffuser=staffuser)

            asset_type = form.cleaned_data['asset_type']
            asset_unique_code = form.cleaned_data['asset_unique_code']
            asset_description = form.cleaned_data['asset_description']
            name = form.cleaned_data['name']
            
            library_asset=LibraryAsset.objects.create(for_institution=StaffObj.institute,asset_type=asset_type,
                                                      asset_unique_code=asset_unique_code,asset_description=asset_description,created_by=StaffObj,name=name)            
            
            messages.add_message(self.request, messages.SUCCESS, 'Library Asset Successfully Saved!')
        return HttpResponseRedirect(self.get_success_url())
    
class ManageLibraryAsset(LoginRequiredMixin,FilterView,ListView):
    model = LibraryAsset
    template_name="library/manage_library_asset.html"
    context_object_name = 'library_asset'
    paginate_by = 10
    filterset_class = LibraryAssetFilter
    login_url=reverse_lazy('staff:login')
    
    
class DeleteLibraryAsset(LoginRequiredMixin,DeleteView):
    model = LibraryAsset
    template_name="library/delete_library_asset.html"
    success_url = reverse_lazy("staff:library:manage_library_asset")
    context_object_name = "form"
    pk_url_kwarg = 'pk'
    login_url=reverse_lazy('staff:login')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.add_message(self.request, messages.SUCCESS, 'Deleted Library Asset Successfully!')
        return HttpResponseRedirect(success_url)
    
    
class EditLibraryAsset(LoginRequiredMixin,UpdateView):
    model = LibraryAsset
    template_name="library/edit_library_asset.html"
    success_url = reverse_lazy("staff:library:manage_library_asset")
    form_class = LibraryAssetEditForm
    context_object_name = 'form'
    pk_url_kwarg = 'pk'
    login_url=reverse_lazy('staff:login')
     
    
    def form_valid(self, form):
        if super(EditLibraryAsset,self).form_valid(form):
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Updated Library Asset Status Successfully!')
        return HttpResponseRedirect(self.get_success_url())
    
    

class ManageLibraryAssetHistory(LoginRequiredMixin,ListView):
    model = AssetHistory
    template_name="library/manage_library_asset_history.html"
    context_object_name = 'library_history'
    paginate_by = 10
    queryset = None
    login_url=reverse_lazy('staff:login')
    mypk = ""
    
    def get_queryset(self,**kwargs):
        pk = self.kwargs.get('pk')
        self.mypk = pk
        asset_id = LibraryAsset.objects.get(id=pk)
        self.queryset = AssetHistory.objects.filter(asset_id=asset_id).order_by('checked_in')
        return super(ManageLibraryAssetHistory,self).get_queryset()
    
    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        context['mypk'] = self.mypk
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = context,
            **response_kwargs
        )

    
class AddLibraryAssetHistory(LoginRequiredMixin,FormView):
    model = AssetHistory
    template_name="library/add_library_asset_history.html"
    success_url = "staff:library:manage_library_asset_history"
    form_class = AddLibraryAssetHistoryForm
    context_object_name = "form"
    login_url=reverse_lazy('staff:login')
    def form_valid(self, form,**kwargs):
        pk = self.kwargs.get('pk')
        library_asset = LibraryAsset.objects.get(id=pk)
        student_id = form.cleaned_data['student_id']
        
        staffuser=User.objects.get(username=self.request.user)
        StaffObj=Staff.objects.get(staffuser=staffuser)
        obj = LibraryAsset.objects.get(id=pk)
        
        if obj.availability:
            AssetHistory.objects.create(asset_id = library_asset,student_id = student_id,checked_out=datetime.now(),checked_in_user_id=StaffObj)
            obj.availability = False
            obj.save()
            messages.add_message(self.request, messages.SUCCESS, 'Asset Check-Out Successfully!')
        else:
            messages.add_message(self.request, messages.SUCCESS, 'Asset Already Check-Out !')
        
        return HttpResponseRedirect(self.get_success_url(pk))    

    def get_success_url(self,pk):
        return reverse(self.success_url, kwargs={'pk': pk})
    
    def get_form_kwargs(self):
        kwargs = super(AddLibraryAssetHistory, self).get_form_kwargs()
        kwargs.update({'request_user': self.request.user})
        return kwargs


@login_required(login_url=reverse_lazy('staff:login'))
def CheckIn(request,pk,id):
    obj=AssetHistory.objects.get(id=id)
    obj.checked_in=datetime.now()
    obj.save()
    
    obj = LibraryAsset.objects.get(id=pk)
    obj.availability = True
    obj.save()
    
    messages.add_message(request, messages.SUCCESS, 'Asset Check-In Successfully!')
    url = reverse("staff:library:manage_library_asset_history",kwargs={'pk':pk})
    return HttpResponseRedirect(url)
    
    