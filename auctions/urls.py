from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("see_auction/<int:auction_id>", views.see_auction, name="see_auction"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("get_wishlist", views.get_wishlist, name="wishlist"),
    path("add_wishlist/<int:id>", views.add_wishlist, name="add_wishlist"),
    path("add_coment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("end_listing/<int:listing_id>", views.end_listing, name="end_listing")
]