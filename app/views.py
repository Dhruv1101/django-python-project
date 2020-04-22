from django.shortcuts import render,get_object_or_404,redirect
from .models import Contact
from django.views.generic import ListView,DetailView
from django.db.models import Q
from django.views.generic.edit import CreateView , UpdateView ,DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin #for class view
from django.contrib.auth.decorators import login_required #for function view
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.

@login_required
def home(request):
    context = {
        'contacts':Contact.objects.all()
    }
    return render(request,'index.html',context)


@login_required
def detail(request,id):
    context={
        'contact':get_object_or_404(Contact,pk=id)
    }
    return render(request,'detail.html',context)

class HomePageView(LoginRequiredMixin,ListView):
    template_name = 'index.html'
    model = Contact
    context_object_name = 'contacts'

    def get_queryset(self):
        contacts = super().get_queryset()
        return contacts.filter(manager =self.request.user)


class ContactDetailView(LoginRequiredMixin,DetailView):
    template_name = 'detail.html'
    model = Contact
    context_object_name = 'contact'



@login_required
def search(request):
    if request.GET:
        search_term=request.GET['search_term']
        search_results = Contact.objects.filter(
            Q(name__icontains=search_term) |
            Q(email__iexact=search_term) |
            Q(phone__iexact=search_term) |
            Q(info__icontains=search_term)
        )
        context = {
            'search_term' :search_term,
            'contacts' : search_results.filter(manager=request.user)
        }
        return render(request,'search.html',context)
    else:
        return redirect('home')

class ContactCreateView(LoginRequiredMixin,CreateView):
    model  = Contact
    template_name = 'create.html'
    fields =['name','email','info','phone',"birth_date",'gender','image']
    
    def form_valid(self,form):
        instance = form.save(commit=False)
        instance.manager = self.request.user
        instance.save()
        messages.success(self.request,'Your contact successfully saved')
        return redirect('home')


class ContactUpdateView(LoginRequiredMixin,UpdateView):
    model  = Contact
    template_name = 'update.html'
    fields =['name','email','info','phone',"birth_date",'gender','image']
    
    def form_valid(self,form):
        instance = form.save()
        messages.success(self.request,'Your contact successfully updated')
        return redirect('detail',instance.pk)

class ContactDeleteView(LoginRequiredMixin,DeleteView):
    model = Contact
    template_name = 'delete.html'
    success_url ='/'

    def delete(self,request, *args , **kwargs):
        messages.success(self.request,'Your contact successfully deleted')
        return super().delete(self,request, *args , **kwargs)        

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
