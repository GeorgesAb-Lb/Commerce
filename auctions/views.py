from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid

def listing(request, id):
    listingdata = Listing.objects.get(pk=id)
    isowner = request.user.username == listingdata.owner.username
    islistinginwatchlist = request.user in listingdata.watchlist.all()
    allcomments = Comment.objects.filter(listing=listingdata)
    return render(request, "auctions/listing.html", {
        "isowner": isowner,
        "listing": listingdata,
        "islistinginwatchlist": islistinginwatchlist,
        "allcomments": allcomments
    })

def closeauction(request, id):
    listingdata = Listing.objects.get(pk=id)
    isowner = request.user.username in listingdata.watchlist.all()
    islistinginwatchlist = request.user.username == listingdata.owner.username
    listingdata.isactive = False
    allcomments = Comment.objects.filter(listing=listingdata)
    listingdata.save()
    return render(request, "auctions/listing.html", {
        "isowner": isowner,
        "listing": listingdata,
        "islistinginwatchlist": islistinginwatchlist,
        "allcomments": allcomments,
        "update": True,
        "message": "Auction Closed Successfully"
    })




def addbid(request, id):
    newbid = request.POST['newbid']
    listingdata = Listing.objects.get(pk=id)
    islistinginwatchlist = request.user in listingdata.watchlist.all()
    allcomments = Comment.objects.filter(listing=listingdata)
    isowner = request.user.username == listingdata.owner.username

    if int(newbid) > listingdata.price.bid:
        updatebid = Bid(user=request.user, bid=int(newbid))
        updatebid.save()
        listingdata.price = updatebid
        listingdata.save()
        return render(request, "auctions/listing.html", {
            "listing": listingdata,
            "message": "Bid Was Placed Successfully",
            "update": True,
            "islistinginwatchlist": islistinginwatchlist,
            "allcomments": allcomments,
            "isowner": isowner
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingdata,
            "message": "Unable To Place Bid!",
            "update": False,
            "islistinginwatchlist": islistinginwatchlist,
            "allcomments": allcomments,
            "isowner": isowner
        })


def addcomment(request, id):
    currentuser = request.user
    listingdata = Listing.objects.get(pk=id)
    message = request.POST["newcomment"]

    newcomment = Comment(
        author=currentuser,
        listing=listingdata,
        message=message
    )

    newcomment.save()
    return HttpResponseRedirect(reverse("listing",args=(id, )))


def displaywatchlist(request):
    currentuser = request.user
    listings = currentuser.listingwatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def removewatchlist(request, id):
    listingdata = Listing.objects.get(pk=id)
    currentuser = request.user
    listingdata.watchlist.remove(currentuser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def addwatchlist(request, id):
    listingdata = Listing.objects.get(pk=id)
    currentuser = request.user
    listingdata.watchlist.add(currentuser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))


def index(request):
    all_categories = Category.objects.all()
    activelistings = Listing.objects.filter(isactive=True)
    return render(request, "auctions/index.html", {
        "listings": activelistings,
        "categories": all_categories
    })

def displaycategory(request):
    if request.method == "POST":
        categoryform = request.POST['category']
        category = Category.objects.get(categorytitle=categoryform)
        all_categories = Category.objects.all()
        activelistings = Listing.objects.filter(isactive=True, category=category)
        return render(request, "auctions/index.html", {
            "listings": activelistings,
            "categories": all_categories

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
        all_categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": all_categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        startingprice = request.POST["startingprice"]
        category = request.POST["category"]
        categorydata = Category.objects.get(categorytitle=category)
        currentuser = request.user
        bid = Bid(bid=int(startingprice), user=currentuser)
        bid.save()

        newListing = Listing(
            title = title,
            description = description,
            imgurl = imageurl,
            price = bid,
            category = categorydata,
            owner = currentuser
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))




