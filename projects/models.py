from django.db import models


class Technology(models.Model):
    """A language, framework, database or tool shown in the skills section
    and used to tag projects."""

    class Category(models.TextChoices):
        LANGUAGE = "Language", "Language"
        FRAMEWORK = "Framework", "Framework"
        DATABASE = "Database", "Database"
        TOOL = "Tool", "Tool"
        OTHER = "Other", "Other"

    class Proficiency(models.TextChoices):
        BEGINNER = "Beginner", "Beginner"
        INTERMEDIATE = "Intermediate", "Intermediate"
        ADVANCED = "Advanced", "Advanced"

    name = models.CharField(max_length=100, unique=True, help_text="Display name, e.g. Python")
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="URL-friendly identifier, e.g. python (auto-filled from name in the admin)",
    )
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    proficiency = models.CharField(
        max_length=20, choices=Proficiency.choices, default=Proficiency.BEGINNER
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order; lower numbers appear first")
    is_visible = models.BooleanField(default=True, help_text="Show this technology on the public site")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name


class Project(models.Model):
    """A portfolio project managed through the Django admin."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="URL-friendly identifier (auto-filled from title in the admin)",
    )
    summary = models.CharField(
        max_length=300, help_text="One or two sentences shown on project cards"
    )
    description = models.TextField(help_text="Full description shown on the project detail page")
    technologies = models.ManyToManyField(
        Technology, related_name="projects", blank=True, help_text="Technologies used in this project"
    )
    github_url = models.URLField(max_length=500, blank=True, help_text="Optional link to the repository")
    demo_url = models.URLField(max_length=500, blank=True, help_text="Optional link to the live demo")
    is_featured = models.BooleanField(default=False, help_text="Highlight this project on the homepage")
    is_published = models.BooleanField(
        default=False, help_text="Only published projects appear on the public site (new projects start as drafts)"
    )
    cover_image = models.ImageField(
        upload_to="covers/",
        blank=True,
        null=True,
        help_text="Optional screenshot for the featured-project card (a styled placeholder is used when empty)",
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order; lower numbers appear first")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title
