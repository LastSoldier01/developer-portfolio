from django.shortcuts import render

from projects.models import Project, Technology


def home(request):
    """Single-page portfolio home with hero, about, projects and contact."""
    featured_projects = (
        Project.objects.filter(is_published=True, is_featured=True)
        .prefetch_related("technologies")
    )
    other_projects = (
        Project.objects.filter(is_published=True, is_featured=False)
        .prefetch_related("technologies")
    )
    technologies = Technology.objects.filter(is_visible=True)

    context = {
        "featured_projects": featured_projects,
        "other_projects": other_projects,
        "technologies": technologies,
    }
    return render(request, "pages/home.html", context)