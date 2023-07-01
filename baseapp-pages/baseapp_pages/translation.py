import swapper
from modeltranslation.translator import TranslationOptions, register

Page = swapper.load_model("baseapp_pages", "Page")


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ("title", "body")
