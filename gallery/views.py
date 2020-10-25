import json
import uuid
import datetime
from storages.backends.gcloud import GoogleCloudStorage

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings

from .forms import PhotoUploadForm
from .models import Photo
from gallery.utils import get_bytes
from gallery.utils.watermark import add_watermark
from gallery.utils.thumbnail import get_thumbnails


def upload_photo_handler(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PhotoUploadForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            photo_db = Photo(title=form.cleaned_data['title'])
            photo_db = handle_uploaded_file(request.FILES['file'], photo_db, request.user)
            urls_html = ''
            for size_url in json.loads(photo_db.urls_json).items():
                urls_html += "%s: %s<br/>" % size_url
            html = "<html><body>uploaded. <br/>%s</body></html>" % urls_html
            return HttpResponse(html)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = PhotoUploadForm()

    return render(request, 'gallery/upload_photo.html', {'form': form})


def handle_uploaded_file(f, photo_db, user):
    gcloud_storage = GoogleCloudStorage()
    photo_uuid = uuid.uuid5(uuid.uuid4(), str(user.id))
    photo_urls = {}
    now = datetime.datetime.now()

    signed_photo = add_watermark(f)
    for size, thumb in get_thumbnails(signed_photo, sizes=[2000, 1000, 600]):

        filename = "user_{user_id}/year_{year}/month_{month}/IMG_{uuid}_{size}.jpg".format(
            user_id=user.id, year=now.year, month=now.month, uuid=photo_uuid, size=str(size)
        )
        with gcloud_storage.open(filename, 'wb+') as destination:

            bytes_photo = get_bytes(thumb)
            destination.write(bytes_photo)
            photo_urls[size] = settings.GS_BASE_URL + filename

    photo_db.uuid = photo_uuid
    photo_db.urls_json = json.dumps(photo_urls)
    photo_db.save()
    return photo_db
