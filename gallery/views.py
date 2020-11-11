import datetime
from bson.errors import InvalidId

from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.views.generic.list import ListView
from django.urls import reverse

from .forms import PhotoUploadForm
from .models import Photo, Album
from .utils import get_bytes
from .utils.watermark import add_watermark
from .utils.thumbnail import get_thumbnails


class AlbumListView(ListView):
    model = Album

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).all()


def list_photo_view(request, user_id: int, album_slug: str):
    # photos = filter(user_id=request.user.id)
    photos = Photo.objects.all()
    return render(request, 'gallery/list_photo.html', {'photo_objects': photos})


def delete_photo_view(request, pk):
    try:
        # Photo.objects.get(user_id=request.user.id, id=pk).delete()
        pass
    except (Photo.DoesNotExist, InvalidId):
        raise Http404
    return JsonResponse({'deleted': 1})


def upload_photo_handler(request, album_id: str):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PhotoUploadForm(request.POST, request.FILES)

        album = Album.objects.get(id=album_id)
        # check whether it's valid:
        if form.is_valid():
            photo_db = Photo(title=form.cleaned_data['title'], user_id=request.user.id)
            handle_uploaded_file(request.FILES['file'], photo_db)
            album.add_photo(photo_db)
            return HttpResponseRedirect(reverse('list'))

        # if a GET (or any other method) we'll create a blank form
    else:
        form = PhotoUploadForm()

    return render(request, 'gallery/upload_photo.html', {'form': form, 'album_id': album_id})


def handle_uploaded_file(photo_file, photo_db: Photo):
    photo_filenames = {}
    now = datetime.datetime.now()

    signed_photo = add_watermark(photo_file)
    for size, thumb in get_thumbnails(signed_photo):

        filename = "user_{user_id}/year_{year}/month_{month}/IMG_{uuid}_{size}.jpg".format(
            user_id=photo_db.user_id, year=now.year, month=now.month, uuid=photo_db.uuid, size=str(size)
        )
        with default_storage.open(filename, 'wb+') as destination:

            bytes_photo = get_bytes(thumb)
            destination.write(bytes_photo)
            photo_filenames[size] = filename

    photo_db.set_filenames(photo_filenames)
    w, h = signed_photo.size
    photo_db.img_ratio = w / h
    photo_db.save()
    return photo_db
