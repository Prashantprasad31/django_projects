from django.shortcuts import render,redirect
from product.models import ProductTable,CartTable
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def index(request):
    data={}
    fetched_products=ProductTable.objects.filter(is_active=True)
    data['products']=fetched_products

    user_id=request.user.id
    id_specific_cartitems=CartTable.objects.filter(uid=user_id)
    count=id_specific_cartitems.count()
    data['cart_count']=count
    return render(request,'product/index.html',context=data)


def filter_by_category(request,category_value):
    data={}
    q1 = Q(is_active=True)
    q2 = Q(category=category_value)
    filter_products=ProductTable.objects.filter(q1 &q2)
    data['products']=filter_products
    return render(request,'product/index.html',context=data)


def sort_by_price(request,sort_value):
    data={}
    if sort_value == 'asc':
        price = 'price'
    else:
        price = "-price"    
    sorted_products=ProductTable.objects.filter(is_active=True).order_by(price)
    data['products']= sorted_products
    return render(request,'product/index.html',context=data)


def sort_by_rating(request,rating_value):
    data={}
    q1 = Q(is_active=True)
    q2 = Q(rating__gt=rating_value)
    rating_products=ProductTable.objects.filter(q1 & q2)
    data['products']= rating_products
    return render(request,'product/index.html',context=data)    
        
        
def filter_by_price_range(request):
    data = {}
    min = request.GET['min']    
    max = request.GET['max']  
    q1 = Q(price__gte=min)
    q2 = Q(price__lte=max)
    q3 = Q(is_active=True)
    filter_products = ProductTable.objects.filter(q1 & q2 & q3)   
    data['products']= filter_products
    return render(request,'product/index.html',context=data)


def product_detail(request,pid):
    product=ProductTable.objects.get(id = pid)
    return render(request,'product/product_detail.html',{'product':product})

def register_user(request):
    data={}
    if request.method=='POST':
        uname=request.POST['username']
        upass=request.POST['password']
        uconf_pass=request.POST['password2']
        if (uname==''or upass=='' or uconf_pass==''):
            data['error_msg']='Field can not be empyt'
            return render (request,'user/register.html',context=data)
        elif(upass!=uconf_pass):
            data['error_msg']='Password and confirm password does not matched'
            return render (request,'user/register.html',context=data)
        elif(User.objects.filter(username=uname).exists()):
            data['error_msg']=uname + 'Already exist'
            return render (request,'user/register.html',context=data)
        else:
            user = User.objects.create(username=uname)
            user.set_password(upass)
            user.save()
            customer = CustomerDetails.objects.create(uid=user)
            customer.save()
            return HttpResponse("Registration done")
    return render (request,'user/register.html')

def login_user(request):
    data={}
    if request.method=='POST':
        uname=request.POST['username']
        upass=request.POST['password']
        if (uname=='' or upass==''):
            data['error_msg']='Field can not be empyt'
            return render (request,'user/login.html',context=data)
        elif(not User.objects.filter(username=uname).exists()):
            data['error_msg']=uname + 'user is not register'
            return render (request,'user/login.html',context=data)
        else:
            user = authenticate(username=uname,password=upass) 
            print(user)
            if user is not None:
                login(request,user)
                return redirect('/product/index')
            else:
                data['error_msg']='Wrong Password'
                return render(request,'user/login.html',context=data)
    return render(request,'user/login.html')   
        
               
def user_logout(request):
    logout(request)
    return redirect('/product/index')    
         
def add_to_cart(request,pid):
    if request.user.is_authenticated:
        uid = request.user.id 
        print("user id = ",uid)
        print("product id = ",pid)
        user = User.objects.get(id=uid)
        product = ProductTable.objects.get(id=pid) 

        q1 = Q(uid = uid)
        q2 = Q(pid = pid)
        available_products=CartTable.objects.filter(q1 & q2)
        print()
        if(available_products.count()>0):
            messages.error(request,'Product is already added to cart.')
            return redirect('/product/index')
        else:
            cart=CartTable.objects.create(pid=product,uid=user)
            cart.save()
            messages.success(request,"Product is added to the cart.")
            return redirect('/product/index')
        # cart = CartTable.objects.create(pid=product , uid=user)
        # cart.save()
        # return redirect('/product/index/')
    else:
        return redirect("/user/login") 
    
def view_cart(request):
    data={}
    user_id=request.user.id
    user=User.objects.get(id=user_id)
    id_specific_cartitems=CartTable.objects.filter(uid=user_id)
    data['products']=id_specific_cartitems
    data['user']=user

    count=id_specific_cartitems.count
    # data['cart_count']=count
    
    total_price=0
    total_quantity=0
    for item in id_specific_cartitems:
        # total_price+=item.pid.prices
        total_price=(total_price+item.pid.price)*(item.quantity)
        total_quantity+=item.quantity
    
    data['total_price']=total_price   
    data['cart_count'] = total_quantity 
    return render(request,"product/cart.html", context=data)        

def remove_item(request,cartid):
    cart=CartTable.objects.filter(id=cartid)
    cart.delete()
    return redirect('/product/cartview')

def update_quantity(request,flag,cartid):
    cart=CartTable.objects.filter(id=cartid)
    acttual_quantity = cart[0].quantity
    if(flag=='1'):
        cart.update(quantity = acttual_quantity+1)
        pass
    else:
        if(acttual_quantity>1):
            cart.update(quantity = acttual_quantity-1)
            pass
    return redirect('/product/cartview')    

import calendar
import time
from product.models import OrderTable

def place_order(request):
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    user_id = request.user.id
    oid=str(user_id)+"-"+str(time_stamp)
    cart=CartTable.objects.filter(uid=user_id)
    for data in cart:
        order=OrderTable.objects.create(order_id=oid,quantity=data.quantity,pid=data.pid,uid=data.uid)
        order.save()

    return HttpResponse("order placed")

def place_order(request):
    data={}
    user_id=request.user.id
    user=User.objects.get(id=user_id)
    id_specific_cartitems=CartTable.objects.filter(uid=user_id)
    customer = CustomerDetails.objects.get(uid = user_id)
    data['customer'] = customer
    data['products']=id_specific_cartitems
    data['user']=user
    total_price=0
    total_quantity=0
    for item in id_specific_cartitems:
        # total_price+=item.pid.prices
        total_price=(total_price+item.pid.price)*(item.quantity)
        total_quantity+=item.quantity
    data['total_price']=total_price   
    data['cart_count'] = total_quantity 
    return render(request,"product/order.html", context=data)   

from product.models import CustomerDetails
# def edit_profile(request):
#     data={}
#     user_id=request.user.id
#     customer_queryset=CustomerDetails.objects.filter(uid=user_id)
#     customer = customer_queryset[0]
#     data['customer']=customer
#     if request.method=='POST':
#         first_name=request.POST['first_name']
#         last_name=request.POST['last_name']
#         phone=request.POST['phone']
#         email=request.POST['email']
#         address_type=request.POST['address_type']
#         full_address=request.POST['full_address']
#         pincode=request.POST['pincode']
#         customer_queryset.update(first_name=first_name,last_name=last_name,phone=phone,email=email,address_type=address_type,full_address=full_address,pincode=pincode)
#         return redirect('/product/index')
#     return render(request,"user/edit_profile.html",context=data)

from django.shortcuts import get_object_or_404

def edit_profile(request):
    data = {}
    user_id = request.user.id
    customer = get_object_or_404(CustomerDetails, uid=user_id)  # Using get_object_or_404 to handle the case where no objects are found
    data['customer'] = customer
    
    if request.method == 'POST':
        # Retrieve POST data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_type = request.POST.get('address_type')
        full_address = request.POST.get('full_address')
        pincode = request.POST.get('pincode')
        
        # Update customer details
        customer.first_name = first_name
        customer.last_name = last_name
        customer.phone = phone
        customer.email = email
        customer.address_type = address_type
        customer.full_address = full_address
        customer.pincode = pincode
        customer.save()  # Save the changes
        
        return redirect('/product/index')
    
    return render(request,"user/edit_profile.html", context=data)


# import razorpay
# def make_payment(request):
    
#     total_price=0
#     id_specific_cartitems =CartTable
#     total_price=(total_price+item.pid.price)*(item.quantity)
#     client = razorpay.Client(auth=("rzp_test_LSC273glOOj6D0","WakiVnT95NpWoJp4SFHwqjdS"))
#     data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
#     payment = client.order.create(data=data)
#     return HttpResponse("payment done") 
    

        
