from typing import Optional

from django.conf import settings
from django.db import models
from django.db.models.fields.files import FieldFile
from django.utils.translation import gettext_lazy as _


HOST = settings.HOST


class BaseModel(models.Model):
    """An abstract base class model that provides self-updating
    ``created`` and ``updated_at`` fields
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

    @property
    def image_url(self) -> Optional[str]:
        file: FieldFile = getattr(self, 'image', False)
        if file:
            if file.name.startswith('https://'):
                return file.name
            return f"{HOST}{file.url}"
        return None

    @property
    def file_url(self) -> Optional[str]:
        file: FieldFile = getattr(self, 'file', False)
        if file:
            if file.name.startswith('https://'):
                return file.name
            return f"{HOST}{file.url}"
        return None

    @property
    def icon_url(self) -> Optional[str]:
        file: FieldFile = getattr(self, 'icon', False)
        if file:
            if file.name.startswith('https://'):
                return file.name
            return f"{HOST}{file.url}"
        return None

    @property
    def avatar_url(self) -> Optional[str]:
        file: FieldFile = getattr(self, 'avatar', False)
        if file:
            if file.name.startswith('https://'):
                return file.name
            return f"{HOST}{file.url}"
        return None
