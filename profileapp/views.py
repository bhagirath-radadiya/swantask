from django.shortcuts import render, redirect
from loginapp.models import User, Profile, ShippingAddress


# Create your views here.

def viewProfile(request):
    if 'user_info' in request.session:
        render_dict = {}
        render_dict['status'] = 'viewProfile'

        get_profile = Profile.objects.filter(user_id=request.session['user_info']['id'])
        if len(get_profile) != 0:
            render_dict['profile'] = get_profile[0]

            render_dict['address'] = get_profile[0].addresses.all()[0]

        get_user = User.objects.get(pk=request.session['user_info']['id'])
        render_dict['user'] = get_user

        return render(request, 'profile.html', render_dict)
    else:
        return redirect('/login/')


def editProfile(request):
    if 'user_info' in request.session:
        render_dict = {}
        render_dict['status'] = 'editProfile'

        get_user = User.objects.get(pk=request.session['user_info']['id'])
        render_dict['user'] = get_user

        get_profile = Profile.objects.filter(user_id=request.session['user_info']['id'])
        if len(get_profile) != 0:
            render_dict['profile'] = get_profile[0]

            render_dict['address'] = get_profile[0].addresses.all()[0]

        return render(request, 'profile.html', render_dict)
    else:
        return redirect('/login/')


def updateProfile(request):
    if 'user_info' in request.session:
        data = {x: request.POST.get(x) for x in request.POST.keys()}
        print('updateProfile : ', data)

        get_user = User.objects.get(pk=request.session['user_info']['id'])
        get_user.firstname = data['firstname']
        get_user.lastname = data['lastname']
        get_user.save()

        get_profile = Profile.objects.filter(user_id=request.session['user_info']['id'])
        if len(get_profile) != 0:
            get_profile[0].mobile_number = data['mobile_number']
            get_profile[0].alternate_mobile_number = data['alternate_mobile_number']
            get_profile[0].save()

            get_address = get_profile[0].addresses.all()[0]
            get_address.address_line_1 = data['address_line_1']
            get_address.address_line_2 = data['address_line_2']
            get_address.city = data['city']
            get_address.state = data['state']
            get_address.zipcode = data['zipcode']
            get_address.country = data['country']
            get_address.save()

        else:
            create_shippingAddress = ShippingAddress(address_line_1=data['address_line_1'],
                                                     address_line_2=data['address_line_2'], city=data['city'],
                                                     state=data['state'], zipcode=data['zipcode'], country=data['country'])
            create_shippingAddress.save()
            create_profile = Profile(mobile_number=data['mobile_number'],
                                     alternate_mobile_number=data['alternate_mobile_number'],
                                     user_id_id=request.session['user_info']['id'])
            create_profile.save()
            create_profile.addresses.add(create_shippingAddress)

        return redirect('/viewProfile/')
    else:
        return redirect('/login/')
