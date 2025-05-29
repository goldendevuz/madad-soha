from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from main.models import UserQuiz, Quiz

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(username="goldendev")
        quiz = Quiz.objects.get(title="Madad IT Qobiliyat")

        user_quiz, created = UserQuiz.objects.get_or_create(
            user=user,
            quiz=quiz,
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Created user_quiz"))
        else:
            self.stdout.write(f"⚠️ UserQuiz already exists")
