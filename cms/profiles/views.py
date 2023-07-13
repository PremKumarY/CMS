from django.shortcuts import render,redirect,HttpResponse
from .models import UserProfile
from .forms import UpdateProfileForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def profile(request, pk):
    user_profile = UserProfile.objects.get(profile_id=pk)
    context = {'profile': user_profile}
    return render(request, 'profiles/profile.html', context)

def account(request):
    user_account = request.user.userprofile
    context ={ 'account': user_account}
    return render(request, 'profiles/account.html', context)



# 
from django.shortcuts import render, redirect
from .forms import UpdateProfileFullForm

def  UpdateProfile(request):
    if request.method == 'POST':
        form = UpdateProfileFullForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the user fields
            user = form.save(commit=False)
            user.save()

            # Save the user profile fields
            user_profile = form.cleaned_data['user_profile']
            user_profile.user = user
            user_profile.save()
            messages.info(request, 'You updated your Profile')
            return redirect('account') 

    else:
        form = UpdateProfileFullForm()

    return render(request, 'profiles/updateprofile.html', {'form': form})

# 


# def UpdateProfile(request):
#     profile = request.user.userprofile
#     form =  UpdateProfileForm( instance=profile)
#     if request.method == 'POST':
#         form = UpdateProfileForm(request.POST, request.FILES, instance = profile)
#         if form.is_valid():
#             form.save()
#             messages.info(request, 'You updated your Profile')
#             return redirect('account')
        
#     context = {'form': form}
#     return render(request, 'profiles/updateprofile.html', context)
    
def DeleteProfile(request):
    profile =request.user.userprofile
    form = UpdateProfileForm (instance=profile)
    if request.method =='POST':
       profile.delete()
       user = request.user
       user.delete() 
       return redirect('index')
    context={'form':form}
    return render(request, 'profiles/deleteprofile.html', context)

def changepassword(request):
    context={}
    if request.method=='POST':
        current = request.POST["npwd"]
        new_pas= request.POST["cpwd"]
        
        user =User.objects.get(id=request.user.id)
        check =user.check_password(current)
        if check==True:
           pass
        else:
           context["msz"] = "Incorrect Password"
           context["col"] = "alert-danger"
           
    return render(request,"profiles/changepassword.html")
