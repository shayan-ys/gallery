import datetime
import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.views.generic.list import ListView
from django.urls import reverse

from .forms import PhotoUploadForm
from .models import Category, Navbar
from .utils import get_bytes
from .utils.watermark import add_watermark
from .utils.thumbnail import get_thumbnails
from .mongo import MONGO


class CategoryListView(ListView):
    model = Category

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).all()


def list_photo_view(request, user_id: int, category_slug: str):
    navbar = Navbar.objects.get(user_id=user_id)
    category = Category.objects.get(slug=category_slug)
    photos = get_photo_document(user_id, category.id).find()
    return render(request, 'gallery/list_photo.html', {'photo_objects': photos, 'category': category, 'navbar': navbar})


def delete_photo(document, photo: dict):
    # delete images
    for _, filename in photo['filenames'].items():
        default_storage.delete(filename)
    # delete DB record
    document.delete_one({"_id": photo['_id']})


def delete_photo_view(request, category_id, photo_uuid):
    category = Category.objects.get(id=category_id)
    user_id = request.user.id
    document = get_photo_document(user_id, category_id)
    photo = document.find_one({"uuid": photo_uuid})

    delete_photo(document, photo)
    return HttpResponseRedirect(reverse('list', kwargs={'user_id': user_id, 'category_slug': category.slug}))


def get_photo_document(user_id: int, category_id: int):
    return MONGO.photos[f'user_{user_id}'][f'category_{category_id}']


def upload_photo_handler(request, category_id: int):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PhotoUploadForm(request.POST, request.FILES)

        # check whether it's valid:
        if form.is_valid():
            category = Category.objects.get(id=category_id)
            user_id = request.user.id
            photo_db = {
                'title': form.cleaned_data['title'],
                'uuid': str(uuid.uuid1()),
                'user_id': user_id,
            }
            photo_db = handle_uploaded_file(request.FILES['file'], photo_db)
            document = get_photo_document(user_id, category_id)
            photo_id = document.insert_one(photo_db).inserted_id

            return HttpResponseRedirect(reverse('list', kwargs={'user_id': user_id, 'category_slug': category.slug}))

        # if a GET (or any other method) we'll create a blank form
    else:
        form = PhotoUploadForm()

    return render(request, 'gallery/upload_photo.html', {'form': form, 'category_id': category_id})


def handle_uploaded_file(photo_file, photo_db: dict):
    photo_filenames = {}
    now = datetime.datetime.now()

    signed_photo = add_watermark(photo_file)
    for size, thumb in get_thumbnails(signed_photo):

        filename = "user_{user_id}/year_{year}/month_{month}/IMG_{uuid}_{size}.jpg".format(
            user_id=photo_db['user_id'], year=now.year, month=now.month, uuid=photo_db['uuid'], size=str(size)
        )
        with default_storage.open(filename, 'wb+') as destination:

            bytes_photo = get_bytes(thumb)
            destination.write(bytes_photo)
            photo_filenames[f'{size}px'] = filename

    photo_db['filenames'] = photo_filenames
    w, h = signed_photo.size
    photo_db['img_ratio'] = w / h
    return photo_db
