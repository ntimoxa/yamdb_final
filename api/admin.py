from .models import Title, Categories, Genres, Review, Comment
from django.contrib import admin


class TitleModel(admin.ModelAdmin):
    list_display = ('pk', "name", "year", "description", "category")


class GenreModel(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "author", "score", "pub_date")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("review", "text", "author", "pub_date")


admin.site.register(Title, TitleModel)
admin.site.register(Categories, CategoryAdmin)
admin.site.register(Genres, GenreModel)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
