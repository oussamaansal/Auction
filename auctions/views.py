from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import *
from django.urls import reverse
from django.db.models import Max
from .forms import *
from django.contrib import messages


from .models import *


def index(request):
    auctions = Auction.objects.annotate(highest_bid=Max("bid__amount"))
    return render(request, "auctions/index.html", {"auctions": auctions})
def won(request):
    auctions = Auction.objects.filter(winner=request.user)
    return render(request, "auctions/won.html", {"auctions": auctions})

def categories(request):
    categs = Category.objects.all()

    return render(request, "auctions/categories.html", {"categs": categs})
def categoryDetails(request,catId):
    category =  get_object_or_404(Category, pk=catId)
    auctions = Auction.objects.filter(categ=category)

    return render(request, "auctions/categDetails.html", {"auctions": auctions,"category":category})

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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        fullN = request.POST["full_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, full_name=fullN)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def newAuction(request):
    if request.method == "POST":
        form = NewAucForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.creator = request.user
            auction.save()
            messages.success(request, 'Auction created successfully!')
            return redirect("index")
        else:
            # Check each field for errors and display messages
            if 'title' in form.errors:
                messages.error(request, 'Please enter a title for the auction.')
            if 'start_bid' in form.errors:
                messages.error(request, 'Please enter a starting bid for the auction.')
            if 'desc' in form.errors:
                messages.error(request, 'Please enter a description for the auction.')
            if 'categ' in form.errors:
                messages.error(request, 'Please select a category for the auction.')
    else:
        form = NewAucForm()
    
    categories = Category.objects.all()    
    templateName = "auctions/newauction.html"
    context = {"form": form, "categories": categories}
    return render(request, templateName, context)


def auctionDetails(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    comments = Comment.objects.filter(auction=auction)
    bids = Bid.objects.filter(auction=auction).order_by('-amount')
    high_bid = bids.first()

    is_winner = request.user == auction.winner  # Check if the user is the winner
    is_creator = request.user == auction.creator  # Check if the user is the creator

    # Handle comment form
    if request.method == 'POST' and 'comment' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.auction = auction
            comment.save()
            return redirect('auction_detail', auction_id=auction.id)
    else:
        comment_form = CommentForm()
        
    message1 = ''
    # Handle bid form
    if request.method == 'POST' and 'bid' in request.POST:
        bid_form = BidForm(request.POST)
        
        
        if bid_form.is_valid():
            new_bid = bid_form.cleaned_data['amount']
            if high_bid is None :
                if new_bid < auction.start_bid+10:
                  message1 = 'Bid amount must be higher than the current highest bid by atleast (10 $).'
                else :
                      bid = Bid(user=request.user, auction=auction, amount=new_bid)
                      bid.save()
                      return redirect('auction_detail', auction_id=auction.id) 
            elif new_bid >= high_bid.amount+10 or new_bid >= auction.start_bid+10:    
                bid = Bid(user=request.user, auction=auction, amount=new_bid)
                bid.save()
                return redirect('auction_detail', auction_id=auction.id)
            else:
                message1 = 'Bid amount must be higher than the current highest bid by atleast (10 $).'
    else:
        bid_form = BidForm()

    # Handle close auction form
    if request.method == 'POST' and 'close_auction' in request.POST:
        close_auction_form = CloseAuctionForm(request.POST)
        if close_auction_form.is_valid():
            auction.is_active = False
            auction.winner = high_bid.user if high_bid else None
            auction.save()
            return redirect('auction_detail', auction_id=auction.id)
    else:
        close_auction_form = CloseAuctionForm()
    is_watched = Watchlist.objects.filter(user=request.user, auction=auction).exists() if request.user.is_authenticated else False

    context = {
        'auction': auction,
        'comment_form': comment_form,
        'bid_form': bid_form,
        'close_auction_form': close_auction_form,
        'comments': comments,
        'bids': bids,
        'high_bid': high_bid,
        'is_winner': is_winner,
        'is_creator': is_creator,
        'is_watched': is_watched ,
        'message1':message1}

    return render(request, 'auctions/auction_detail.html', context)

@login_required
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    context = {
        'watchlist_items': watchlist_items
    }
    return render(request, 'auctions/watchlist.html', context)

@login_required
def add_to_watchlist(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    Watchlist.objects.get_or_create(user=request.user, auction=auction)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_from_watchlist(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    Watchlist.objects.filter(user=request.user, auction=auction).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

