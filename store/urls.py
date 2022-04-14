from django.urls import path
from . import views
from .views import SearchResultsView

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.update_item, name="update_item"),
    path('order_process/', views.orderProcess, name="order_process"),
    path('register/', views.register_user, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('search', SearchResultsView.as_view(), name='search_results'),
]
