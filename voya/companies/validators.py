import cloudinary.api
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator:
    def __init__(self, max_size_mb: int, message=None):
        self.max_size_mb = max_size_mb
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = (_('File size must be below or equal to %(max_size_mb)s MB') % {'max_size_mb': self.max_size_mb})
        else:
            self.__message = value

    def __call__(self, value):
        if hasattr(value, 'size') and value.size > self.max_size_mb * 1024 * 1024:
            raise ValidationError(self.message)
