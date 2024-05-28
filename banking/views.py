from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def account_details(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'banking/account_details.html', {'account': account, 'transactions': transactions})

@login_required
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(user=request.user)
            if transaction.transaction_type == 'deposit':
                transaction.account.balance += transaction.amount
            elif transaction.transaction_type == 'withdraw' and transaction.account.balance >= transaction.amount:
                transaction.account.balance -= transaction.amount
            else:
                return render(request, 'banking/transaction.html', {'form': form, 'error': 'Insufficient balance'})
            transaction.account.save()
            transaction.save()
            return redirect('account_details')
    else:
        form = TransactionForm()
    return render(request, 'banking/transaction.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Account.objects.create(user=user, account_number=f"ACC{user.id:04d}")
            return redirect('account_details')
    else:
        form = UserCreationForm()
    return render(request, 'banking/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('account_details')
    else:
        form = AuthenticationForm()
    return render(request, 'banking/login.html', {'form': form})


@login_required
def check_balance(request):
    account = Account.objects.get(user=request.user)
    return render(request, 'banking/check_banking.html', {'account': account})