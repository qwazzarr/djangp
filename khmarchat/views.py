
# Create your views here.
from khmarchat.models import Message , Message2
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import path, reverse_lazy , reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
#from .forms import Signup
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404,redirect 
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth.models import User
# Create your views here.
class TalkMain(LoginRequiredMixin, View):
    def get(self, request):
        return render(request , 'khmarchat/talk.html' , {'user_list':User.objects.all()})  
    def post(self, request):
        message = Message(text = request.POST['message'] , owner = request.user)
        message.save()
        return redirect(reverse('kchat:talk'))
class TalkMessages(LoginRequiredMixin , View):
    def get(self, request):
        messages = Message.objects.all().order_by('-created_at')[:10]
        results = []
        for message in messages:
            result = [message.text , naturaltime(message.created_at)]
            results.append(result)
        return JsonResponse(results, safe = False)
class PrivateTalk(LoginRequiredMixin , View):
    def get(self , request , pk):
        user = User.objects.get(pk = pk)
        return render(request , 'khmarchat/privatetalk.html', {'pk':pk , 'fname': user.first_name} , ) 
    def post(self , request , pk):
        message = Message2(text = request.POST['message'] , owner = request.user, recipient = User.objects.get(pk = pk))
        message.save()
        return redirect(reverse('kchat:privatetalk',kwargs={'pk':pk}))
class PrivateMessages(LoginRequiredMixin , View):
    def get(self, request , pk ):
        reciever = User.objects.get(pk = pk)
        messages = Message2.objects.filter(owner = request.user , recipient = reciever)
        messages2 = Message2.objects.filter(owner = reciever , recipient = request.user )
        messages3 = messages | messages2 
        results = []
        for message in messages3:
            result = [message.text , naturaltime(message.created_at)]
            results.append(result)
        return JsonResponse(results, safe = False)
