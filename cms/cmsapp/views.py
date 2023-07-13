from django.shortcuts import render,redirect,HttpResponse
from .models import Post
from .forms import PostForm
from.models import Contact
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post
from django.contrib.auth.forms import PasswordResetForm



# Create your views here.
@login_required(login_url='login')
def index(request):
    posts= Post.objects.all()
    page = request.GET.get('page')
    num_of_items = 3
    paginator = Paginator(posts, num_of_items)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page=1
        posts= paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)
    
    context={'posts':posts, 'paginator':paginator}
    
    return render(request,'cmsapp/index.html',context)

def about(request):
    return render(request,'cmsapp/about.html')

def detail(request,slug):
    post=Post.objects.get(slug=slug)
    posts = Post.objects.exclude(post_id__exact=post.post_id)[:5]
    context ={'post':post,'posts':posts}
    return render(request, 'cmsapp/detail.html', context)


def createPost(request):
    profile = request.user.userprofile
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid:
            post= form.save(commit=False)
            post.slug = slugify(post.title)
            post.writer = profile
            post.save()
            messages.info(request, 'Artical Created Successfuly!!')
            return redirect('create')
        else:
            messages.error(request, 'Artical not Created ERROR!!')
    context={'form': form}
    return render(request, 'cmsapp/create.html',context)

def updatePost(request, slug):
    post= Post.objects.get(slug=slug)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.info(request, 'Artical Updated Successfuly!!')

            return redirect('detail', slug=post.slug)
    context = {'form': form}
    return render(request, 'cmsapp/create.html', context)

def deletePost(request,slug):
    post=Post.objects.get(slug=slug)
    form=PostForm(instance=post)
    if request.method =='POST':
        post.delete()
        messages.info(request, 'Artical Deleted Successfuly!!')
        return redirect('index')
    context={'form': form}
    return render(request,'cmsapp/delete.html', context)


def contact(request):
    if request.method == 'POST':
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        subject = request.POST.get('subject')
        
        contact.name=name
        contact.email=email
        contact.number=number
        contact.subject=subject
        
        contact.save()
        messages.info(request, 'Submited Successfuly!!')
        
    return render(request,'cmsapp/contact.html')


def usersignup(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1!=pass2:
            return HttpResponse('your password incorrect...')
        else:
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')  
    return render(request,'cmsapp/signup.html') 

def userlogin(request):
   if request.method == 'POST':
       username= request.POST.get('username')
       pass1 = request.POST.get('password')
       user = authenticate(request,username=username,password=pass1)
       if user is not None:
           login(request,user)
           return redirect ('index')
       else:
           return HttpResponse("Username or Password is incorrect !!!")
   return render(request, 'cmsapp/login.html') 
def signout(request):
    logout(request)
    return redirect("index")


def search(request):
    # posts= Post.objects.all()
    query= request.GET['query']
    if len(query)>50:
        posts=Post.objects.none()
    else:
        postsTitle= Post.objects.filter(title__icontains=query)
        postsBody= Post.objects.filter(body__icontains=query)
        posts=postsTitle.union(postsBody)
        
    if posts.count() ==0:
        messages.error(request, "No search results found. Please refine your query..!!!")
    params = {'posts':posts, 'query':query}
    return render(request, 'cmsapp/search.html', params)
# 

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                from_email='noreply@example.com',
                email_template_name='cmsapp/reset_password_email.html',
                subject_template_name='cmsapp/reset_password_subject.txt'
            )
            messages.success(request, 'Password reset email has been sent.')
            return redirect('cmsapp:forgot_password')
    else:
        form = PasswordResetForm()
    
    return render(request, 'cmsapp/forgot_password.html', {'form': form})