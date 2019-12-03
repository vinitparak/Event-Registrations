from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate,
         name='activate'),
    path('public_event/', views.public_event, name='publicevent'),
    path('private_event/', views.private_event, name='privatevent'),
    path('user/total/', views.user_total, name='user_total'),
    path('user/', views.user, name='user'),
    path('total/', views.total, name='total'),
    path('event/<slug:id>/', views.event, name='event'),
    path('delete/<slug:id>', views.delete, name='delete'),
    path('registerevent/<slug:id>', views.registerevent, name='registerevent'),
    path('registered/', views.registered, name='registered'),
    path('registered/registeredtotal/', views.registeredtotal, name='registeredtotal'),
    path('unregister/<slug:id>', views.unregister, name='unregister'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
