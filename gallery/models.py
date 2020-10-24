import os
import datetime
import posixpath
from PIL import Image
from io import StringIO
import mongoengine as mongo

from django.core.files import File
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver


# def user_directory_path(instance: 'Media', filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     user_filename = 'user_{0}/{1}_{2}'.format(instance.created_by_id, instance.id, filename)
#     date_dirname = datetime.datetime.now().strftime('uploads/%Y/%m/')
#     return posixpath.join(date_dirname, user_filename)


class Photo(mongo.Document):
    title = mongo.StringField(max_length=130, required=True)
    url_source = mongo.URLField()


# class Media(models.Model):
#     class Meta:
#         abstract = True
#
#     title = models.CharField(max_length=130)
#     caption = models.TextField(max_length=2070, blank=True)
#
#     file = models.FileField(upload_to=user_directory_path)
#     instagram_url = models.URLField(blank=True)
#
#     width = models.IntegerField(null=True, blank=True)
#     height = models.IntegerField(null=True, blank=True)
#
#     created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


# class Photo(Media):
    # original 1366
    # mobile 640
    # Instagram 125
    # mobile placeholder 37
    # photo_640 = models.ImageField(upload_to=user_directory_path)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     if not self.id:
    #         # new Photo
    #         pass
    #     super(Photo, self).save(force_insert, force_update, using, update_fields)


# class Video(Media):
#     pass


# @receiver(post_delete, sender=Photo)
# def photo_cleanup(sender, instance: Photo, **kwargs):
#     if instance.file_local:
#         if os.path.isfile(instance.file_local.path):
#             os.remove(instance.file_local.path)
#     if instance.file_cloud:
#         instance.file_cloud.delete()
