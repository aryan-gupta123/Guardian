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
        {'id': 1, 'merchant': 'Enron', 'merchant_id': 40101, 'amount': 2480.00, 'risk_level': 'Risky', 'risk_score': 0.95, 'ticker': 'ENRN.Q', 'timestamp': '2024-01-15 09:05:00'},
        {'id': 2, 'merchant': 'Theranos', 'merchant_id': 40102, 'amount': 1650.00, 'risk_level': 'Risky', 'risk_score': 0.92, 'ticker': 'THRN.P', 'timestamp': '2024-01-15 09:40:00'},
        {'id': 3, 'merchant': 'FTX Trading', 'merchant_id': 40103, 'amount': 5100.00, 'risk_level': 'Risky', 'risk_score': 0.97, 'ticker': 'FTX', 'timestamp': '2024-01-15 10:25:00'},
        {'id': 4, 'merchant': 'Wirecard AG', 'merchant_id': 40104, 'amount': 3215.00, 'risk_level': 'Risky', 'risk_score': 0.9, 'ticker': 'WDI', 'timestamp': '2024-01-15 11:10:00'},
        {'id': 5, 'merchant': 'Bernie Madoff Investment Securities', 'merchant_id': 40105, 'amount': 6850.00, 'risk_level': 'Risky', 'risk_score': 0.99, 'ticker': 'MADOFF', 'timestamp': '2024-01-15 11:55:00'},
        {'id': 6, 'merchant': 'Luckin Coffee', 'merchant_id': 40106, 'amount': 890.00, 'risk_level': 'Risky', 'risk_score': 0.78, 'ticker': 'LKNCY', 'timestamp': '2024-01-15 12:40:00'},
        {'id': 7, 'merchant': 'Satyam Computer Services', 'merchant_id': 40107, 'amount': 1475.00, 'risk_level': 'Risky', 'risk_score': 0.82, 'ticker': 'SAY', 'timestamp': '2024-01-15 13:15:00'},
        {'id': 8, 'merchant': 'Berkshire Hathaway', 'merchant_id': 50101, 'amount': 420.00, 'risk_level': 'Safe', 'risk_score': 0.08, 'ticker': 'BRK.A', 'timestamp': '2024-01-15 14:00:00'},
        {'id': 9, 'merchant': 'Apple Inc.', 'merchant_id': 50102, 'amount': 180.00, 'risk_level': 'Safe', 'risk_score': 0.12, 'ticker': 'AAPL', 'timestamp': '2024-01-15 14:45:00'},
        {'id': 10, 'merchant': 'Microsoft Corporation', 'merchant_id': 50103, 'amount': 235.00, 'risk_level': 'Safe', 'risk_score': 0.1, 'ticker': 'MSFT', 'timestamp': '2024-01-15 15:30:00'},
        {'id': 11, 'merchant': 'Costco Wholesale', 'merchant_id': 50104, 'amount': 95.50, 'risk_level': 'Safe', 'risk_score': 0.06, 'ticker': 'COST', 'timestamp': '2024-01-15 16:05:00'},
        {'id': 12, 'merchant': 'Visa Inc.', 'merchant_id': 50105, 'amount': 310.00, 'risk_level': 'Safe', 'risk_score': 0.14, 'ticker': 'V', 'timestamp': '2024-01-15 16:40:00'},
        {'id': 13, 'merchant': 'JPMorgan Chase', 'merchant_id': 50106, 'amount': 560.00, 'risk_level': 'Medium', 'risk_score': 0.38, 'ticker': 'JPM', 'timestamp': '2024-01-15 17:25:00'},
        {'id': 14, 'merchant': 'Patagonia', 'merchant_id': 50107, 'amount': 145.00, 'risk_level': 'Safe', 'risk_score': 0.05, 'ticker': 'PRIVATE', 'timestamp': '2024-01-15 18:10:00'},
        {'id': 15, 'merchant': 'Lehman Brothers (Estate)', 'merchant_id': 40108, 'amount': 2725.00, 'risk_level': 'Risky', 'risk_score': 0.88, 'ticker': 'LEHMQ', 'timestamp': '2024-01-15 18:45:00'},
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
