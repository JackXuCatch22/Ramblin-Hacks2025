from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
#this should be in the backend login
import bcrypt
import boto3
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id= os.getenv("AWS_ACCESS_KEY_ID_dynamo"), 
    aws_secret_access_key= os.getenv("AWS_SECRET_ACCESS_KEY_dynamo"),
    region_name='us-east-2'
)
table = dynamodb.Table('Ramblin_Hackathon_Users')


def chat(request):
    return render(request, 'chat.html')

@csrf_exempt
@api_view(['POST'])

def chat_with_bot(request):
    gtca = "Total checking accounts: " + str(getTotalCheckingAccounts())
    tca = "Total credit accounts: " + str(getTotalCreditAccounts())
    gtcm = "Total checking money: " + str(getTotalCheckingMoney())
    gtcma = "Total credit money: " + str(getTotalCreditMoney())

    stuff = gtca + " | " + tca + " | " + gtcm + " | " + gtcma

    user_message = request.data.get('message')

    if not user_message:
        return Response({"error": "No message provided"}, status=400)

    try:
        classification = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a classifier. "
                        "Determine if the user's question is mainly about finance, money, banking, saving, budgeting, investing, debt, loans, or credit. "
                        "If YES, respond ONLY with 'yes'. If NOT, respond ONLY with 'no'. "
                        "NO extra words. Just 'yes' or 'no'."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        classification_response = classification.choices[0].message.content.strip().lower()

        print(f"Classification result: {classification_response}")

        if classification_response.startswith("n"):
            return Response({"botResponse": "This is not a question related to finance. Please ask me something else."})

        prompt = (
            "You are a helpful financial advisor. "
            "Explain financial concepts clearly in under 70 words, in a way teenagers can understand. "
            f"User's financial information: {stuff}"
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        bot_response = completion.choices[0].message.content
        return Response({"botResponse": bot_response})

    except Exception as e:
        return Response({"error": f"Internal server error: {str(e)}"}, status=500)


def checkUserExists(username):
        response = table.get_item(Key={'username': username})
        if 'Item' in response:
            return True
        return False

def checkPassword(username, password):
    response = table.get_item(Key={'username': username})
    if 'Item' not in response:
        return False 
    
    storedPasswordHash = response['Item'].get('password')
    if not storedPasswordHash:
        return False 
    if bcrypt.checkpw(password.encode('utf-8'), storedPasswordHash.encode('utf-8')):
        return True 
    return False 

def storePassword(username, password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    response = table.put_item(
        Item={
            'username': username,
            'password': hashed_password.decode('utf-8')  
        }
    )
    return True


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
        #error message here instead of going back to login
        errorMessage = "User does not exist. Please register."
        return render(request, 'login.html', {'error_message': errorMessage})
    
    if not passwordExists:
        errorMessage = "Incorrect password. Please try again."
        return render(request, 'login.html', {'error_message': errorMessage})
    
    #if login is successful go to dashboard
    return redirect('dashboard')


