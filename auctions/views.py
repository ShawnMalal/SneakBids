from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Category, Listings
from .models import User


def index(request):
    activeListings = Listings.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", { 
        "listings": activeListings,
        "categories": allCategories
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


def create_view(request): 

    if request.method =="GET": 
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else: 
        # Get respective information
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        price = request.POST["price"]
        imageURL = request.POST["link"]
        # Get username
        currentUser = request.user

        categoryData = Category.objects.get(categoryName=category)
        # new listing object
        newListing = Listings( 
            itemName=title, 
            description=description,
            category=categoryData,
            price=float(price),
            imageUrl=imageURL,
            owner=currentUser
        )
        # save the new listing
        newListing.save()

        return HttpResponseRedirect(reverse(index))


def displayBrand(request): 
    if request.method == "POST": 
        categoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryFromForm)
        activeListings = Listings.objects.filter(isActive=True, category=category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html", { 
            "listings": activeListings,
            "categories": allCategories
        })

def buy(request, id): 
    listingData = Listings.objects.get(pk=id)
    isListingInWatch = request.user in listingData.watchlist.all()
    return render(request, "auctions/buy.html", { 
        "listing": listingData,
        "isListingInWatch": isListingInWatch
    })


def bid(request, id): 
    return render(request, "auctions/bid.html")


def removeFromWatch(request, id):
    listingData = Listings.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("buy",args=(id, )))


def addToWatch(request, id): 
    listingData = Listings.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("buy",args=(id, )))

def displayWatchlist(request): 
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return render (request, "auctions/displayWatchlist.html", { 
        "listings": listings
    })


        
