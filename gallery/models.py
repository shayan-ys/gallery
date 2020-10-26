import json
import mongoengine as mongo

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.conf import settings


class Photo(mongo.Document):
    title = mongo.StringField(max_length=130, required=True)
    uuid = mongo.UUIDField(binary=False)
    filenames_json = mongo.StringField()
    user_id = mongo.IntField()

    @property
    def urls(self):
        return [(size, settings.GS_BASE_URL + filename) for size, filename in self.filenames]

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

    def delete(self, signal_kwargs=None, **write_concern):
        for _, filename in self.filenames:
            default_storage.delete(filename)
        super(Photo, self).delete(signal_kwargs, **write_concern)
