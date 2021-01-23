from django.shortcuts import render, redirect
from django.http import JsonResponse
from productapp.models import Product
from .models import Order
from django.core import serializers
from loginapp.models import Profile, ShippingAddress


# Create your views here.

def addToCart(request, foo):
    if 'user_info' in request.session:
        if foo == 'direct':
            productId = request.GET['productId']
            get_product = Product.objects.get(pk=productId)

            temp_dict = {}
            product_data = {'image': str(get_product.image), 'name': get_product.name,
                            'brand': get_product.brand, 'price': get_product.price,
                            'category': get_product.category, 'totalPrice': get_product.price,
                            'quantity': 1}
            temp_dict[get_product.id] = product_data

            check_order_availibility = Order.objects.filter(orderstatus='addtocart',
                                                            user_id_id=request.session['user_info']['id'])

            if len(check_order_availibility) == 0:
                create_order = Order(product=temp_dict, user_id_id=request.session['user_info']['id'],
                                     totalPrice=get_product.price)
                create_order.tax = create_order.totalPrice * 0.18
                create_order.grandTotal = create_order.totalPrice + create_order.tax
                create_order.save()
            else:
                get_order = check_order_availibility[0]

                product = get_order.product
                if productId not in product:
                    product[get_product.id] = product_data

                if productId in product:
                    product[productId]['quantity'] = product[productId]['quantity'] + 1
                    product[productId]['totalPrice'] = product[productId]['totalPrice'] + get_product.price
                get_order.product = product

                totalPrice = 0
                for key, value in product.items():
                    totalPrice = totalPrice + value['totalPrice']
                get_order.totalPrice = totalPrice
                get_order.tax = get_order.totalPrice * 0.18
                get_order.grandTotal = get_order.totalPrice + get_order.tax
                if get_order.discount is not None:
                    get_order.grandTotal = get_order.grandTotal-get_order.discount
                get_order.save()

            return JsonResponse({'success': get_product.name + " successfully add to cart."})

        if foo == 'indirect':
            productId = request.GET['productId']
            quantity = request.GET['quantity']
            get_product = Product.objects.get(pk=productId)

            temp_dict = {}
            product_data = {'image': str(get_product.image), 'name': get_product.name,
                            'brand': get_product.brand, 'price': get_product.price,
                            'category': get_product.category, 'totalPrice': float(get_product.price) * float(quantity),
                            'quantity': int(quantity)}
            temp_dict[get_product.id] = product_data

            check_order_availibility = Order.objects.filter(orderstatus='addtocart',
                                                            user_id_id=request.session['user_info']['id'])

            if len(check_order_availibility) == 0:
                create_order = Order(product=temp_dict, user_id_id=request.session['user_info']['id'],
                                     totalPrice=get_product.price * int(quantity))
                create_order.tax = create_order.totalPrice * 0.18
                create_order.grandTotal = create_order.totalPrice + create_order.tax
                create_order.save()
            else:
                get_order = check_order_availibility[0]

                product = get_order.product
                if productId not in product:
                    product[get_product.id] = product_data

                if productId in product:
                    product[productId]['quantity'] = int(quantity)
                    product[productId]['totalPrice'] = product[productId]['price'] * product[productId]['quantity']
                get_order.product = product

                totalPrice = 0
                for key, value in product.items():
                    totalPrice = totalPrice + value['totalPrice']
                get_order.totalPrice = totalPrice

                get_order.tax = get_order.totalPrice * 0.18
                get_order.grandTotal = get_order.totalPrice + get_order.tax
                if get_order.discount is not None:
                    get_order.grandTotal = get_order.grandTotal - get_order.discount

                get_order.save()

            return JsonResponse({'success': get_product.name + " successfully add to cart."})
    else:
        return JsonResponse({'loginRequire': "loginRequire"})


def cart(request):
    if 'user_info' in request.session:
        render_dict = {}
        validation = Order.objects.filter(user_id_id=request.session['user_info']['id'], orderstatus='addtocart')
        if len(validation) != 0:

            get_profile = Profile.objects.filter(user_id=request.session['user_info']['id'])
            if len(get_profile) != 0:
                render_dict['profile'] = get_profile[0]
                render_dict['address'] = get_profile[0].addresses.all()[0]

            if len(validation[0].product) != 0:
                render_dict['order'] = validation[0]
            else:
                get_order = validation[0]
                get_order.delete()
                render_dict['empty'] = "your cart is empty."
        else:
            render_dict['empty'] = "your cart is empty."
        return render(request, 'cart.html', render_dict)
    else:
        return redirect('/login/')


def updateCart(request):
    if 'user_info' in request.session:
        json = {}
        productId = request.GET['productId']
        quantity = request.GET['quantity']

        get_order = Order.objects.get(orderstatus='addtocart', user_id_id=request.session['user_info']['id'])
        product = get_order.product
        product[productId]['quantity'] = int(quantity)
        product[productId]['totalPrice'] = product[productId]['price'] * product[productId]['quantity']
        get_order.product = product

        totalPrice = 0
        for key, value in product.items():
            totalPrice = totalPrice + value['totalPrice']
        get_order.totalPrice = totalPrice

        get_order.tax = get_order.totalPrice * 0.18
        get_order.grandTotal = get_order.totalPrice + get_order.tax
        if get_order.discount is not None:
            get_order.grandTotal = get_order.grandTotal - get_order.discount
        get_order.save()

        json['totalPrice'] = product[productId]['totalPrice']
        json['orderPrice'] = get_order.totalPrice
        json['discount'] = get_order.discount
        json['tax'] = get_order.tax
        json['grandTotal'] = get_order.grandTotal

        return JsonResponse(json)
    else:
        return redirect('/login/')


def couponCode(request):
    if 'user_info' in request.session:
        code = {'code1': 100, 'code2': 200, 'code3': 300, '': 0}
        json = {}

        couponCode = request.GET['couponCode']
        if couponCode in code:
            get_order = Order.objects.get(orderstatus='addtocart', user_id_id=request.session['user_info']['id'])
            if get_order.code is None:
                get_order.code = couponCode
                get_order.discount = code[couponCode]
                get_order.grandTotal = get_order.grandTotal - get_order.discount
            else:
                get_order.code = couponCode
                get_order.grandTotal = get_order.grandTotal + get_order.discount
                get_order.discount = code[couponCode]
                get_order.grandTotal = get_order.grandTotal - get_order.discount
            get_order.tax = get_order.totalPrice * 0.18
            get_order.save()
            json['orderPrice'] = get_order.totalPrice
            json['discount'] = get_order.discount
            json['tax'] = get_order.tax
            json['grandTotal'] = get_order.grandTotal
        else:
            json['error'] = 'please eneter valide code.'

        return JsonResponse(json)
    else:
        return redirect('/login/')


def deleteOrder(request):
    if 'user_info' in request.session:
        productId = request.GET['productId']

        get_order = Order.objects.get(orderstatus='addtocart', user_id_id=request.session['user_info']['id'])
        del get_order.product[productId]
        get_order.product = get_order.product

        totalPrice = 0
        for key, value in get_order.product.items():
            totalPrice = totalPrice + value['totalPrice']
        get_order.totalPrice = totalPrice

        get_order.tax = get_order.totalPrice * 0.18
        get_order.grandTotal = get_order.totalPrice + get_order.tax
        if get_order.discount is not None:
            get_order.grandTotal = get_order.grandTotal - get_order.discount
        get_order.save()
        return redirect('/cart/')
    else:
        return redirect('/login/')


def checkout(request):
    if 'user_info' in request.session:
        # render_dict = []
        # data = {x: request.POST.get(x) for x in request.POST.keys()}
        # render_dict['order'] = Order.objects.get(orderstatus='addtocart', user_id_id=request.session['user_info']['id'])
        #
        # get_profile = Profile.objects.filter(user_id=request.session['user_info']['id'])
        # if len(get_profile) != 0:
        #     render_dict['profile'] = get_profile[0]
        #     render_dict['address'] = get_profile[0].addresses.all()[0]
        #
        # get_order.userDetail = 'name : {} {} \nmobile number : {} {} \naddress : {}\n{}\n{}\n{}\n{}\n{}'.format(
        #     data['firstname'], data['lastname'], data['mobile_number'], data['alternate_mobile_number'],
        #     data['address_line_1'], data['address_line_2'], data['city'], data['state'], data['zipcode'], data['country'])
        # get_order.save()

        render_dict = {}

        validation = Order.objects.filter(user_id_id=request.session['user_info']['id'], orderstatus='addtocart')
        if len(validation) != 0:

            get_profile = Profile.objects.filter(user_id=request.session['user_info']['id'])
            if len(get_profile) != 0:
                render_dict['profile'] = get_profile[0]
                render_dict['address'] = get_profile[0].addresses.all()[0]

            if len(validation[0].product) != 0:
                render_dict['order'] = validation[0]

        return render(request, 'checkout.html',render_dict)
    else:
        return redirect('/login/')
