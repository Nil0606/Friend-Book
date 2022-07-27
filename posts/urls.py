from django.urls import path
from . import views
from django.views.generic import RedirectView
urlpatterns = [
    path("home/",views.home,name="home"),
    path("",RedirectView.as_view(url="/home/")),
    path("posts/<int:pk>/like",views.like,name="like"),
    path("posts/add/",views.add.as_view(),name="add"),
    path("search/",views.search.as_view(),name="search")
]
