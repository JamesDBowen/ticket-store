"""ticketstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#pylint: disable=C0103

from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ticketstore.tickets.views import ClientViewSet, EventViewSet, CustomerViewSet, TicketViewSet

api_router = DefaultRouter(trailing_slash=False)
api_router.register(r'client', ClientViewSet)
api_router.register(r'event', EventViewSet)
api_router.register(r'customer', CustomerViewSet)
api_router.register(r'ticket', TicketViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
]
