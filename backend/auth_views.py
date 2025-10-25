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
        {'id': 1, 'merchant': 'Tesla, Inc.', 'amount': 120.50, 'risk_level': 'Safe', 'risk_score': 0.2, 'ticker': 'TSLA', 'timestamp': '2024-01-15 10:30:00'},
        {'id': 2, 'merchant': 'Apple Store', 'amount': 55.20, 'risk_level': 'Safe', 'risk_score': 0.1, 'ticker': 'AAPL', 'timestamp': '2024-01-15 11:15:00'},
        {'id': 3, 'merchant': 'Crypto Exchange', 'amount': 1500.00, 'risk_level': 'Risky', 'risk_score': 0.9, 'ticker': 'CRYPTO', 'timestamp': '2024-01-15 12:00:00'},
        {'id': 4, 'merchant': 'Starbucks', 'amount': 12.75, 'risk_level': 'Safe', 'risk_score': 0.1, 'ticker': 'SBUX', 'timestamp': '2024-01-15 13:45:00'},
        {'id': 5, 'merchant': 'Amazon', 'amount': 780.00, 'risk_level': 'Medium', 'risk_score': 0.6, 'ticker': 'AMZN', 'timestamp': '2024-01-15 14:30:00'},
        {'id': 6, 'merchant': 'Microsoft', 'amount': 250.00, 'risk_level': 'Safe', 'risk_score': 0.2, 'ticker': 'MSFT', 'timestamp': '2024-01-15 15:15:00'},
        {'id': 7, 'merchant': 'Unknown Merchant', 'amount': 5200.00, 'risk_level': 'Risky', 'risk_score': 0.95, 'ticker': 'UNKNOWN', 'timestamp': '2024-01-15 16:00:00'},
        {'id': 8, 'merchant': 'Google', 'amount': 30.00, 'risk_level': 'Safe', 'risk_score': 0.1, 'ticker': 'GOOGL', 'timestamp': '2024-01-15 16:45:00'},
        {'id': 9, 'merchant': 'Meta', 'amount': 950.00, 'risk_level': 'Medium', 'risk_score': 0.7, 'ticker': 'META', 'timestamp': '2024-01-15 17:30:00'},
        {'id': 10, 'merchant': 'Netflix', 'amount': 85.00, 'risk_level': 'Safe', 'risk_score': 0.3, 'ticker': 'NFLX', 'timestamp': '2024-01-15 18:15:00'},
    ]

    risk_counts = {
        'safe': sum(1 for t in transactions if t['risk_level'] == 'Safe'),
        'medium': sum(1 for t in transactions if t['risk_level'] == 'Medium'),
        'risky': sum(1 for t in transactions if t['risk_level'] == 'Risky'),
    }

    context = {
        'username': request.user.username,
        'transactions': transactions,
        'risk_counts': risk_counts,
    }
    return render(request, 'dashboard.html', context)