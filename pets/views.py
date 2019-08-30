from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from .models import Pet
from .forms import PetForm, PetUpdateForm ,SignupForm, SigninForm 



def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("pets-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('pets-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect("signin")



def pets_list(request):
    context = {
        'pets' : Pet.objects.filter(available=True),
    }
    return render(request,'pets_list.html', context)

def pet_detail(request, pet_id):
    pet = Pet.objects.get(id= pet_id)
    context = {
        'pet' : pet,
    }
    return render(request,'pet_detail.html', context)


def create_pet(request):
    if request.user.is_anonymous:
        return redirect('signin')
    form = PetForm()
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pets-list')
    context = {
        "form":form,
    }
    return render(request, 'create_pet.html', context)

def update_pet(request, pet_id):
    if request.user.is_anonymous:
        return redirect('signin')
    pet_obj = Pet.objects.get(id= pet_id)
    form = PetUpdateForm(instance= pet_obj)
    if request.method == "POST":
        form = PetUpdateForm(request.POST, request.FILES, instance=pet_obj)
        if form.is_valid():
            form.save()
            return redirect('pet-detail' , pet_id)
    context = {
        "form":form,
        'pet_obj': pet_obj,
    }
    return render(request, 'pet_update.html', context)

def delete_pet(request, pet_id):
    if request.user.is_authenticated:
        pet = Pet.objects.get(id= pet_id)
        pet.delete()
        return redirect('pets-list')
    return redirect('signin')

