import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from main.models import UserQuiz, Quiz, UserOption

User = get_user_model()


class Command(BaseCommand):
    help = "Create a fresh UserQuiz for 'goldendev' and generate 14 random UserOption answers."

    def handle(self, *args, **options):
        user = User.objects.get(username="goldendev")
        quiz = Quiz.objects.get(title="Madad IT Qobiliyat")

        # ✅ Always create a new UserQuiz (no get_or_create)
        user_quiz = UserQuiz.objects.create(user=user, quiz=quiz, completed=False)
        self.stdout.write(self.style.SUCCESS(f"🆕 Created new UserQuiz: ID {user_quiz.id}"))

        questions = quiz.questions.all().order_by('order')

        for question in questions:
            options = list(question.options.all())
            if not options:
                self.stdout.write(self.style.WARNING(f"❌ No options for question {question.text}"))
                continue

            selected_option = random.choice(options)  # <-- Correct: choose Option instance directly

            UserOption.objects.create(
                user=user,
                quiz=user_quiz,
                question=question,
                option=selected_option,  # Pass Option instance, NOT option_id
            )

            self.stdout.write(self.style.SUCCESS(f"✅ Q{question.order}: {selected_option.text}"))

        # ✅ Mark quiz as completed
        user_quiz.completed = True
        user_quiz.save()

        self.stdout.write(self.style.SUCCESS("🎯 Quiz attempt completed with 14 random answers!"))
