from django.shortcuts import HttpResponse, render,redirect
from .auth  import users_collection,db
import bcrypt
from pymongo import MongoClient
from django.contrib import messages
from bson import ObjectId
from datetime import datetime

def login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        global user
        user=username
        password=request.POST.get("password")
         # Find user in database
        user = users_collection.find_one({"username": username})
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            
            return redirect("home")
        else:
            return HttpResponse("Wrong Username or Password!.... Try Again😁")
    return render(request,"login.html")

def register(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        # Check if the username already exists
        if users_collection.find_one({"username": username}):
            messages.error(request, 'Username taken already!.... Try another one')
            return redirect("register")
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Store user in the database
        users_collection.insert_one({"username": username, "password": hashed_password})
        return redirect("home")
    return render(request,"register.html")
def home(request):
    return render(request,"home.html")

def add_transaction(request):
    if request.method=="POST":
        user=request.POST.get("username")
        users_collection=db[f"{user}_transactions"]
        transaction = {
            "username": user,
            "amount":float(request.POST.get("amount")),
            "category":request.POST.get("category"),
            "type": request.POST.get("type"),    
            "date": request.POST.get("date"),
        }
        users_collection.insert_one(transaction)
        return  redirect("home")
    return render(request,"add_trans.html")

def view_transaction(request):
    if request.method=="POST":
        username=request.POST.get("username")
        user_collection=db[f"{username}_transactions"]
        data=list(user_collection.find({"username":username}))
        return render(request,'view_tran.html',{'data':data})
    return render(request,"view_tran.html")

def update_transaction(request):
    if request.method=="POST":
        username=request.POST.get("username")
        user_collection=db[f"{username}_transactions"]
        data=list(user_collection.find({"username":username}))

        transactions = []
        for record in data:
            transactions.append({
                "id": str(record["_id"]),  # Convert MongoDB ObjectId to string
                "username": record["username"],
                "amount": record["amount"],
                "category": record["category"],
                "type": record["type"],
                "date": record["date"],
            })



        return render(request,'update_tran.html',{'data':transactions})
    return render(request,'update_tran.html')


def update_details(request, username, transaction_id):
    transaction_id = request.POST.get("transaction_id")
    mongo_id = ObjectId(transaction_id)

    # Access the correct user’s collection (adjust as per your logic)
    users_collection = db[f"{username}_transactions"]
    # Fetch the specific transaction using ObjectId
    transaction = users_collection.find({"_id": mongo_id})
    print()
    for i in transaction:
        print("hello")
    return HttpResponse("hello")
def set_budget(request):
    budget=request.POST.get("budget")
    username=request.POST.get("username")
    try:
        users_collection.update_one({"username":username}, {"$set": {"budget": budget}})
        print("New Budget Updated")
    except:
        print("Error occured!..  Try again.")
    return render(request,'set_budget.html')

def check_budget(request):
    if request.method=="POST":
        username=request.POST.get("username")
        budget=users_collection.find_one({ "username":username}, { "budget": 1 })
        return render(request,"check_budget.html",{'budget':budget})
    return render(request,"check_budget.html")

def financial_reports(request):
    if request.method == "POST":
        username = request.POST.get("username")
        users_collection = db[f"{username}_transactions"]
        
        # Convert cursor to list
        data = list(users_collection.find({"username": username}))
        
        total_income = 0.0
        total_expense = 0.0
        
        for record in data:
            if record["type"] == "income":
                total_income += float(record["amount"])
            elif record["type"] == "expense":
                total_expense += float(record["amount"])
        
        saving = total_income - total_expense

        return render(request, "monthly_reports.html", {
            'data': data,
            'saving': saving,
            'total_income': total_income,
            'total_expense': total_expense
        })

    return render(request, "monthly_reports.html")
