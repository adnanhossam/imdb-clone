from .models import Name
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class NameCreateView(LoginRequiredMixin, CreateView):
    model = Name
    fields = ["name", "profile_picture", "profession"]
    template_name = "add_name.html"
    success_url = reverse_lazy("list_name")


class NameListView(ListView):
    model = Name
    context_object_name = "name"
    template_name = "list_name.html"
    paginate_by = 9  # Set how many names per page

    def get_queryset(self):
        queryset = Name.objects.all()

        # Filter by profession if selected
        profession = self.request.GET.get("profession")
        if profession:
            queryset = queryset.filter(profession=profession)

        # Filter by search query if provided
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                name__icontains=search_query
            )  # Case-insensitive search on 'name'

        return queryset


class NameDeleteView(LoginRequiredMixin, DeleteView):
    model = Name
    context_object_name = "name"
    template_name = "delete_name.html"
    success_url = reverse_lazy("list_name")


class NameUpdateView(LoginRequiredMixin, UpdateView):
    model = Name
    fields = ["name", "profile_picture", "profession"]
    context_object_name = "Name"
    template_name = "update_name.html"
    success_url = reverse_lazy("list_name")


class NAmeDetailView(DetailView):
    model = Name
    context_object_name = "Name"
    fields = ["name", "profile_picture", "profession"]
    template_name = "detail_name.html"
