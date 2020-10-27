from datetime import datetime
import json
import mongoengine as mongo

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.conf import settings


class Photo(mongo.Document):
    title = mongo.StringField(max_length=130, required=True)
    uuid = mongo.UUIDField(binary=False)
    filenames_json = mongo.StringField()
    img_ratio = mongo.FloatField()
    user_id = mongo.IntField()
    created_at = mongo.DateTimeField()
    updated_at = mongo.DateTimeField()
    is_deleted = mongo.BooleanField(default=False)
    deleted_time = mongo.DateTimeField()

    def save(self, force_insert=False, validate=True, clean=True, write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, save_condition=None, signal_kwargs=None, **kwargs):
        if self.id:  # update
            self.updated_at = datetime.now()
        else:  # create
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        super(Photo, self).save(force_insert, validate, clean, write_concern, cascade, cascade_kwargs, _refs,
                                save_condition, signal_kwargs)

    @property
    def urls(self):
        return {int(size): settings.GS_BASE_URL + filename for size, filename in self.filenames}

    @staticmethod
    def filter_size_filename(size_filename):
        if len(size_filename) > 1:
            filename = size_filename[1]
            if filename:
                if default_storage.exists(filename):
                    return True
        return False

    @property
    def filenames(self):
        size_filenames_tuple = json.loads(self.filenames_json).items()
        return filter(Photo.filter_size_filename, size_filenames_tuple)
        # return filter(lambda size_filename: default_storage.exists(size_filename[1]), size_filenames_tuple)

    def get_dimensions(self, size_point: int):
        if self.img_ratio < 1:
            # size: height
            return int(size_point * self.img_ratio), size_point
        else:
            # size: width
            return size_point, int(size_point * self.img_ratio)

    def delete(self, signal_kwargs=None, **write_concern):
        for _, filename in self.filenames:
            default_storage.delete(filename)
        super(Photo, self).delete(signal_kwargs, **write_concern)
