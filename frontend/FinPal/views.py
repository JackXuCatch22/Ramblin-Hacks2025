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
def getTotalCheckingAccounts():
    return [
        ("A", 10),
        ("B", 20),
        ("C", 30),
        ("D", 40)
    ]

def getTotalCreditAccounts():
    return [
        ("1", 20),
        ("2", 30),
    ]

def getTotalCheckingMoney():
    return 100

def getTotalCreditMoney():
    return 50


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


