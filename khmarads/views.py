from django.shortcuts import render
# Create your views here.
from khmarads.models import Ad , Comment , Fav
from khmarads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import path, reverse_lazy , reverse
from .forms import Signup
from django.shortcuts import render,get_object_or_404,redirect  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from khmarads.forms import CreateForm , CommentForm
from django.http import HttpResponse
from django.db.models import Q
class AdListView(View):
    def get(self,request):
        model = Ad
        ad_list = Ad.objects.all()
        stval = request.GET.get("search", False)
        if stval:
            ad_list = ad_list.filter(Q(title__contains = stval)|Q(text__contains = stval))
        if request.user.is_authenticated:
            thing_list = Fav.objects.all()
            rows = thing_list.filter(owner= self.request.user)
            favorites = [ row.ad for row in rows ]
            ctx = {'ad_list' : ad_list, 'favorites': favorites}
            return render(request, 'khmarads/Ad_list.html', ctx)
        return render(request,'khmarads/Ad_list.html',{'ad_list' : ad_list})
    # By convention:
    # template_name = "myarts/Ad_list.html"

class AdDetailView(LoginRequiredMixin , View):
    def get(self ,request, pk):
        model = Ad.objects.get(id = pk)
        list_of_comments = Comment.objects.filter(ad=model).order_by('-updated_at')
        comment_form = CommentForm
        ctx = {'comments':list_of_comments , 'form':comment_form, 'ad':model ,}
        return render(request , 'khmarads/Ad_detail.html' , ctx)
class AdDeleteView(OwnerDeleteView):
    model = Ad

'''class Regist(CreateView):
    model = User
    fields = '__all__'
    success_url = reverse_lazy('khmarads:all')
'''
def registration(request):
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create_user(username,email,password,)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return redirect(reverse('login'))
    else:
        form = Signup()
    return render(request,'khmarads/signup.html',{'form':form})
def jstest(request):
    ctx = { 'User': User.username }
    return render(request , 'khmarads/jstest.html', ctx)

class AdCreateView(LoginRequiredMixin,View):
    template_name = 'khmarads/Ad_form.html'
    success_url = reverse_lazy('khmarads:all')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)

class AdUpdateView(LoginRequiredMixin,View):
    template_name = 'khmarads/Ad_form.html'
    success_url = reverse_lazy('khmarads:all')
    def get(self, request, pk) :
        pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
        print('-1', pic)
        form = CreateForm(instance=pic)
        print('0', pic)
        ctx = { 'form': form }
        return render(request, self.template_name, ctx)
    def post(self, request, pk) :
        pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None,instance=pic)
        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        print('1', pic)
        pic = form.save(commit=False)
        print('2', pic)
        pic.save()
        print('3', pic)
        return redirect(self.success_url)
def stream_file(request, pk) :
    pic = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response
class CommentCreateView(LoginRequiredMixin , View):
    template= 'khmarads/Ad_comment_create.html'
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user,  ad =f)
        comment.save()
        return redirect(reverse_lazy('khmarads:ad_detail', args=[pk]))
class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = 'khmarads/Ad_comment_delete.html'
    def get_success_url(self):
        ad = self.object.ad
        return reverse('khmarads:ad_detail', args=[ad.id])

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin , View):
    def post(self, request , pk):
        ad = get_object_or_404(Ad, id =pk)
        fav = Fav(owner = request.user ,ad = ad)
        try:
            fav.save()
        except IntegrityError as e:
            pass
        return HttpResponse()
@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin , View):
    def post(self, request , pk):
        ad = get_object_or_404(Ad, id = pk)
        fav = Fav.objects.get(owner = request.user ,ad = ad)
        try:
            fav.delete()
        except:
            pass
        return HttpResponse()
        

