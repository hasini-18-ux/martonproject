from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.http import HttpResponse
import logging
from .models import Post,About,Category
from django.core.paginator import Paginator
from .forms import ContactForm, LoginForm,RegisterForm,ForgotPasswordForm,ResetPasswordForm
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group
def detail(request,slug):
    #post=next((item for item in posts if item['id']==int(post_id)),None)
    if request.user and not request.user.has_perm('amazon.view_post'):
        messages.error(request,'You have no permission to view any post')
        return redirect('amazon:index')
    try:
        post=Post.objects.get(slug=slug)
        related_posts=Post.objects.filter(category=post.category).exclude(pk=post.id)
    except Post.DoesNotExist:
        return HttpResponse("Post not found", status=404)
    #logger=logging.getLogger("TESTING")
    #logger.debug(f'Post variable is {post}')
    return render(request,'amazon/detail.html',{'post':post,'related_posts':related_posts})
def old_url_redirect(request):
    return redirect(reverse('amazon:new_url'))
def new_page_url(request):
    return HttpResponse("This is the new URL.")
def index(request):
    amazon_title="Fashion Place"
    all_posts=Post.objects.filter(is_published=True)
    paginator=Paginator(all_posts,3)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'amazon/index.html',{'amazon_title':amazon_title,'page_obj':page_obj})
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        logger=logging.getLogger("TESTING")
        if form.is_valid():
            print(ContactForm.__mro__)
            form.save()
            logger.debug(f'Post Data is {form.cleaned_data["name"]} {form.cleaned_data["email"]} {form.cleaned_data["message"]}')
            success_message = "Thank you for contacting us! We will get back to you soon."
            return render(request,'amazon/contact.html',{'success_message': success_message})
        else:
            logger.debug(f'form is invalid')
            return render(request,'amazon/contact.html',{'form': form,'name':name,'email':email,'message':message})
        
    return render(request,'amazon/contact.html')
def about(request):
    about_content=About.objects.first().content
    return render(request,'amazon/About.html',{'about_content':about_content})
def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        name=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save() 
            readers_group,created=Group.objects.get_or_create(name="Readers")
            user.groups.add(readers_group)
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect("/blog/login")
        else:
            print("Form is invalid")
            return render(request,'amazon/register.html',{'form':form,'username':name,'email':email,'password':password})
    else:
        form=RegisterForm()
    return render(request,'amazon/register.html',{'form':form})
def login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        name=request.POST.get('username')
        password=request.POST.get('password')
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                auth_login(request,user)
                print("login Successfull")
                return redirect('amazon:index')
        else:
            print("Form is invalid")
            return render(request,'amazon/login.html',{'form':form,'username':name,'password':password})
    else:
        form=LoginForm()
    return render(request,'amazon/login.html',{'form':form})
def fashionhub(request):
    title="MARTON"
    #getting the posts of user
    all_posts=Post.objects.filter(user=request.user)
    #paginate
    paginator=Paginator(all_posts,3)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'amazon/fashionhub.html',{'title':title,'page_obj':page_obj})
def logout(request):
    auth_logout(request)
    return redirect("/blog/")
def forgotpassword(request):
    form=ForgotPasswordForm()
    if request.method=='POST':
        form=ForgotPasswordForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            user=User.objects.get(email=email)
            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            current_site=get_current_site(request)
            domain=current_site.domain
            subject="Reset Password requested"
            message=render_to_string('amazon/reset_password_email.html',{'domain':domain,'uid':uid,'token':token})
            send_mail(subject,message,'pghasini2006@gmail.com',[email])
            messages.success(request,"Email has been sent")

    return render(request,'amazon/forgotpassword.html',{'form':form})
def resetpassword(request,uidb64, token):
    form=ResetPasswordForm()
    if request.method=='POST':
        form=ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password=form.cleaned_data['new_password']
            try:
                uid=urlsafe_base64_decode(uidb64)
                user=User.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user=None
            if user is not None and default_token_generator.check_token(user,token):
                user.set_password(new_password)
                user.save()
                messages.success(request,"Your password has been reset successfully")
                return redirect('amazon:login')
            else:
                messages.error(request,"The password reset link is invalid")

    return render(request,"amazon/resetpassword.html",{'form':form})

@login_required
@permission_required("amazon.add_post",raise_exception=True)
def new_post(request):
    categories=Category.objects.all()
    form=PostForm()
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('amazon:fashionhub')
    return render(request,'amazon/newpost.html',{'categories':categories,'form':form})

@login_required
@permission_required("amazon.change_post",raise_exception=True)
def edit_post(request,post_id):
    categories=Category.objects.all()
    post=get_object_or_404(Post,id=post_id)
    form=PostForm()
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,"Your post has been updated successfully")
            return redirect("amazon:fashionhub")
    return render(request,'amazon/edit_post.html',{'categories':categories,'post':post,'form':form})
@login_required
@permission_required("amazon.delete_post",raise_exception=True)
def delete_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    post.delete()
    messages.success(request,"Post deleted successfully")
    return redirect("amazon:fashionhub")

@login_required
@permission_required("amazon.can_publish",raise_exception=True)
def publish_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    post.is_published=True
    post.save()
    messages.success(request,"Post published successfully")
    return redirect("amazon:fashionhub")

