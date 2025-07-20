from django.contrib import admin
from django.urls import path
from studentManagerApp import views
urlpatterns = [
    path('',views.login_view,name='login-page'),
    path('home-page/<str:role>/<int:id>', views.home_page_view, name='home-page'),
    path('edit-page/<str:role>/<int:id>',views.edit_page_view, name='edit-page'),
    path('enregistrer-notes/', views.enregistrer_notes, name='enregistrer_notes'),
    path('admin/', admin.site.urls),
]
