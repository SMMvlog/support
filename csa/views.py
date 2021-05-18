from django.shortcuts import render,redirect
from .models import CustomerEnquiry
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
# Create your views here.

def Home(request):
    return render(request,'home.html')

def Query(request):
    if request.method == "POST":
        name = request.POST['name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        queries = request.POST['queries']
        cust=CustomerEnquiry(name=name, mobile=mobile, email=email, queries=queries)
        cust.save()
        id = cust.id
        url = f"http://127.0.0.1:8000/{id}"
        send_mail('Support Desk mail',f'The Consumer Name is {name} And the Consumer mail id is {email}\n The Consumer Query: {queries}  \n you can response him by this link: {url}',None,[settings.EMAIL_HOST_USER],fail_silently=False)
        messages.success(request,f"Thank You Mr.{name} for Your Valueable feedback we will be get back soon!!")
        return redirect("/")
    return render(request,'query.html')
    
def Resp(request,id):
    url = f"http://127.0.0.1:8000/review"
    enq = CustomerEnquiry.objects.get(id=id)
    if request.method == "POST":
        resp = request.POST.get('resp') 
        send_mail('Thank for your Suggestion',f'Hello Mr. {enq.name}\n as per you Suggestion {resp}\n \n You can rate us by this link: {url}',None,[enq.email],fail_silently=False)  
    enq = CustomerEnquiry.objects.get(id=id)
    return render(request,'response.html',{'enq':enq})

def Review(request):
    return render(request,'review.html')