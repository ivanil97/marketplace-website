from modeltranslation.translator import TranslationOptions, register

from products.models import Product, Category, Discount, Feature, SliderBanner, StaticBanner, Tag


@register(Product)
class ProductTranslation(TranslationOptions):
    fields = "name", "description",


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = "name", "description",


@register(Discount)
class DiscountTranslation(TranslationOptions):
    fields = "description",


@register(Feature)
class FeatureTranslation(TranslationOptions):
    fields = "name",


@register(SliderBanner)
class SliderBannerTranslation(TranslationOptions):
    fields = "title", "description",


@register(StaticBanner)
class StaticBannerTranslation(TranslationOptions):
    fields = "title", "description",


@register(Tag)
class TagTranslation(TranslationOptions):
    fields = "name",
