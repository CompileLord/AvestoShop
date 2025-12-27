from django.urls import path
from .views import (
    MainListView, SearchResultsView, ShopDetailView, PostDetailView, 
    ShopDashboardView, PostCreateView, PostUpdateView, PostDeleteView, 
    ShopCreateView, CommentCreateView, LikeCreateView, AddToCartView, 
    DeleteFromCartView, CartListView, ProfileRedirectView, ConfirmSaleView
)

urlpatterns = [
    path('', MainListView.as_view(), name='main'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('shop/<int:pk>/', ShopDetailView.as_view(), name='shop_detail'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('dashboard/<int:pk>/', ShopDashboardView.as_view(), name='shop_dashboard'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('shop/new/', ShopCreateView.as_view(), name='shop_create'),
    path('post/<int:post_id>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('post/<int:post_id>/like/', LikeCreateView.as_view(), name='like_create'),
    path('post/<int:post_id>/add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/delete/<int:pk>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('shop/cart/confirm_sale/', ConfirmSaleView.as_view(), name='confirm_sale'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('profile/', ProfileRedirectView.as_view(), name='profile'),
]