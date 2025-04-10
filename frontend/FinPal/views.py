from django.shortcuts import render, redirect

#this should be in the backend login
import bcrypt
import boto3
import os
from dotenv import load_dotenv

load_dotenv()
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id= os.getenv("AWS_ACCESS_KEY_ID_dynamo"), 
    aws_secret_access_key= os.getenv("AWS_SECRET_ACCESS_KEY_dynamo"),
    region_name='us-east-2'
)
table = dynamodb.Table('Ramblin_Hackathon_Users')

def checkUserExists(username):
        response = table.get_item(Key={'username': username})
        # print(response, "checkUser")
        if 'Item' in response:
            return True
        return False

def checkPassword(username, password):
    #get user data from DynamoDB and check username exists
    response = table.get_item(Key={'username': username})
    # print(username)
    # print(response)
    if 'Item' not in response:
        return False 
    
    #get stored password from DynamoDB and check pass
    storedPasswordHash = response['Item'].get('password')
    if not storedPasswordHash:
        return False 
    if bcrypt.checkpw(password.encode('utf-8'), storedPasswordHash.encode('utf-8')):
        return True 
    return False 

def storePassword(username, password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    #store the hashed password in DynamoDB
    response = table.put_item(
        Item={
            'username': username,
            'password': hashed_password.decode('utf-8')  
        }
    )
    return True
#end of login backend


#start of plaid backend

def fetch_plaid_account_data():
    return {
        'checking_accounts': [
            {"name": "Platypus Federal Reserve Bank Checking", "balance": 1500.00},
            {"name": "Bank of Timbuktu Checking", "balance": 2300.00},
            {"name": "Cloudsdale Valley Checking", "balance": 1800.00},
            {"name": "Infinity Checking", "balance": 600.00}
        ],
        'credit_accounts': [
            {"name": "Platypus Federal Reserve Bank Credit Card", "balance": 500.00},
            {"name": "Cloudsdale Valley Credit Card", "balance": 200.00},
            {"name": "Infinity Credit Card", "balance": 500.00},
            {"name": "Bank of Timbuktu Credit Card", "balance": 320.00}
        ]
    }


def getTotalCheckingAccounts():
    accounts_data = fetch_plaid_account_data()
    checking_accounts = accounts_data['checking_accounts']
    return [(account['name'], account['balance']) for account in checking_accounts]

def getTotalCreditAccounts():
    accounts_data = fetch_plaid_account_data()
    credit_accounts = accounts_data['credit_accounts']
    return [(account['name'], account['balance']) for account in credit_accounts]

def getTotalCheckingMoney():
    accounts_data = fetch_plaid_account_data()
    checking_accounts = accounts_data['checking_accounts']
    return sum(account['balance'] for account in checking_accounts)


def getTotalCreditMoney():
    accounts_data = fetch_plaid_account_data()
    credit_accounts = accounts_data['credit_accounts']
    return sum(account['balance'] for account in credit_accounts)


#end of plaid


def chat(request):
    return render(request, 'chat.html')

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def dashboardView(request):
    checkingAccounts = getTotalCheckingAccounts()
    creditAccounts = getTotalCreditAccounts()

    checkingTotal = getTotalCheckingMoney()
    creditTotal = getTotalCreditMoney()
    netBal = checkingTotal - creditTotal
    return render(request, 'dashboard.html', 
                  {'checkingAccounts': checkingAccounts, 
                   'creditAccounts' : creditAccounts, 
                   'totalSaved': checkingTotal, 
                   'totalUsed': creditTotal, 
                   'netBalance' : netBal})

def loginCheck(request):
    username = request.POST.get('username')
    password = request.POST.get('password')  
    
    userExists = checkUserExists(username)
    passwordExists = checkPassword(username, password)
    
    if not userExists:
        # error message here instead of going back to login
        errorMessage = "User does not exist. Please register."
        return render(request, 'login.html', {'error_message': errorMessage})
    
    if not passwordExists:
        errorMessage = "Incorrect password. Please try again."
        return render(request, 'login.html', {'error_message': errorMessage})
    
    #if login is successful go to dashboard
    return redirect('dashboard')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if checkUserExists(username):
            return render(request, 'signup.html', {'error_message': 'Username already exists. Please choose another.'})

        storePassword(username, password)
        return render(request, 'signup.html', {'success_message': 'Account created! Please log in.'})

    return render(request, 'signup.html')

def signupCheck(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'signup.html', {'error_message': 'Passwords do not match.'})

        if checkUserExists(username):
            return render(request, 'signup.html', {'error_message': 'Username already exists. Please choose another.'})

        storePassword(username, password)
        return render(request, 'signup.html', {'success_message': 'Account created! Please log in.'})

    return redirect('signup')

def logout_view(request):
    return redirect('home')  # Make sure 'home' is a valid URL name



