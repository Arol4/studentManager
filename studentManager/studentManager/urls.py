from django.contrib import admin
from django.urls import path
from studentManagerApp import views
urlpatterns = [
    path('',views.login_view,name='login-page'),
    path('home-page/<str:role>/<int:id>',views.home_page_view, name='home-page'),
    path('admin/', admin.site.urls),
]
