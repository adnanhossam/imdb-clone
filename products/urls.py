from products.views import (
    ProductDeleteView,
    ProductCreateView,
    ProductListView,
    ProductUpdateView,
    ProductDetailView,
)
from django.urls import path


urlpatterns = [
    path("products", ProductListView.as_view(), name="product_list"),
    path("products/add/", ProductCreateView.as_view(), name="add_product"),
    path(
        "products/<int:pk>/detail/", ProductDetailView.as_view(), name="detail_product"
    ),
    path(
        "products/<int:pk>/update/", ProductUpdateView.as_view(), name="update_product"
    ),
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="delete_product"
    ),
]
