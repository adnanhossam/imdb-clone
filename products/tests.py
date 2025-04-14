from django.test import Client, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from cast.models import Name
from .models import Products


class TestProductModel(TestCase):
    def setUp(self):
        self.writer = Name.objects.create(name="tamer ashour", profession="Writer")
        self.director = Name.objects.create(
            name="youssef shahin", profession="Director"
        )
        self.actor = Name.objects.create(name="lebleba", profession="Actor")
        self.product = Products.objects.create(
            name="almala7a",
            director=self.director,
            year_of_production="2010",
            length=160,
            imdb_rating=8,
            your_rating=7,
            type="movie",
        )
        self.product.writer.set([self.writer])
        self.product.actors.set([self.actor])

    def test_product_is_valid(self):
        name = Products.objects.get(name="almala7a")
        self.assertTrue(name)


class TestProductViews(TestCase):
    def setUp(self):
        self.writer = Name.objects.create(name="tamer ashour", profession="Writer")
        self.director = Name.objects.create(
            name="youssef shahin", profession="Director"
        )
        self.actor = Name.objects.create(name="lebleba", profession="Actor")
        mock_image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01",  # Minimal PNG header bytes
            content_type="image/jpeg",
        )
        self.product = Products.objects.create(
            name="almala7a",
            director=self.director,
            year_of_production="2010",
            length=160,
            imdb_rating=8,
            your_rating=7,
            type="movie",
            thumbnail=mock_image,
        )
        self.product.writer.set([self.writer])
        self.product.actors.set([self.actor])
        self.client = Client()

    def test_list_products(self):
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "productlist.html")
        self.assertEqual(len(response.context.get("products")), 1)


class ProductCreateViewTest(TestCase):
    def setUp(self):
        self.create_url = reverse(
            "add_product"
        )  # Replace 'add_product' with your actual URL name for the view.

    def test_get_create_view(self):
        """Test if the ProductCreateView renders correctly."""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "products/product_form.html"
        )  # Replace with the actual template name.

    def test_post_create_valid_product(self):
        """Test creating a product with valid data."""
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01",
            content_type="image/jpeg",
        )

        data = {
            "name": "Test Product",
            "type": "Movie",
            "imdb_rating": 8.5,
            "year_of_production": 2023,
            "length": 120,
            "thumbnail": image,
        }

        response = self.client.post(self.create_url, data)

        # Check that the response redirects after successful creation
        self.assertEqual(response.status_code, 302)

        # Check that the product was created
        self.assertEqual(Products.objects.count(), 1)
        product = Products.objects.first()
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.type, "Movie")
        self.assertEqual(product.imdb_rating, 8.5)

    def test_post_create_invalid_product(self):
        """Test creating a product with invalid data."""
        data = {
            "name": "",  # Invalid: Name is required
            "type": "InvalidType",  # Assuming you validate the type choices
            "imdb_rating": "invalid",  # Invalid: Must be a float
        }

        response = self.client.post(self.create_url, data)

        # Check that the response does not redirect (form errors)
        self.assertEqual(response.status_code, 200)

        # Ensure the form returned errors
        self.assertContains(response, "This field is required", html=True)
        self.assertContains(response, "Select a valid choice", html=True)

        # Check that no product was created
        self.assertEqual(Products.objects.count(), 0)
