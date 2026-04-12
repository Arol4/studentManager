from django.contrib import admin
from django.urls import path
from studentManagerApp import views
urlpatterns = [
    path('',views.login_view,name='login-page'),
    path('home-page/', views.home_page_view, name='home-page'),
    path('edit-page/',views.edit_page_view, name='edit-page'),
    path('profile-page/',views.profile_page_view, name='profile-page'),
    path('enregistrer-notes/', views.enregistrer_notes_matiere, name='enregistrer_notes'),
    path('enregistrer-notes-etudiant/', views.enregistrer_notes_etudiant, name='enregistrer_notes_etudiant'),
    path('tableau-notes/', views.tableau_notes_view, name='tableau-notes'),
    path('stats-page/', views.stats_page_view, name='stats-page'),
    path('log-out/',views.log_out_view, name='log-out'),
    path('admin/', admin.site.urls),
]
