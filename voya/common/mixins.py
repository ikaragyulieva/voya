from django import forms


class PlaceholderMixin:
    """
    Mixin to add placeholder to form fields.
    """
    def add_placeholders(self):
        for field_name, field in self.fields.items():  # ('first_name': field_obj)
            placeholder = field.label or field_name.replace('_', ' ').capitalize()
            field.widget.attrs['placeholder'] = placeholder

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholders()


class StyledFormMixin:
    """
    Mixin to add custom styling to form fields, placing labels above fields
    and applying consistent CSS classes.
    """
    form_field_class = 'form-control'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing_classes} {self.form_field_class}".strip()
