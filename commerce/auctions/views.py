from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import datetime

from .models import User, Listing, Bid, Watchlist


class CreateListing(forms.Form):
    name = forms.CharField(label='', widget=forms.Textarea(attrs={
        "placeholder": "Name"}))
    price = forms.FloatField(label='',  widget=forms.Textarea(attrs={
        "placeholder": "price"}))
    description = forms.CharField(label='',  widget=forms.Textarea(attrs={
        "placeholder": "Description"}))
    category = forms.CharField(label='',  widget=forms.Textarea(attrs={
        "placeholder": "Category"}))
    image = forms.CharField(label='', widget=forms.Textarea(attrs={
        "placeholder": "Image url"}))


class NewBid(forms.Form):
    price = forms.FloatField(label='', widget=forms.Textarea(attrs={
        "placeholder": "Bid"}))




def index(request):
    return render(request, "auctions/index.html", {
        "lists":Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "create_form": CreateListing()
        })
    
    elif request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():
            list = Listing(
                name=form.cleaned_data['name'],
                price=form.cleaned_data['price'],
                owner=request.user,
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                date=datetime.datetime.now(),
                image=form.cleaned_data['image'],
            )
            list.save()

            return HttpResponseRedirect(reverse('index'))
        


def listings(request, list_id):
    return render(request, "auctions/listings.html", {
        "list_id": list_id,
        "list_form": Listing.objects.get(id=list_id),
        "list_bid": NewBid(),
        "bids": Bid.objects.get(id=1)
    })


@login_required
def bid(request, id):
    if request.method == 'POST':
        form = NewBid(request.POST)

        if form.is_valid():
            user_bid = form.cleaned_data['price']
            price = Listing.objects.get(id=id)
            if user_bid < price.price:
                return HttpResponseRedirect(reverse('index'))
            else:
                price.price = user_bid
                price.save()
                bid_t = Bid(user=request.user, price=user_bid)
                bid_t.save()
                bid_t.times = bid_t.times + 1
                bid_t.save()
                return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('index'))
              
    else:
        return HttpResponseRedirect(reverse('index'))


