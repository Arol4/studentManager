from django.contrib import admin
from django.urls import path
from studentManagerApp import views
urlpatterns = [
    path('',views.login_view),
    path('admin/', admin.site.urls),
]
