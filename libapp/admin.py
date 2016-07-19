from django.contrib import admin
from libapp.models import Book, DVD, Libuser, Libitem, Suggestion
import datetime
from PIL import Image


# Register your models here.
class BookInline(admin.StackedInline):
    model = Book  # This shows all fields of Book.
    fields = [('title', 'author'), 'duedate',]   #  Customizes to show only certain fields
    extra = 0


class DVDInline(admin.StackedInline):
    model = DVD
    fields = [('title', 'maker', 'pubyr', 'duration'), ('checked_out', 'itemtype', 'user', 'duedate'), 'rating']
    extra = 0



class ImageInline(admin.TabularInline):
    model = Libuser
    fields = ['photo']
    extra = 0


def renew(modeladmin, request, queryset):
    for obj in queryset:
        if obj.checked_out == True:
            queryset.update(duedate=obj.duedate + datetime.timedelta(days=21))


class LibuserAdmin(admin.ModelAdmin):
    fields = [('username'), ('first_name', 'last_name')]
    list_display = ('username', 'first_name', 'admin_image')
    inlines = [BookInline, DVDInline, ImageInline]


class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'author', 'pubyr'), ('checked_out', 'itemtype', 'user', 'duedate'),'category']
    list_display = ('title', 'borrower', 'overdue')
    actions = [renew]

    def borrower(self, obj=None):
        if obj.checked_out == True:
            return obj.user     #Returns the user who has borrowed this book
        else:
            return ''


class DVDAdmin(admin.ModelAdmin):
    fields = [('title', 'maker', 'pubyr'), ('checked_out', 'itemtype', 'user', 'duedate'), 'rating']
    list_display = ('title', 'rating', 'borrower','overdue')
    actions = [renew]

    def borrower(self, obj=None):
        if obj.checked_out == True:
            return obj.user      #Return the user who has borrowed this book
        else:
            return ''



admin.site.register(Book, BookAdmin)
admin.site.register(DVD, DVDAdmin)
admin.site.register(Libuser, LibuserAdmin)
admin.site.register(Suggestion)


