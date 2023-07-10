from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserSignupForm, UserUpdateForm, ProfileUpdateForm
# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Signup Succesful {username}!You May Now Log In!')
            form.save()
            return redirect('userlogin')
    else:
        form = UserSignupForm()
    return render(request, 'users/signup.html', {'form': form})



@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, f'Your account has been updated!')
        
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
        'user':user,
    }

    return render(request, 'users/profile.html', context)
