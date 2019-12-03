from datetime import datetime

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db.models import Q

from .forms import *
from .tokens import account_activation_token
from .models import PublicEvent, RegisteredEvents


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "GET":
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    elif request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False

            user.save()

            site = get_current_site(request)

            subject = 'Activate your Account'

            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject, message="", html_message=message)

            return redirect('home')
        else:
            return render(request, 'register.html', {'form': form})

    return redirect('register')


def login_request(request):
    """
    This function logins in a user if the credentials are valid
    :param request:
    :return: render template if get or login and redirect if post
    """

    if request.user.is_authenticated:
        return redirect('home')

    message = None
    if request.method == 'GET':
        form = LoginForm()

    elif request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user.profile.email_confirmed is False:
                message = 'Please activate your account'
            else:
                login(request, user)
                return redirect('home')
        else:
            message = 'Invalid username or password'

    return render(request, 'login.html', {'form': form, 'message': message})


def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


@login_required()
def home(request):
    return render(request, 'home.html')


@login_required()
def total(request):
    public = list(PublicEvent.objects.filter(~Q(host=request.user)).values_list('id', flat=True))
    total = ['public_'+str(i) for i in public]
    private = list(PrivateEvent.objects.filter(~Q(host=request.user)).values_list('id', flat=True))
    total += ['private_'+str(i) for i in private]
    return JsonResponse({'count': total})


@login_required()
def event(request, id):
    etype, id = id.split('_')
    id = int(id)
    if 'public' in etype:
        eventData = PublicEvent.objects.get(id=id)
        time = datetime.strftime(eventData.date, "%a, %d %b %Y")
        data = {
            'description': eventData.description,
            'title': eventData.title,
            'no_of_attendees': eventData.no_of_attendees,
            'time': time,
        }

        if eventData.image.name != 'default.jpg' and eventData.image.name != '':
            data['image'] = eventData.image.name
        print(data)

    if 'private' in etype:
        eventData = PrivateEvent.objects.get(id=id)
        time = datetime.strftime(eventData.date, "%a, %d %b %Y")
        data = {
            'description': eventData.description,
            'title': eventData.title,
            'time': time
        }
        print(eventData.image)
        if eventData.image.name != 'default.jpg' and eventData.image.name != '':
            data['image'] = eventData.image.name
        print(data)

    return JsonResponse(data)


@login_required()
def public_event(request):
    if request.method == 'GET':
        form = AddPublicEventForm()

    elif request.method == 'POST':
        form = AddPublicEventForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.host = request.user
            post.save()
            return redirect('home')
        form = AddPublicEventForm()
    return render(request, 'addpublicevent.html', {'form': form})

@login_required()
def private_event(request):
    if request.method == 'GET':
        form = AddPrivateEventForm()

    elif request.method == 'POST':
        form = AddPrivateEventForm(request.POST, request.FILES)
        print([(field.label, field.errors) for field in form])
        if form.is_valid():
            form = form.cleaned_data
            event = PrivateEvent(host=request.user, title=form['title'], description = form['description'], date = form['date'], image=form['image'])
            event.save()
            
            users = [i.strip() for i in form['invitees'].split(',')]

            for user in users:
                event.invitees.add(User.objects.get(username=user))

            event.save()

            return redirect('home')
        form = AddPrivateEventForm()
    return render(request, 'addprivateevent.html', {'form': form})


@login_required()
def user_total(request):
    public = list(PublicEvent.objects.filter(host=request.user).values_list('id', flat=True))
    total = ['public_'+str(i) for i in public]
    user = User.objects.get(username=request.user)
    private = list(PrivateEvent.objects.filter(invitees__in=[user]).values_list('id', flat=True))
    total += ['private_'+str(i) for i in private]
    return JsonResponse({'count': total})


@login_required()
def user(request):
    return render(request, 'user.html')


@login_required()
def delete(request, id):
    etype, id = id.split('_')
    id = int(id)
    if 'public' in etype:
        post = PublicEvent.objects.get(id=id)
        author = post.host
        # print(request.user == author)
        if request.user != author:
            return JsonResponse({})
        post.delete()
        return JsonResponse({'success': True})

    if 'private' in etype:
        post = PrivateEvent.objects.get(id=id)
        author = post.host
        if request.user != author:
            return JsonResponse({})
        post.delete()
        return JsonResponse({'success': True})

    return JsonResponse({})


@login_required()
def registerevent(request, id):
    user = request.user
    exists = RegisteredEvents.objects.filter(user = user, event = id)
    if(len(exists) == 0):
        etype, eid = id.split('_')
        eid = int(eid)
        eventData = getEventData(etype, eid)
        registered = RegisteredEvents.objects.filter(user=user)
        # print(registered)
        for i in registered:
            eetype, eeid = i.event.split('_')
            eeid = int(eeid)
            eData = getEventData(eetype, eeid)
            if eventData.date.date() == eData.date.date():
                return JsonResponse({'result': 'You cannot register as it clashes with another event'})
        re = RegisteredEvents(user = user, event = id)
        re.save()
        result = 'You have been registered'
    else:
        result = 'You have already registered to the event'

    return JsonResponse({'result': result})

def getEventData(etype, id):
    if 'public' in etype:
        eventData = PublicEvent.objects.get(id=id)
    else:
        eventData = PrivateEvent.objects.get(id=id)
    return eventData


def registered(request):
    return render(request, 'registered.html')


def registeredtotal(request):
    count = RegisteredEvents.objects.filter(user=request.user).values_list('event', flat=True)
    return JsonResponse({'count': list(count)})


def unregister(request, id):
    eventData = RegisteredEvents.objects.get(user = request.user, event = id)
    eventData.delete()
    return JsonResponse({'success': 'Successfully unregistered'})


def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and user.profile.email_confirmed is True:
        return redirect('home')

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return redirect('login')