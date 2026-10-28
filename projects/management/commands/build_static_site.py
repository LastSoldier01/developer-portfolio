from pathlib import Path
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.test import Client

from projects.models import Project


class Command(BaseCommand):
    help = "Build a static GitHub Pages site from the current Django templates and published projects."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default="dist",
            help="Directory where the static site will be written.",
        )
        parser.add_argument(
            "--base-path",
            default="/developer-portfolio",
            help="Base path used by GitHub Pages project sites.",
        )

    def handle(self, *args, **options):
        output_dir = Path(options["output"]).resolve()
        base_path = options["base_path"].rstrip("/")
        if not base_path.startswith("/"):
            base_path = "/" + base_path

        # GitHub Pages project sites are served under /<repository-name>/.
        settings.FORCE_SCRIPT_NAME = base_path
        settings.STATIC_URL = base_path + "/static/"
        from django.urls import set_script_prefix

        set_script_prefix(base_path + "/")

        # Collect static files first so they can be copied into the output.
        self.stdout.write("Collecting static files...")
        from django.core.management import call_command

        call_command("collectstatic", "--noinput", verbosity=0)

        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True)

        client = Client(HTTP_HOST="localhost")
        pages = [("/", "index.html")]
        pages.append(("/projects/", "projects/index.html"))

        for slug in Project.objects.filter(is_published=True).order_by(
            "order", "-created_at"
        ).values_list("slug", flat=True):
            pages.append((f"/projects/{slug}/", f"projects/{slug}/index.html"))

        self.stdout.write(f"Building {len(pages)} page(s)...")
        for url, relative_path in pages:
            destination = output_dir / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            try:
                response = client.get(url)
            except Exception as exc:  # pragma: no cover - build-time safety
                raise CommandError(f"Failed to render {url}: {exc}") from exc

            if response.status_code != 200:
                raise CommandError(
                    f"Failed to render {url}: HTTP {response.status_code}"
                )

            content = response.content
            if isinstance(content, bytes):
                content = content.decode(response.charset or "utf-8")
            destination.write_text(content, encoding="utf-8")
            self.stdout.write(f"  wrote {relative_path}")

        static_root = Path(settings.STATIC_ROOT)
        if static_root.exists():
            shutil.copytree(static_root, output_dir / "static")
            self.stdout.write("Copied collected static files to dist/static")

        self.stdout.write(self.style.SUCCESS(f"Static site written to {output_dir}"))