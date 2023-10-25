from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("displaycategory", views.displaycategory, name="displaycategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("removewatchlist/<int:id>", views.removewatchlist, name="removewatchlist"),
    path("addwatchlist/<int:id>", views.addwatchlist, name="addwatchlist"),
    path("watchlist", views.displaywatchlist, name="displaywatchlist"),
    path("addcomment/<int:id>", views.addcomment, name="addcomment"),
    path("addbid/<int:id>", views.addbid, name="addbid"),
    path("closeauction/<int:id>", views.closeauction, name="closeauction")
]
