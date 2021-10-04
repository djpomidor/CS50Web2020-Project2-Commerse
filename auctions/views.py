from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from auctions.models import *

from django.contrib.auth.decorators import login_required


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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

@login_required(redirect_field_name='index')
def create_listing(request):
    if request.method == "POST":
        title_ = request.POST["title"]
        description_ = request.POST["description"]
        photo = request.POST["photo"]
        bid_ = request.POST["price"]
        category = request.POST["category"]
        listing = Listing(
            user_id=request.user.id,
            title = title_,
            description = description_,
            price = bid_,
            image = photo,
            category_id=int(Category.objects.get(name=category)),
            active = True)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html", {
            "categories": Category.objects.all()
        })


def listings(request, id):
    if request.method == "POST":
        new_bid = request.POST["bid"]
        listing = Listing.objects.get(id=id)
        if int(new_bid) < listing.price:
            return render(request, "auctions/error.html", {
                "new_bid": new_bid, "price": listing.price, "message": "Your bid is to small", "listing": listing
            })
        bid = Bid(user_id=request.user.id, user_price=new_bid, listing_id=listing.id)
        bid.save()
        listing.price = new_bid
        listing.save()
        return HttpResponseRedirect(reverse("listings", args=[id]))

    else:
        user_name_bid = Bid.objects.filter(listing_id=id)
        return render(request, "auctions/listings.html", {
            "listing": Listing.objects.get(id=id),
            "bids": Bid.objects.filter(listing_id=id, user_price__gte = Listing.objects.get(id=id).price),
            "comments":Comment.objects.filter(listing_id=id),
            "n":user_name_bid.count()
        })

def comments(request, id):
    if request.method == "POST":
        comment = Comment(user_id=request.user.id, listing_id=id, text=request.POST["comment"])
        comment.save()
        return HttpResponseRedirect(reverse("listings", args=[id]))
    else:
        return HttpResponseRedirect(reverse("listings", args=[id]))

def watchlist(request):
    if "watchlist" not in request.session:
        request.session["watchlist"] = []
    listings = Listing.objects.filter(id__in=request.session["watchlist"])
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.session["watchlist"], "listings": listings
    })

def add_to_watchlist(request, id):
    if "watchlist" not in request.session:
        request.session["watchlist"] = []

    if request.method == "POST":
        if id in request.session["watchlist"]:
            return HttpResponseRedirect(reverse("listings", args=[id]))
        else:
            request.session["watchlist"] += [id]
            return HttpResponseRedirect(reverse("listings", args=[id]))
    else:
        return HttpResponseRedirect(reverse("listings", args=[id]))

def remove_from_watchlist(request,id):
    p = request.session["watchlist"]
    p.remove(id)
    request.session["watchlist"] = p
    return HttpResponseRedirect(reverse("watchlist"))

def categories(request, name):
    if name == "Uncategorised":
        listings = Listing.objects.all()
        return render(request, "auctions/categories.html", {
            "listings": listings,
            "names": Category.objects.all()
        })
    else:
        listings = Listing.objects.filter(category=Category.objects.get(name=name).id)
    return render(request, "auctions/categories.html", {
        "listings": listings,
        "names": Category.objects.all()
    })
