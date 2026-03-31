from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # ✅ Auto login after signup
            login(request, user)

            # ✅ Success message
            messages.success(request, "Account created successfully!")

            return redirect('expense_list')  # go directly to dashboard

        else:
        
            messages.error(request, "Please correct the errors below.")

    else:
        form = UserCreationForm()

    return render(request, 'users/signup.html', {'form': form})