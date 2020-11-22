from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey

rendition_sizes = [25, 150, 480, 1080, 1920]


class Navbar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.user} - navbar'


class Category(SortableMixin):
    title = models.CharField(max_length=64)
    slug = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    navbar = SortableForeignKey(Navbar, related_name='categories', on_delete=models.SET_NULL, blank=True, null=True)
    # ordering field
    category_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.__str__()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['category_order']
