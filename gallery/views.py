import json
import uuid
import datetime
from bson.errors import InvalidId
from storages.backends.gcloud import GoogleCloudStorage

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.urls import reverse
from django.views.generic.list import ListView

from .forms import PhotoUploadForm
from .models import Photo
from gallery.utils import get_bytes
from gallery.utils.watermark import add_watermark
from gallery.utils.thumbnail import get_thumbnails


def list_photo_view(request):
    photos = Photo.objects.filter(user_id=request.user.id).all_fields()
    return render(request, 'gallery/list_photo.html', {'photo_objects': photos})


def delete_photo_view(request, pk):
    try:
        Photo.objects.get(user_id=request.user.id, id=pk).delete()
    except (Photo.DoesNotExist, InvalidId):
        raise Http404
    return HttpResponseRedirect(reverse('list'))


def upload_photo_handler(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PhotoUploadForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            photo_db = Photo(title=form.cleaned_data['title'], user_id=request.user.id)
            handle_uploaded_file(request.FILES['file'], photo_db)
            return HttpResponseRedirect(reverse('list'))

        # if a GET (or any other method) we'll create a blank form
    else:
        form = PhotoUploadForm()

    return render(request, 'gallery/upload_photo.html', {'form': form})


def handle_uploaded_file(photo_file, photo_db: Photo):
    photo_uuid = uuid.uuid5(uuid.uuid4(), str(photo_db.user_id))
    photo_filenames = {}
    now = datetime.datetime.now()

    signed_photo = add_watermark(photo_file)
    for size, thumb in get_thumbnails(signed_photo, sizes=[2000, 1000, 600]):

        filename = "user_{user_id}/year_{year}/month_{month}/IMG_{uuid}_{size}.jpg".format(
            user_id=photo_db.user_id, year=now.year, month=now.month, uuid=photo_uuid, size=str(size)
        )
        with default_storage.open(filename, 'wb+') as destination:

            bytes_photo = get_bytes(thumb)
            destination.write(bytes_photo)
            photo_filenames[size] = filename

    photo_db.uuid = photo_uuid
    photo_db.filenames_json = json.dumps(photo_filenames)
    w, h = signed_photo.size
    photo_db.img_ratio = w / h
    photo_db.save()
    return photo_db
