from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Album, Photo


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    exclude = ('id', 'photos_json', 'user')

    def save_model(self, request, obj: Album, form, change):
        if not change:  # create
            obj.set_id()
            obj.photos_json = []
            obj.user = request.user
            if Album.objects.get(id=obj.id):
                # unique error
                raise ValidationError('Album with same name exists')
        super().save_model(request, obj, form, change)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
