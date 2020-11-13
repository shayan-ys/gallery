from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

rendition_sizes = [25, 150, 480, 1080, 1920]


class Category(models.Model):
    title = models.CharField(max_length=64)
    slug = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super().save(force_insert, force_update, using, update_fields)
