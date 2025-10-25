from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('homepage')

@login_required
def dashboard_view(request):
    # Dummy data for the transaction table
    transactions = [
        {'id': 1, 'merchant': 'GlobalTech Solutions', 'amount': 120.50, 'risk': '🟢 Safe', 'actions': ['View', 'More']},
        {'id': 2, 'merchant': 'QuickMart Groceries', 'amount': 55.20, 'risk': '🟢 Safe', 'actions': ['View', 'More']},
        {'id': 3, 'merchant': 'ElectroGadget Store', 'amount': 1500.00, 'risk': '🔴 Risky', 'actions': ['Block', 'View', 'More']},
        {'id': 4, 'merchant': 'Coffee Bean Cafe', 'amount': 12.75, 'risk': '🟢 Safe', 'actions': ['View', 'More']},
        {'id': 5, 'merchant': 'Travel Adventures Inc.', 'amount': 780.00, 'risk': '🟡 Medium', 'actions': ['Review', 'View', 'More']},
        {'id': 6, 'merchant': 'Online Gaming Hub', 'amount': 250.00, 'risk': '🟢 Safe', 'actions': ['View', 'More']},
        {'id': 7, 'merchant': 'Luxury Watches Co.', 'amount': 5200.00, 'risk': '🔴 Risky', 'actions': ['Block', 'View', 'More']},
        {'id': 8, 'merchant': 'Local Bookstore', 'amount': 30.00, 'risk': '🟢 Safe', 'actions': ['View', 'More']},
        {'id': 9, 'merchant': 'International Payments', 'amount': 950.00, 'risk': '🟡 Medium', 'actions': ['Review', 'View', 'More']},
        {'id': 10, 'merchant': 'Gadget Repair Shop', 'amount': 85.00, 'risk': '🟢 Safe', 'actions': ['View', 'More']},
    ]

    risk_counts = {
        'safe': sum(1 for t in transactions if 'Safe' in t['risk']),
        'medium': sum(1 for t in transactions if 'Medium' in t['risk']),
        'risky': sum(1 for t in transactions if 'Risky' in t['risk']),
    }

    context = {
        'username': request.user.username,
        'transactions': transactions,
        'risk_counts': risk_counts,
    }
    return render(request, 'dashboard.html', context)