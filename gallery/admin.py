from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    readonly_fields = ('id', 'slug', 'user')

    def save_model(self, request, obj: Category, form, change):
        if not change:  # create
            obj.user = request.user
            # if Category.objects.get(slug=obj.slug):
            #     # unique error
            #     raise ValidationError('Album with same name exists')
        super().save_model(request, obj, form, change)
