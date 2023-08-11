from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserSignupForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout

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

@login_required()
def profile(request, username):
    """
    Renders the users profile, checks that the user matches profile user
    """
    # user = get_object_or_404(User, username=username)
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)

    context = {
        "profile": profile,
    }

    return render(request, "users/profile.html", context)

@login_required
def edit_profile(request, username):
    user = request.user
    # user = User.objects.get(username=username)
    p_user = get_object_or_404(User, username=username)
    
    profile = Profile.objects.get(user=p_user)
    if profile.user != user and not user.is_superuser:
        messages.error(request, "You are not authorized to edit this review.")
        return redirect(reverse("profile" , kwargs={'username': username}))

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, f'Your account has been updated!')
        
            return redirect('profile', username=username)

    else:
        user_form = UserUpdateForm(instance=p_user)
        profile_form = ProfileUpdateForm(instance=p_user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
        'user':user,
    }

    return render(request, 'users/edit_profile.html', context)

@login_required()
def delete_profile(request, username):
    
    
    user = request.user
    # user = User.objects.get(username=username)
    p_user = get_object_or_404(User, username=username)
    
    profile = Profile.objects.get(user=p_user)
    if not user.is_superuser and profile.user != user:
        messages.error(
            request, "You are not authorized to delete this review."
        )
        return redirect(reverse(f'{restaurant.category}'))

    if request.method == "POST":
        if not user.is_superuser:
            logout(request)
        p_user.delete()
        
        if user.is_superuser:
            messages.success(request, f"account has been deleted ")
        else:
            messages.success(request, f"Your account has been deleted {user.username} ")
        return redirect("dublineats-home")

    context = {"username": username}
    return render(request, "users/edit_profile.html", context)
