from django.test import TestCase

from .models import Project, Technology


class TechnologyModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.python = Technology.objects.create(
            name="Python",
            slug="python",
            category=Technology.Category.LANGUAGE,
            proficiency=Technology.Proficiency.ADVANCED,
            order=1,
        )
        cls.django = Technology.objects.create(
            name="Django",
            slug="django",
            category=Technology.Category.FRAMEWORK,
            proficiency=Technology.Proficiency.INTERMEDIATE,
            order=2,
        )

    def test_str_returns_name(self):
        self.assertEqual(str(self.python), "Python")
        self.assertEqual(str(self.django), "Django")

    def test_defaults(self):
        technology = Technology.objects.create(name="Git", slug="git")
        self.assertEqual(technology.category, Technology.Category.OTHER)
        self.assertEqual(technology.proficiency, Technology.Proficiency.BEGINNER)
        self.assertEqual(technology.order, 0)
        self.assertTrue(technology.is_visible)

    def test_default_ordering_is_order_then_name(self):
        self.assertEqual(list(Technology.objects.all()), [self.python, self.django])

    def test_created_and_updated_timestamps_are_set(self):
        self.assertIsNotNone(self.python.created_at)
        self.assertIsNotNone(self.python.updated_at)


class ProjectModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.python = Technology.objects.create(name="Python", slug="python")
        cls.django = Technology.objects.create(name="Django", slug="django")
        cls.project = Project.objects.create(
            title="Task Manager API",
            slug="task-manager-api",
            summary="A REST API for managing tasks.",
            description="A full description of the Task Manager API.",
        )
        cls.project.technologies.set([cls.python, cls.django])

    def test_str_returns_title(self):
        self.assertEqual(str(self.project), "Task Manager API")

    def test_defaults(self):
        self.assertFalse(self.project.is_featured)
        self.assertFalse(self.project.is_published)  # new projects start as drafts
        self.assertEqual(self.project.order, 0)
        self.assertEqual(self.project.github_url, "")
        self.assertEqual(self.project.demo_url, "")
        self.assertFalse(self.project.cover_image)  # image is optional

    def test_many_to_many_relationship(self):
        self.assertEqual(self.project.technologies.count(), 2)
        # assertCountEqual ignores order — it checks that both items are present.
        self.assertCountEqual(self.project.technologies.all(), [self.python, self.django])
        # Reverse relation: every technology knows its projects (related_name="projects")
        self.assertIn(self.project, self.python.projects.all())
        self.assertIn(self.project, self.django.projects.all())

    def test_project_without_technologies_is_allowed(self):
        bare_project = Project.objects.create(
            title="Scratch Pad", slug="scratch-pad", summary="Tiny project.", description="Details."
        )
        self.assertEqual(bare_project.technologies.count(), 0)

    def test_default_ordering_is_order_then_newest_first(self):
        newer = Project.objects.create(
            title="Second Project", slug="second-project", summary="Newer one.", description="Details."
        )
        # Both have order=0, so the most recently created project comes first.
        self.assertEqual(list(Project.objects.all()), [newer, self.project])


class HomeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.python = Technology.objects.create(name="Python", slug="python")
        cls.hidden_tech = Technology.objects.create(name="COBOL", slug="cobol", is_visible=False)
        cls.featured = Project.objects.create(
            title="Featured API",
            slug="featured-api",
            summary="Summary.",
            description="Details.",
            is_published=True,
            is_featured=True,
        )
        cls.other = Project.objects.create(
            title="Small Tool",
            slug="small-tool",
            summary="Summary.",
            description="Details.",
            is_published=True,
        )
        cls.draft = Project.objects.create(
            title="Secret Draft",
            slug="secret-draft",
            summary="Summary.",
            description="Details.",
            is_featured=True,  # unpublished drafts must never appear
        )

    def test_home_renders_with_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_splits_featured_and_other_projects(self):
        response = self.client.get("/")
        featured = list(response.context["featured_projects"])
        other = list(response.context["other_projects"])
        self.assertEqual([p.pk for p in featured], [self.featured.pk])
        self.assertEqual([p.pk for p in other], [self.other.pk])

    def test_home_never_includes_unpublished_projects(self):
        response = self.client.get("/")
        shown = list(response.context["featured_projects"]) + list(response.context["other_projects"])
        self.assertNotIn(self.draft, shown)

    def test_home_shows_only_visible_technologies(self):
        response = self.client.get("/")
        names = [t.name for t in response.context["technologies"]]
        self.assertEqual(names, ["Python"])


class ProjectViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.published = Project.objects.create(
            title="Published API",
            slug="published-api",
            summary="Summary.",
            description="A longer body.",
            is_published=True,
        )
        cls.draft = Project.objects.create(
            title="Draft API",
            slug="draft-api",
            summary="Summary.",
            description="Details.",
        )

    def test_archive_lists_only_published_projects(self):
        response = self.client.get("/projects/")
        self.assertEqual(response.status_code, 200)
        projects = list(response.context["projects"])
        self.assertEqual([p.pk for p in projects], [self.published.pk])

    def test_detail_renders_published_project(self):
        response = self.client.get(f"/projects/{self.published.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published API")

    def test_detail_returns_404_for_draft(self):
        response = self.client.get(f"/projects/{self.draft.slug}/")
        self.assertEqual(response.status_code, 404)

    def test_detail_returns_404_for_unknown_slug(self):
        response = self.client.get("/projects/no-such-project/")
        self.assertEqual(response.status_code, 404)
