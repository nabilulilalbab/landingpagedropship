from django.urls import path
from . import views
app_name = 'landingpage'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('order/<slug:slug>/', views.create_order, name='create_order'),
    path('kategori/<int:category_id>/', views.Product_by_filter, name='product_by_filter'),
]