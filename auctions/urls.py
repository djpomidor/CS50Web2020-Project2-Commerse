from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register",),
    path("create-listing", views.create_listing, name="create-listing"),
    path("accounts/login/", views.login_view),
    path("listings/<int:id>", views.listings, name="listings"),
    path("listings/<int:id>/comments", views.comments, name="comments"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_to_watchlist/<int:id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:name>", views.categories, name="categories")

]
