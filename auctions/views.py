from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Comment, Bid


def index(request):
    #could need to add if condition to check if listing is active **
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "category": None
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

@login_required
def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html")
    
    #request method is POST
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["price"]
        image = request.POST["img"]
        category = request.POST["category"]
        user = request.user
        active = True
        
        #create listing
        listing = Listing(title=title, description=description, starting_bid=starting_bid, image=image, category=category, user=user, active=active)
        listing.save()        
        return HttpResponseRedirect(reverse("index"))
    
@login_required
def enlarged(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    #get comments for list
    comments = listing.comments.all()
    bids = listing.bids.all()
    if bids:
        highest = bids.order_by('-bid')[0]
        highest_bid = highest.bid
        highest_bidder = highest.user
    else:
        highest_bid = listing.starting_bid
        highest_bidder = None

    print(highest_bid)

    return render(request, "auctions/enlarged.html", {
        "listing": listing,
        "comments": comments,
        "message": None,
        "highest_bid": highest_bid,
        "highest_bidder": highest_bidder
    })


def comment(request, listing_id):
    if request.method == "POST":
        comment_words = request.POST["comm"]
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        
        #create comment
        comment = Comment(comment=comment_words, user=user, listing=listing)
        comment.save()

        return HttpResponseRedirect(reverse("enlarged", args=(listing_id,)))
    
    #request method is GET
    else:
        return HttpResponseRedirect(reverse("enlarged", args=(listing_id,)))
    
def bid(request, listing_id):
        
    if request.method == "POST":
        bid = float(request.POST["biddy"])
        listing = Listing.objects.get(pk=listing_id)
        comments = listing.comments.all()

        all_bids = listing.bids.all()
        if all_bids:
            highest_bid = all_bids.order_by('-bid')[0]
            highest_bidder = highest_bid.user

            if bid <= highest_bid.bid:
                return render(request, "auctions/enlarged.html", {
                    "listing": listing,
                    "comments": comments,
                    "message": "Bid must be greater than the current highest bid.",
                    "highest_bid": highest_bid.bid,
                    "highest_bidder": highest_bidder
                })

        highest_bid = listing.starting_bid 
        highest_bidder = None
        if bid < highest_bid:
            return render(request, "auctions/enlarged.html", {
                "listing": listing,
                "comments": comments,
                "message": "Bid must be greater than or equal to the starting price.",
                "highest_bid": highest_bid,
                "highest_bidder": highest_bidder
            })

def close(request, listing_id): 
    #add on idea: closed page filled with all closed listings
    print("OEIOEJFOJIFEOJEFOIEJOIFJOEJOEFJOEFIJOEFIJEOIFJ")
    
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("enlarged", args=(listing_id,)))


def categories(request):
    category_name = request.GET.get('category')
    if not category_name:
        category_name = "Fashion"

    listings = Listing.objects.filter(category=category_name)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "category": category_name
    })

@login_required
def watchlist(request):
    if request.method == "GET":
        user = request.user
        listings = user.watchlist.all()
        return render(request, "auctions/index.html", {
            "listings": listings,
            "category": "Watchlist"
        })
    
    #request method is POST
    user = request.user
    listing_id = request.POST["watchlister"]
    listing = Listing.objects.get(pk=listing_id)
    user.watchlist.add(listing)
    comments = listing.comments.all()
    bids = listing.bids.all()
    if bids:
        highest = bids.order_by('-bid')[0]
        highest_bid = highest.bid
        highest_bidder = highest.user
    else:
        highest_bid = listing.starting_bid
        highest_bidder = None

    return render(request, "auctions/enlarged.html", {
        "listing": listing,
        "comments": comments,
        "message": None,
        "highest_bid": highest_bid,
        "highest_bidder": highest_bidder
    })
