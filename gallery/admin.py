from django.contrib import admin

from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline, SortableTabularInline

from .models import Category, Navbar


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'slug', 'user')

    def save_model(self, request, obj: Category, form, change):
        if not change:  # create
            obj.user = request.user
        super().save_model(request, obj, form, change)


class CategoryInline(SortableTabularInline):
    model = Category
    extra = 0
    readonly_fields = ('title', 'slug', 'user')


@admin.register(Navbar)
class NavbarAdmin(NonSortableParentAdmin):
    inlines = [CategoryInline]
    readonly_fields = ('user',)

    def has_add_permission(self, request):
        return Navbar.objects.filter(user=request.user).count() == 0

    def save_model(self, request, obj: Navbar, form, change):
        if not change:
            obj.user = request.user
        super(NavbarAdmin, self).save_model(request, obj, form, change)
