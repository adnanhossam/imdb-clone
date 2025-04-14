from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css_class):
    """
    Adds a CSS class to a form field widget. If the widget already has a class,
    the new class will be appended.
    """
    existing_classes = field.field.widget.attrs.get("class", "")
    updated_classes = f"{existing_classes} {css_class}".strip()
    field.field.widget.attrs["class"] = updated_classes
    return field
