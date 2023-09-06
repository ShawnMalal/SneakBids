from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("create", views.create_view, name="create"), 
    path("displayBrand", views.displayBrand, name="displayBrand"), 
    path("buy/<int:id>/", views.buy, name="buy"), 
    path("bid/<int:id>/", views.bid, name="bid"),
    path("removeFromWatch/<int:id>/", views.removeFromWatch, name="removeFromWatch"),
    path("addToWatch/<int:id>/", views.addToWatch, name="addToWatch"), 
    path("displayWatchlist", views.displayWatchlist, name="displayWatchlist")
]
