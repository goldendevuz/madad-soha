from django.core.management.base import BaseCommand

from main.models import Specialty


class Command(BaseCommand):
    help = "Add predefined specialties to the database"

    def handle(self, *args, **options):
        specialties = [
            "Frontend",
            "Backend",
            "Grafik dizayn",
            "SMM",
            "Komp. savodxonligi",
            "AI savodxonligi",
            "Til qobiliyati",
        ]

        created_count = 0
        for title in specialties:
            specialty, created = Specialty.objects.get_or_create(title=title)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created specialty: {title}"))
                created_count += 1
            else:
                self.stdout.write(f"Specialty already exists: {title}")

        self.stdout.write(self.style.SUCCESS(f"Total new specialties created: {created_count}"))
