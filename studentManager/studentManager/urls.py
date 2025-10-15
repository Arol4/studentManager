from django.contrib import admin
from django.urls import path
from studentManagerApp import views
urlpatterns = [
    path('',views.login_view,name='login-page'),
    path('home-page/<str:role>/<int:id>', views.home_page_view, name='home-page'),
    path('edit-page/<str:role>/<int:id>',views.edit_page_view, name='edit-page'),
    path('profile-page/<str:role>/<int:id>',views.profile_page_view, name='profile-page'),
    path('enregistrer-notes/', views.enregistrer_notes, name='enregistrer_notes'),
    path('tableau-notes/<str:role>/<int:id>', views.tableau_notes_view, name='tableau-notes'),
    path('log-out',views.log_out_view, name='log-out'),
    path('admin/', admin.site.urls),
]
