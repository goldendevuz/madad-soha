import json
from types import SimpleNamespace
import requests
from django.http import JsonResponse
from icecream import ic
from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from telegraph import Telegraph
from .google import get_user_rows
from .models import UserOption, Option, UserSpecialty, UserQuiz, Quiz
from .utils import format_as_html
from core.config import BEARER_AUTH_TOKEN, SMS_URL

User = get_user_model()

SHEET_ID = '1TQJiyNvJXaMbQvvweNO9Yeg6VuybdmeSycMtSM5VkyE'

async def send_sms_message(html_message, phone):
    url = SMS_URL

    payload = json.dumps({
    "number": phone.replace("+998", ""),
    "text": f"""{html_message}""",
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {BEARER_AUTH_TOKEN}',
    }
    ic(payload)
    ic(headers)

    response = requests.request("POST", url, headers=headers, data=payload)
    ic(response)
    ic(response.json())
    return response.json()

@api_view(['POST'])
def send_latest_google_response(request):
    responses_rows = get_user_rows(SHEET_ID)
    ic(responses_rows)
    if not responses_rows:
        return JsonResponse({'status': 'error', 'message': 'No data found'})
    responses_row = responses_rows[-1]
    ic(responses_row)

    if not responses_row or len(responses_row) < 17:
        return JsonResponse({'status': 'error', 'message': 'No data found'})

    user, created = User.objects.get_or_create(full_name=responses_row[17], student_phone=responses_row[15])

    quiz = Quiz.objects.get(title="Madad IT Qobiliyat")
    user_quiz = UserQuiz.objects.create(user=user, quiz=quiz)

    # repeated_question = "Quyidagilardan qaysi birini bajargansiz?"

    user_options_count = 0
    for option_text in responses_row[1:15]:
        if option_text:
            option_text = option_text.replace("‘", "'").replace("’", "'")
            ic(option_text)
            option = Option.objects.get(text=option_text)
            ic(option, "topildiyov")
            question = option.question
            ic(question, "topildi")
            UserOption.objects.get_or_create(
                user=user,
                quiz=user_quiz,
                question=question,
                option=option
            )
            user_options_count += 1

    # Get top 2 UserSpecialty objects by score
    top_specialties = list(
        UserSpecialty.objects.filter(user=user, quiz=user_quiz)
        .order_by('-score')[:2]
    )

    # Extract scores
    scores = [s.score for s in top_specialties]
    total = sum(scores)

    # Prepare result with specialty title and percentage
    result = SimpleNamespace(
        first=SimpleNamespace(
            title=top_specialties[0].specialty.title,
            percentage=round(top_specialties[0].score / total * 100, 2) if total else 0
        ),
        second=SimpleNamespace(
            title=top_specialties[1].specialty.title,
            percentage=round(top_specialties[1].score / total * 100, 2) if total else 0
        )
    )
    
    html_message = format_as_html(result)
    ic(html_message)

    async_to_sync(send_sms_message)(html_message, phone=responses_row[15])

    ic(user_options_count, "user_options_count")
    if user_options_count == 14:
        user_quiz.completed = True
        user_quiz.save(update_fields=['completed'])
    
    return JsonResponse({'status': 'sent', 'message': html_message})