from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Comment, Bid, Wishlist
from django import forms
from django.forms import ModelForm
from django.utils import timezone
from datetime import timedelta



class CommentForm(forms.Form):
    text = forms.CharField(min_length=5, max_length=100, required=True, widget=forms.TextInput({'placeholder' : 'Your coment text here...', 'label' : 'Add a comment', 'class' : 'form-control'}))

# Check for any expired listings
def check_for_expired():
    for listing in Listing.objects.filter(active = True):
        listing.check_expired()
        
check_for_expired()

@login_required(login_url="/login")
def index(request):
    

    check_for_expired()
    
    auctions = Listing.objects.filter(active= True).all()
    return render(request, "auctions/index.html", {
        'auctions' : auctions
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
    return HttpResponseRedirect(reverse("login"))


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
    

@login_required(login_url="/login")
# See auction data and bid for it
def see_auction(request, auction_id):
    check_for_expired()
    auction_data = Listing.objects.filter(pk=auction_id).all()
    bids_data = Bid.objects.filter(listing = auction_id)



    # Form for Bidding
    class BidForm(forms.Form):
        bid = forms.IntegerField(min_value= auction_data[0].currentPrice + 1, max_value= 99999, widget=forms.TextInput(attrs={'placeholder' : auction_data[0].currentPrice + 1}))
    # Initiate Form
    bid_form = BidForm()

        # Check wishlist
    check_wishlist = Wishlist.objects.filter(user = request.user, listing = auction_data[0]).all()
    if len(check_wishlist) > 0:
        wishlist = True
    else:
        wishlist = False


    # Load Comments
    comments = Comment.objects.filter(listing = auction_data[0]).all()
    for comment in comments:
        comment.profile_pic = User.objects.filter(pk = comment.user.pk).first().profile_picture
        if comment.profile_pic == '0':
            comment.profile_pic = None
    comment_form = CommentForm()

    # If request = post, check if form is valid
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid() and auction_data[0].active:
             # If form is valid, check if bid > currentPrice and submit it
             b = Bid(listing = auction_data[0], bid_price = form.cleaned_data['bid'], user_id = request.user)
             if b.bid_price > auction_data[0].currentPrice:
                Listing.objects.filter(pk=auction_id).update(currentPrice = b.bid_price)
                Listing.objects.filter(pk=auction_id).update(expire = timezone.now() + timedelta(hours = 24))
                b.save()
                
        else:
            return render(request , "auctions/see_auction.html", {
        'data' : auction_data[0], 'form' : bid_form, 'bids' : bids_data, 'wishlist' : wishlist, 'comments' : comments, 'comment_form' : comment_form 
    })
    # Load Bids Data and render listing template
    bids_data = Bid.objects.filter(listing = auction_id).order_by('-bid_price')[:10]



    return render(request , "auctions/see_auction.html", {
        'data' : auction_data[0], 'form' : bid_form, 'bids' : bids_data, 'wishlist' : wishlist, 'comments' : comments, 'comment_form' : comment_form 
    })

@login_required(login_url="/login")
def create_listing(request):
        
    class ListingForm(ModelForm):
        
        title = forms.CharField(
        min_length=5,  # Django enforces this server-side
        widget=forms.TextInput(attrs={'minlength': '5', 'maxlength' : 64,  'required': 'true'})
    )
        class Meta:
            model = Listing
            fields = ["title", "photo", "startingPrice", "category"]

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        print("FILES:", request.FILES) 

        if form.is_valid():
            data = form.cleaned_data
            l = Listing(title = data['title'], user_posted = request.user, photo = data['photo'], startingPrice = data['startingPrice'], category = data['category'], currentPrice = data['startingPrice'])
            l.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse(reverse("create_listing"))



    
    form = ListingForm()
    form.fields['photo'].widget.attrs = {"onchange" : "previewImage(event)"}
    for field in form.fields:
        form.fields[field].widget.attrs["placeholder"] = field.capitalize
    return render(request, "auctions/create_listing.html", { 'form' : form})

@login_required(login_url="/login")
def get_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user).all()
    return render(request, "auctions/wishlist.html", {'wishlist' : wishlist})

@login_required(login_url="/login")
def add_wishlist(request, id):
    auction_data = Listing.objects.filter(pk=id).all()
    if request.method == 'POST':
        if Wishlist.objects.filter(user = request.user, listing = auction_data[0]).count() == 0:
                wish = Wishlist(user = request.user, listing = auction_data[0])
                wish.save()
                print('added')
        else:
                Wishlist.objects.filter(user = request.user, listing = auction_data[0]).delete()
                print('removed')
    return HttpResponseRedirect(reverse("see_auction", args=[id]))


@login_required(login_url="/login")
def add_comment(request, listing_id):
    listing = Listing.objects.filter(pk = listing_id).all()[0]
    form = CommentForm(request.POST)
    if form.is_valid():
        comm = Comment(user = request.user, listing = listing, comment = form.cleaned_data['text'])
        comm.save()
    return HttpResponseRedirect(reverse("see_auction", args=[listing_id]))


@login_required(login_url="/login")
def end_listing(request, listing_id):
    listing = Listing.objects.filter(pk = listing_id).first()
    if listing.user_posted == request.user:
        Listing.objects.filter(pk=listing_id).update(active = False)
    return HttpResponseRedirect(reverse("see_auction", args=[listing_id]))
