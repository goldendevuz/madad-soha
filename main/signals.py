from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import UserOption, Score, UserSpecialty


@receiver(post_save, sender=UserOption)
def update_user_specialty_score(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user
    quiz = instance.quiz.quiz if instance.quiz and instance.quiz.quiz else None
    user_quiz = instance.quiz if instance.quiz else None
    option = instance.option
    question = instance.question

    if not user_quiz:
        return

    # Get all Score rows related to the selected option in the quiz
    scores = Score.objects.filter(quiz=quiz, option=option)

    for score in scores:
        user_specialty, created = UserSpecialty.objects.get_or_create(
            user=user,
            quiz=user_quiz,
            specialty=score.specialty,
            defaults={'question': question, 'score': 0}
        )
        user_specialty.score += 1
        user_specialty.save()
