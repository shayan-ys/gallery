from storages.backends.gcloud import GoogleCloudStorage
from django.db import models


class Media(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=130)
    caption = models.TextField(max_length=2070, blank=True)

    file_local = models.FileField(upload_to='uploads/%Y/%m/')
    file_cloud = models.FileField(upload_to='uploads/%Y/%m/', storage=GoogleCloudStorage)
    instagram_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Image(Media):
    pass


class Video(Media):
    pass
