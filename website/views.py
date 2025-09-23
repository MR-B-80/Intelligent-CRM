from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, AudioUploadForm
from .models import Customer, CallRecord
from google import genai
from google.genai import types
import json
import re

def custom_404(request, exception):
    return render(request, "404.html", status=404)
    
def home(request):
    records =  Customer.objects.all()

    #check to see if logging in
    if request.method == 'POST':
        Username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=Username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been log in !")
            return redirect("home")
        else:
            messages.success(request, "Pleas try  again...")
            return redirect("home")
    else:
        return render(request, "home.html", {'records':records})

def logout_user(request):
    logout(request)
    messages.success(request, "you have been logged out...")
    return redirect("home")

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authentication and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have successfully Registered!! ")
            return redirect("home")
    else:
        form = SignUpForm()
        return render(request, "register.html", {'form':form})
    return render(request, "register.html", {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Customer.objects.get(id=pk)
        customer_calls = CallRecord.objects.filter(customer=customer_record).order_by('-id')
        return render(request, "record.html", {
            'customer_record':customer_record,
            'customer_calls':customer_calls
        })
    else:
        messages.success("You must be logged in !")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Customer.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Customer Deleted successfully...")
        return redirect("home")
    else:
        messages.success("You must be logged in !")
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Customer Added...")
                return redirect('home')
        return render(request, "add_record.html", {'form':form})
    else:
        messages.success(request, "You Must Logged In...")
        return redirect('home')
   
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Customer.objects.get(id=pk) 
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer Has Been Updated!")
            return redirect('home')
        return render(request, "update_record.html", {'form':form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')
        
def upload_audio_file(request, pk):
    customer = Customer.objects.get(id=pk)
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():

            call_record = form.save(commit=False)
            call_record.customer = customer
            call_record.save()


            myfile = client.files.upload(file=call_record.audio_file.path)
            prompt = """
                You are an expert AI assistant for analyzing sales conversations.  
                I will provide you with an audio file of a conversation between a salesperson and a customer.  

                Your tasks are:
                1. Transcribe the full conversation into text.  
                2. Distill the following customer call transcript into a single, concise sentence (under 50 words) that captures the main outcome and next step.  
                3. Provide clear, practical suggestions for how the salesperson could improve their communication (tone, persuasion, handling objections, empathy, etc.) every item under 30 words.  

                Return the result in strict JSON format like this:
                {
                    "transcript": "...",
                    "summary": "...",
                    "suggestions": [
                        "Suggestion 1...",
                        "Suggestion 2...",
                        "Suggestion 3..."
                    ]
                }

            """
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, myfile],
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
                ),
            )

            response_json = response.text
            clean_text = re.sub(r"^```json\s*|\s*```$", "", response_json.strip(), flags=re.MULTILINE)
            data = json.loads(clean_text)
            call_record.transcript = data['transcript']
            call_record.summary = data['summary']
            res = ''
            for i, val in enumerate(data['suggestions']):
                res += f"{i+1}- {val} \n"
            call_record.suggestion = res
            call_record.save()

            messages.success(request, "File Has Been Uploaded")
            return redirect('record', pk=customer.id)
    else:
        form = AudioUploadForm()

    calls = CallRecord.objects.filter(customer=customer)
    return render(request, 'upload_audio_file.html', {'customer': customer, 'form': form, 'calls': calls})

def suggestion(request, pk):
    customer = Customer.objects.get(id=pk)
    calls = CallRecord.objects.filter(customer=customer).order_by('-id').values_list('summary', flat=True)[:10]
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    if request.method == 'GET':
        print("helo")
        suggestion_prompt = f"""
        You are acting as a professional marketing and sales advisor. I will provide you with a conversation between a user and a salesperson.
        Your tasks:  
        1. Create a **concise and accurate summary** of the conversation, highlighting the main points, the user's needs, and concerns.  
        2. Provide several **practical strategies and suggestions** for continuing the conversation with this user, including communication tips, appropriate questions, and persuasive approaches.  
        3. Divide your output clearly into two sections:  
        - Conversation Summary  
        - Strategies and Recommendations for Next Steps  

        Conversation:  {calls}  
        """
        suggestion = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[suggestion_prompt],
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            ),
        )

        return JsonResponse({'suggestion': suggestion.text})