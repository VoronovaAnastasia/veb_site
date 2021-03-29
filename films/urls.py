from django.urls import path
from . import views

urlpatterns=[
    path("",views.get_films_list,name="get_films_list"),
    path('<int:film_id>',views.film,name="get_films_by_id"),
    path("login", views.log_in, name="login"),
    path('signup', views.sign_up, name="signup"),
    path('logout', views.log_out, name="logout")

]