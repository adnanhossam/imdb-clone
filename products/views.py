from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from products.models import Products
from .forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


logger = logging.getLogger(__name__)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Products
    form_class = ProductForm
    template_name = "productcreate.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        product = form.save()
        product.save()  # Make sure to explicitly save the product after form validation
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form is invalid, render the form with error messages
        return self.render_to_response({"form": form})


class ProductListView(ListView):
    model = Products
    context_object_name = "products"
    template_name = "productlist.html"
    paginate_by = 9  # Set how many names per page

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        product_type = self.request.GET.get("type", "")
        products = Products.objects.all()

        if query:
            products = products.filter(
                Q(name__icontains=query) | Q(actors__name__icontains=query)
            ).distinct()

        if product_type:
            products = products.filter(type=product_type)

        return products


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Products
    context_object_name = "product"
    template_name = "productdelete.html"
    success_url = reverse_lazy("product_list")

    def get(self, request, *args, **kwargs):
        # Fetch the product object for the confirmation page
        product = self.get_object()
        return render(request, self.template_name, {"product": product})

    def post(self, request, *args, **kwargs):
        # If the user confirms, delete the product
        product = self.get_object()
        product.delete()
        return redirect(self.success_url)

    def get_object(self):
        # Get the object by ID or raise a 404 if not found
        product_id = self.kwargs.get("pk")
        return get_object_or_404(Products, pk=product_id)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Products
    form_class = ProductForm
    context_object_name = "product"
    template_name = "productupdate.html"
    success_url = reverse_lazy("product_list")

    def product_update(request, pk):
        product = get_object_or_404(Products, pk=pk)
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect("product_list")
        else:
            form = ProductForm(instance=product)
        return render(request, "product_form.html", {"form": form, "product": product})


class ProductDetailView(DetailView):
    model = Products
    form_class = ProductForm
    context_object_name = "product"
    template_name = "productdetail.html"
