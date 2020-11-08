import uuid
from datetime import datetime
import mongoengine as mongo

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.conf import settings

from .utils import get_closest

rendition_sizes = [25, 150, 480, 1080, 1920]


class TimedDocument(mongo.Document):
    created_at = mongo.DateTimeField()
    updated_at = mongo.DateTimeField()

    meta = {
        'abstract': True,
    }

    def save(self, force_insert=False, validate=True, clean=True, write_concern=None, cascade=None, cascade_kwargs=None, _refs=None, save_condition=None, signal_kwargs=None, **kwargs):
        if self.id:  # update
            self.updated_at = datetime.now()
        else:  # create
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        super().save(force_insert, validate, clean, write_concern, cascade, cascade_kwargs, _refs, save_condition, signal_kwargs)


class Album(TimedDocument):
    title = mongo.StringField(max_length=64, required=True)
    user_id = mongo.IntField()


class Photo(mongo.Document):
    title = mongo.StringField(max_length=130, required=True)
    uuid = mongo.UUIDField(binary=False)

    filename_1920 = mongo.StringField()
    filename_1080 = mongo.StringField()
    filename_480 = mongo.StringField()
    filename_150 = mongo.StringField()
    filename_25 = mongo.StringField()
    sizes = mongo.ListField()

    img_ratio = mongo.FloatField()
    user_id = mongo.IntField()
    created_at = mongo.DateTimeField()
    updated_at = mongo.DateTimeField()
    is_deleted = mongo.BooleanField(default=False)
    deleted_time = mongo.DateTimeField()

    def save(self, force_insert=False, validate=True, clean=True, write_concern=None, cascade=None, cascade_kwargs=None, _refs=None, save_condition=None, signal_kwargs=None, **kwargs):
        if self.id:  # update
            self.updated_at = datetime.now()
        else:  # create
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.uuid = uuid.uuid5(uuid.uuid4(), str(self.user_id))
        super(Photo, self).save(force_insert, validate, clean, write_concern, cascade, cascade_kwargs, _refs, save_condition, signal_kwargs)

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
