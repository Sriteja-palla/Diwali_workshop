from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CrackerForm, SweetsForm, GiftsForm, CrackersForm, RegistrationForm, RecaptchaForm
from .models import Crackers, Sweets, Gifts, Cart
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        captcha_form = RecaptchaForm(request.POST)
        if form.is_valid() and captcha_form.is_valid():
            user = form.save()

            # REGISTER MAIL - Welcome Mail
            send_mail(
                'Welcome to Diwali Shop 🎆',
                f'Hi {user.username},\n\nNee account create ayyindhi! Ippudu nuvvu Diwali Shop lo order cheyochu.\n\nThank You!',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            messages.success(request, "Account created! Please login.")
            return redirect('login')
    else:
        form = RegistrationForm()
        captcha_form = RecaptchaForm()
    return render(request, 'register.html', {'form': form, 'captcha_form': captcha_form})

@login_required
def add_crakers(request):
    form = CrackerForm()
    if request.method == "POST":
        form = CrackerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, 'crack.html', {'form': form})

@login_required
def home(request):
    cat = request.GET.get('cat', 'all')
    cart_items = Cart.objects.filter(user=request.user)

    crackers = Crackers.objects.all()
    for c in crackers:
        cart = cart_items.filter(cracker=c).first()
        c.cart_qty = cart.quantity if cart else 0
        c.cart_id = cart.id if cart else 0

    sweets = Sweets.objects.all()
    for s in sweets:
        cart = cart_items.filter(sweet=s).first()
        s.cart_qty = cart.quantity if cart else 0
        s.cart_id = cart.id if cart else 0

    gifts = Gifts.objects.all()
    for g in gifts:
        cart = cart_items.filter(gift=g).first()
        g.cart_qty = cart.quantity if cart else 0
        g.cart_id = cart.id if cart else 0

    show_popup = request.session.pop('show_order_popup', False)
    context = {'cat': cat, 'data': crackers, 'sweets': sweets, 'gifts': gifts,'show_popup':show_popup}
    return render(request, 'home.html', context)

@login_required
def add_sweets(request):
    form = SweetsForm()
    if request.method == "POST":
        form = SweetsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, 'sweets.html', {'form': form})

@login_required
def add_gifts(request):
    form = GiftsForm()
    if request.method == "POST":
        form = GiftsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, 'Gifts.html', {'form': form})

@login_required
def add_craker(request):
    form = CrackersForm()
    if request.method == "POST":
        form = CrackersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, 'Crackers.html', {'form': form})

@login_required
def add_to_cart(request, item_type, item_id):
    if item_type == 'cracker':
        item = get_object_or_404(Crackers, id=item_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, cracker=item)
    elif item_type == 'sweet':
        item = get_object_or_404(Sweets, id=item_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, sweet=item)
    elif item_type == 'gift':
        item = get_object_or_404(Gifts, id=item_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, gift=item)
    else:
        return redirect("home")
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("home")

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = 0
    for item in cart_items:
        if item.cracker:
            total += item.cracker.price * item.quantity
        elif item.sweet:
            total += item.sweet.s_price * item.quantity
        elif item.gift:
            total += item.gift.gift_price * item.quantity
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, "Cart empty undhi!")
        return redirect("view_cart")

    total = 0
    order_details = ""
    for item in cart_items:
        if item.cracker:
            name = item.cracker.cracker_name
            price = item.cracker.price
        elif item.sweet:
            name = item.sweet.sweet_name
            price = item.sweet.s_price
        elif item.gift:
            name = item.gift.gift_name
            price = item.gift.gift_price
        item_total = price * item.quantity
        total += item_total
        order_details += f"- {name} x {item.quantity} = Rs. {item_total}\n"

    # ORDER MAIL - Customer ki + Neeku kuda
    message = f"Hi {request.user.username},\n\nNee Diwali Order Confirm Ayyindhi!\n\nOrder Details:\n{order_details}\nTotal Amount: Rs. {total}\n\nThank You for Shopping with us! 🎆"
    
    send_mail(
        f'Diwali Order Confirmed - Rs. {total} 🎆',
        message,
        settings.EMAIL_HOST_USER,
        [request.user.email, settings.EMAIL_HOST_USER],
        fail_silently=False,
    )

    cart_items.delete()
    # messages.success(request, "Order Placed! Details nee Email ki pampamu.")
    request.session['show_order_popup']= True
    return redirect("home")

def increase_qty(request, cart_id):
    item = get_object_or_404(Cart, id=cart_id)
    item.quantity += 1
    item.save()
    if request.GET.get('next') == 'home':
        return redirect("home")
    return redirect("view_cart")

def decrease_qty(request, cart_id):
    item = get_object_or_404(Cart, id=cart_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    if request.GET.get('next') == 'home':
        return redirect("home")
    return redirect("view_cart")

def remove_item(request, cart_id):
    item = get_object_or_404(Cart, id=cart_id)
    item.delete()
    return redirect("view_cart")

def user_logout(request):
    logout(request)
    return redirect('register')