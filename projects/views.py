from django.shortcuts import get_object_or_404, render

from .models import Project


def project_list(request):
    """Archive page listing every published project (newest first)."""
    projects = Project.objects.filter(is_published=True).prefetch_related("technologies")
    return render(request, "projects/project_list.html", {"projects": projects})


def project_detail(request, slug):
    """Detail page for a single published project; drafts return 404."""
    project = get_object_or_404(
        Project.objects.prefetch_related("technologies"),
        slug=slug,
        is_published=True,
    )
    return render(request, "projects/project_detail.html", {"project": project})
