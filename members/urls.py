from django.conf import settings
from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.conf.urls.static import static
urlpatterns = [
    path('signup/',views.signup_view.as_view(),name="signup"),
    path('login/',views.login_view.as_view(),name="login"),
    path('logout/',views.logout_view,name="logout"),
    path("profile/<str:key>/",views.profile_view,name="profile"),
    path("profile/<str:key>/edit/",views.profile_edit_view.as_view(),name="profile_edit"),
    path("profile/<str:key>/friends/",views.friends.as_view(),name="friends"),
]
