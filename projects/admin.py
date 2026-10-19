from django.contrib import admin

from .models import Project, Technology


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "order", "is_visible")
    list_filter = ("category", "proficiency", "is_visible")
    search_fields = ("name",)
    ordering = ("order", "name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "is_featured", "order", "created_at")
    list_filter = ("is_published", "is_featured", "technologies", "created_at")
    search_fields = ("title", "summary", "description")
    ordering = ("order", "-created_at")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies",)
    readonly_fields = ("created_at", "updated_at")
