from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, AudioUploadForm
from .models import Customer, CallRecord
from google import genai
from google.genai import types

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
        #Look Up Records
        customer_record = Customer.objects.get(id=pk)
        return render(request, "record.html", {'customer_record':customer_record})
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
    client = genai.Client(api_key="GEMINI_API_KEY")

    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():

            call_record = form.save(commit=False)
            call_record.customer = customer
            call_record.save()


            myfile = client.files.upload(file=call_record.audio_file.path)
            prompt = 'Generate a transcript of the speech.'
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, myfile],
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
                ),
            )
            call_record.transcript = response.text
            call_record.save()

            summary_prompt = f"""
                Distill the following customer call transcript into a single, concise sentence (under 25 words) that captures the main outcome and next step.
                Transcript:
                ---
                {response.text}
                ---
            """
            summary = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[summary_prompt],
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
                ),
            )
            call_record.summary = summary.text
            call_record.save()

            messages.success(request, "File Has Been Uploaded")
            return redirect('record', pk=customer.id)
    else:
        form = AudioUploadForm()

    calls = CallRecord.objects.filter(customer=customer)
    return render(request, 'upload_audio_file.html', {'customer': customer, 'form': form, 'calls': calls})