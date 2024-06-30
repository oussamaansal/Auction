from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newauct", views.newAuction, name="newauct"),
    path("auction/<int:auction_id>/", views.auctionDetails, name="auction_detail"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path(
        "auction/<int:auction_id>/add_to_watchlist/",
        views.add_to_watchlist,
        name="add_to_watchlist",
    ),
    path(
        "auction/<int:auction_id>/remove_from_watchlist/",
        views.remove_from_watchlist,
        name="remove_from_watchlist",
    ),
    path("categories", views.categories, name="categories"),
    path("categories/<int:catId>/", views.categoryDetails, name="catDetails"),
    path("won", views.won, name="won"),
]
