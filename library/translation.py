from modeltranslation.translator import register, TranslationOptions
from .models import Book


@register(Book)
class UserTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)
