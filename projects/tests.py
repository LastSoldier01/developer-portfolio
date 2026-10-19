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
        self.assertTrue(self.project.is_published)
        self.assertEqual(self.project.order, 0)
        self.assertEqual(self.project.github_url, "")
        self.assertEqual(self.project.demo_url, "")

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
