# from django.contrib import admin
# from .models import Photo, Video
#
#
# @admin.register(Photo)
# class PhotoAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         if not obj.pk:
#             # Only set added_by during the first save.
#             obj.created_by = request.user
#         super().save_model(request, obj, form, change)
#
#
# admin.site.register(Video)
