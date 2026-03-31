from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import Profile
from .forms import ProfileForm

# SIGNUP
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = UserCreationForm()

    return render(request, 'users/signup.html', {'form': form})


# LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # ✅ Django's login
            messages.success(request, "Login successful!")
            return redirect('expense_list')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'users/login.html')



from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")

            return redirect('profile')   # ✅ VERY IMPORTANT

        else:
            print(form.errors)  # 🔍 DEBUG

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/profile.html', {'form': form})
    