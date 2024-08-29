from django.db import models


class User(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=150)
    agreement_accepted = models.BooleanField(default=False)
