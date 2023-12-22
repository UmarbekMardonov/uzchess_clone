from modeltranslation.translator import register, TranslationOptions
from .models import News


@register(News)
class UserTranslationOptions(TranslationOptions):
    fields = ('content', 'title',)
