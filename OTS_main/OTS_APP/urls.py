from django.urls import path
from . import views
# from django.contrib.
# auth import views as auth

from django.contrib import admin  # Django admin module
from django.conf import settings   # Application settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # Static files serving
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('landingPage/', views.landingPage, name="landingPage"),
    path('upcoming_events/', views.upcoming, name="upcoming"),
    path('current_events/', views.current, name="current"),
    path('individual_event/', views.individualEvent, name="individualEvent"),
    # path('create_events/', views.createEvent, name="createEvent"),
    # path('edit_events/', views.editEvent, name="editEvent"),
    
    
] 
#  Serve media files if DEBUG is True (development mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files using staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
