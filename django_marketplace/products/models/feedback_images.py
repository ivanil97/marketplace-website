from django.db import models


class FeedbackImages(models.Model):
    """Изображения товароа по отзыву покпателя"""
    image = models.ImageField(null=True, blank=True, upload_to="images_feedback")
    product = models.ForeignKey("FeadBack", on_delete=models.SET_NULL, related_name='images', null=True, blank=True)

    def __str__(self):
        return "FeedBackImage " + self.pk
