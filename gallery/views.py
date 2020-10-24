from storages.backends.gcloud import GoogleCloudStorage

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import PhotoUploadForm
from gallery.utils.watermark import add_watermark


def upload_photo_handler(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PhotoUploadForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            html = "<html><body>uploaded</body></html>"
            return HttpResponse(html)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = PhotoUploadForm()

    return render(request, 'gallery/upload_photo.html', {'form': form})


def handle_uploaded_file(f):
    gcloud_storage = GoogleCloudStorage()
    with gcloud_storage.open('test.jpg', 'wb+') as destination:
        photo = add_watermark(f)
        destination.write(photo)
