from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
from PayTm import Checksum, PaytmChecksum
from django.contrib import messages
import requests
import json
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from orderapp.models import Order
from loginapp.models import Profile, User, ShippingAddress
from productapp.models import Product
from datetime import date
from django.core.mail import send_mail
from django.conf import settings

MERCHANT_KEY = '!c362cynoSpV4ER@'


# Create your views here.

def loadPayment(request):
    render_dict = []
    data = {x: request.POST.get(x) for x in request.POST.keys()}
    get_order = Order.objects.get(orderstatus='addtocart', user_id_id=request.session['user_info']['id'])

    get_order.userDetail = 'name : {} {} \nmobile number : {} {} \naddress : {}\n{}\n{}\n{}\n{}\n{}'.format(
        data['firstname'], data['lastname'], data['mobile_number'], data['alternate_mobile_number'],
        data['address_line_1'], data['address_line_2'], data['city'], data['state'], data['zipcode'], data['country'])
    get_order.save()

    outOfStock_list = []
    for key, value in get_order.product.items():
        if Product.objects.get(pk=int(key)).quantity < value['quantity']:
            outOfStock_list.append(value['name'])

    if len(outOfStock_list) == 0:
        param_dict = {
            'MID': 'nHXgex32367017368258',
            'ORDER_ID': str(get_order.id + 8000),
            'TXN_AMOUNT': str(get_order.grandTotal),
            'CUST_ID': request.session['user_info']['username'],
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})
    else:
        temp = ""
        for i in outOfStock_list:
            temp = i + ", " + temp

        messages.error(request, temp[0:-1] + ' items is out of stock. remove from cart.')
        send_mail(
            'out of stock',
            temp[0:-1] + ' items is out of stock. remove from cart.',
            settings.EMAIL_HOST_USER,
            [get_order.user_id.username, ]
        )

        return redirect('/cart/')


@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    print("++++++++++++++++++++++++++++++++++=", response_dict)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            get_order = Order.objects.get(pk=int(response_dict['ORDERID']) - 8000)
            get_order.paymentstatus = 'success'
            get_order.orderstatus = 'ordered'
            get_order.orderDate = date.today()
            get_order.save()

            for key, value in get_order.product.items():
                get_product = Product.objects.get(pk=int(key))
                get_product.quantity = get_product.quantity - value['quantity']
                get_product.save()

            get_user = User.objects.get(pk=get_order.user_id_id)
            request.session['user_info'] = {'id': get_user.id, 'username': get_user.username,
                                            'password': get_user.password, 'firstname': get_user.firstname,
                                            'lastname': get_user.lastname}
            send_mail(
                'order placed',
                'your order place sucessfully\n',
                settings.EMAIL_HOST_USER,
                [get_user.username, ]
            )
            return redirect('/')

        else:
            get_order = Order.objects.get(pk=int(response_dict['ORDERID']) - 8000)

            get_user = User.objects.get(pk=get_order.user_id_id)
            request.session['user_info'] = {'id': get_user.id, 'username': get_user.username,
                                            'password': get_user.password, 'firstname': get_user.firstname,
                                            'lastname': get_user.lastname}
            messages.error(request, 'try again.')
            send_mail(
                'order error',
                'somthing wrong.\ntry again.',
                settings.EMAIL_HOST_USER,
                [get_user.username, ]
            )

            return redirect('/checkout/')
