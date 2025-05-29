import json
import requests
from django.http import JsonResponse
from icecream import ic
from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from telegraph import Telegraph

from .google import get_user_rows, get_result_rows
from .models import UserOption, Option, UserSpecialty, UserQuiz, Quiz
from .utils import format_as_html, format_as_html_parents
from core.config import BEARER_AUTH_TOKEN

User = get_user_model()

SHEET_ID = '18r4BkP9NU7r2MLTG-oBPTSbVHkzZimVy96OhUXhskRM'

async def send_sms_message(html_message, phone):
    url = "https://piglet-factual-mentally.ngrok-free.app/api/sms/"

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

    rows = get_result_rows(SHEET_ID)
    if not rows:
        return JsonResponse({'status': 'error', 'message': 'No data found'})

    user, created = User.objects.get_or_create(full_name=responses_row[16], student_phone=responses_row[15])

    quiz = Quiz.objects.get(title="Madad IT Qobiliyat")
    user_quiz = UserQuiz.objects.create(user=user, quiz=quiz)

    user_options_count = 0
    for option_text in responses_row[1:15]:
        if option_text:
            option = Option.objects.get(text=option_text)
            question = option.question
            UserOption.objects.get_or_create(
                user=user,
                quiz=user_quiz,
                question=question,
                option=option
            )
            user_options_count += 1

    full_name = responses_row[21]

    telegraph = Telegraph()
    telegraph.create_account(short_name='testbot')

    title = request.data.get('title', 'Farzandingizning test natijangiz')

    content = full_name
    response = telegraph.create_page(
        title=title,
        html_content=f'<p>{content}</p>',
    )
    # ic(response)
    html_message = format_as_html(responses_row, path=response['path'])
    ic(html_message)

    async_to_sync(send_sms_message)(html_message, phone=responses_row[15])

    if user_options_count == 14:
        user_quiz.completed = True
    return JsonResponse({'status': 'sent', 'message': html_message})