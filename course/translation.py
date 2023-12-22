from modeltranslation.translator import register, TranslationOptions
from .models import CourseBig, CourseLittle1, CourseLittle2, Mentor


@register(CourseBig)
class UserTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(CourseLittle1)
class UserTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(CourseLittle2)
class UserTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Mentor)
class UserTranslationOptions(TranslationOptions):
    fields = ('description',)

