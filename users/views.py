from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserSignupForm
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
def profile(request):
    
    profile = Profile.objects.get(user=request.user)


    return render(request, 'users/profile.html', {'profile': profile})
