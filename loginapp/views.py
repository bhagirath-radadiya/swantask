from django.shortcuts import render, redirect
from .models import User, ShippingAddress, Profile
from django.contrib import messages
import re
from django.core.mail import send_mail
from django.conf import settings

pattern_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def validateEmail(email):
    if (re.search(pattern_email, email)):
        return True
    else:
        return False


def login(request):
    return render(request, 'login.html')


def insertLogin(request):
    data = {x: request.POST.get(x) for x in request.POST.keys()}
    print('insertLogin : ', data)

    get_user = User.objects.filter(username=data['username'], password=data['password'])
    print(get_user)
    if len(get_user) != 0:
        request.session['user_info'] = {'id': get_user[0].id, 'username': get_user[0].username,
                                        'password': get_user[0].password, 'firstname': get_user[0].firstname,
                                        'lastname': get_user[0].lastname}
        return redirect('/')
    else:
        messages.error(request, 'please enter correct username or password.')
        return redirect('/login/')


def registration(request):
    render_dict = {}
    if 'temp_registration' in request.session:
        render_dict = request.session['temp_registration']
        del request.session['temp_registration']
    return render(request, 'registration.html', render_dict)


def insertRegistration(request):
    data = {x: request.POST.get(x) for x in request.POST.keys()}
    print('insertRegistration : ', data)
    # insertRegistration :  {'csrfmiddlewaretoken': 'zvZJFxSWTcjt6q3CawgdKei7DvuIw45EjBSgJKMTECTDEOoj4QcfnUSgJGIngZZ4', 'firstname': 'bhagirath', 'lastname': 'radadiya', 'username': 'b.radadiya1998@gmail.com', 'password': '12345'}

    request.session['temp_registration'] = data

    if len(data['firstname']) == 0 or len(data['firstname']) > 20:
        messages.error(request, 'firstname must be 0 to 20 characters')
        return redirect(registration)

    if len(data['lastname']) == 0 or len(data['lastname']) > 20:
        messages.error(request, 'lastname must be 0 to 20 characters')
        return redirect(registration)

    if len(data['username']) == 0 or len(data['username']) > 250:
        messages.error(request, 'username must be 0 to 250 characters')
        return redirect(registration)
    else:
        if validateEmail(data['username']) == False:
            messages.error(request, 'enter valid email')
            return redirect(registration)

    if len(data['password']) < 4 or len(data['password']) > 10:
        messages.error(request, 'password must be 0 to 250 characters')
        return redirect(registration)

    if User.objects.filter(username=data['username']).exists() == False:
        create = User(username=data['username'], firstname=data['firstname'], lastname=data['lastname'],
                      password=data['password'])
        create.save()
        messages.success(request, 'your registration complited sucessfully.')
        del request.session['temp_registration']

        send_mail(
            'Registration Successfully',
            'your registration done sucessfully.\n username : ' + data['username'] + "\n password : " + data[
                'password'],
            settings.EMAIL_HOST_USER,
            ['b.radadiya1998@gmail.com', ]
        )

        return redirect('/login/')
    else:
        messages.error(request, 'username allready exist.')
        return redirect(registration)


def logout(request):
    request.session.clear()
    return redirect('/')
