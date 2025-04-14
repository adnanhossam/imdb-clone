from django.urls import path
from .views import (
    NameCreateView,
    NameListView,
    NameDeleteView,
    NameUpdateView,
    NAmeDetailView,
)

urlpatterns = [
    path("add-name/", NameCreateView.as_view(), name="add_name"),
    path("list-name/", NameListView.as_view(), name="list_name"),
    path(
        "name/delete/<int:pk>/",
        NameDeleteView.as_view(),
        name="delete_name",
    ),
    path(
        "update-name/<int:pk>/",
        NameUpdateView.as_view(),
        name="update_name",
    ),
    path("detail_name/<int:pk>/", NAmeDetailView.as_view(), name="detail_name"),
]
