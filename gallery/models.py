import uuid
import json
import typing
from djongo import models

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.conf import settings

from .utils import get_closest

rendition_sizes = [25, 150, 480, 1080, 1920]


class Photo(models.Model):
    title = models.CharField(max_length=130)
    uuid = models.UUIDField(blank=True, null=True)

    filename_1920 = models.CharField(max_length=240, blank=True, null=True)
    filename_1080 = models.CharField(max_length=240, blank=True, null=True)
    filename_480 = models.CharField(max_length=240, blank=True, null=True)
    filename_150 = models.CharField(max_length=240, blank=True, null=True)
    filename_25 = models.CharField(max_length=240, blank=True, null=True)
    sizes = models.JSONField()

    img_ratio = models.FloatField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_time = models.DateTimeField(blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id:  # update
            pass
        else:  # create
            self.uuid = uuid.uuid5(uuid.uuid4(), str(self.user_id))
        super(Photo, self).save(force_insert, force_update, using, update_fields)

    def set_filenames(self, filenames_size: dict):
        for size in rendition_sizes:
            try:
                setattr(self, f'filename_{size}', filenames_size[size])
                self.sizes.append(size)
            except KeyError:
                pass

    def get_url_for_size(self, size_point: int) -> str:
        return self.urls[get_closest(size_point, self.sizes)]

    @property
    def urls(self):
        return {int(size): settings.GS_BASE_URL + filename for size, filename in self.filenames}

    @property
    def filenames(self):
        size_filenames_tuple = []
        for size in self.sizes:
            if hasattr(self, f'filename_{size}'):
                filename = getattr(self, f'filename_{size}')
                if filename:
                    if default_storage.exists(filename):
                        size_filenames_tuple.append((size, filename))
        return size_filenames_tuple

    def delete(self, signal_kwargs=None, **write_concern):
        for _, filename in self.filenames:
            default_storage.delete(filename)
        super(Photo, self).delete(signal_kwargs, **write_concern)


class Album(models.Model):
    title = models.CharField(max_length=64)
    photos_json = models.JSONField(blank=True, null=True)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_photos(self):
        photo_ids = json.loads(self.photos_json)
        return Photo.objects.filter(id__in=list(photo_ids))

    def set_photos(self, photos: models.QuerySet):
        photo_ids = photos.values_list('id', flat=True)
        self.photos_json = json.dumps(photo_ids)
        self.save()

    photos = property(get_photos, set_photos)
