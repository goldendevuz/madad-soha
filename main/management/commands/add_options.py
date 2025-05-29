from django.core.management.base import BaseCommand, CommandError

from main.models import Option, Question


class Command(BaseCommand):
    help = "Add options to 14 questions (4 per question, total 56 options)"

    def handle(self, *args, **options):
        question_ids = [
            # First 9 questions
            "89e515bf-aacb-4cc2-a958-7f46858393ef",
            "7eb52f9b-5ec1-46bf-be69-5892e8aeeff1",
            "accf8951-fb62-46eb-a414-11968be274a8",
            "39ea6f59-d66b-412f-9d69-ee1c0e389110",
            "e7dabe90-4eb5-4313-8b45-972466039c28",
            "01db9df5-9943-46ab-9f50-5682955fefa3",
            "2474569b-ba88-4a5b-b026-4aa7e7c8fe21",
            "732a26b7-9dfd-4f7b-88f9-2d55cfa77c49",
            "0e56208d-cd06-42ef-9b74-8b3a4983e006",
            # New questions 10–14
            "4477fcba-7029-462d-b05d-9ba43c2ed708",
            "8362635b-6c8c-4a44-b1f4-aa13db15bedc",
            "8bb37db4-08d0-4be9-b654-0ce13e8125c5",
            "6d684c5f-7e97-4e25-9f99-21a26e0a34de",
            "134ce033-eec6-4b56-a702-e532b52de8c2",
        ]

        option_texts = [
            # First 36
            "Chiroyli va tartibli ko‘rinishiga",
            "Qanchalik ishlashiga",
            "Qulaylik va tartibga",
            "Axborot tushunarliligiga",
            "Tashqi dizayn bilan ishlash",
            "Tizimini yaratish",
            "Matnlar va postlar tayyorlash",
            "Ma’lumotlarni boshqarish",
            "Sayt tuzilmasini yaratish",
            "Grafik interfeysga ishlov berish",
            "Matnlar va tarjimalar ustida ishlash",
            "Ijtimoiy tarmoqlarga kontent tayyorlash",
            "Tahliliy hisob-kitob qilish",
            "Yaratuvchanlik, dizaynlar qilish",
            "Post va hikoyalar yozish",
            "Rejali tizim qurish",
            "Jarayonni avtomatlashtirish",
            "Chizmalarda ifodalash",
            "Formulalar bilan soddalashtirish",
            "Tarjima qilish",
            "Sahifani mobil qurilmaga moslash",
            "Katta hajmdagi ma’lumotni soddalashtirish",
            "Ishlarni jadvalga asosida boshqarish",
            "So‘z boyligimni  oshirish",
            "Figma yoki Canva’da dizayn qilganman",
            "Python yoki boshqa kodlarni sinab ko‘rganman",
            "Telegram yoki WhatsApp bot ishlatib ko‘rganman",
            "Duolingo, LingQ kabi ilovalar orqali til o‘rganganman",
            "Dizayner yoki SMMchi bo‘lishni xohlayman",
            "Frontend yoki backend dasturchi bo‘lishni xohlayman",
            "AI (suniy idrok) bilan ishlashni xohlayman",
            "Tarjima bilan shug‘ullanishni xohlayman",
            "Telegram postlar yozganman",
            "Excel’da formulalar yozganman",
            "Canva’da dizayn qilganman",
            "Chet tillaridagi darslarni eshitganman",
            # New 20
            "HTML orqali oddiy veb sahifa tuzganman",
            "Kompyuterdagi fayllarni tartibli saqlayman",
            "Sun’iy intellekt foydalanaman",
            "O‘zbek tilida grammatik jihatdan to‘g‘ri yozaman",
            "Boshidan qayta boshlayman",
            "Kodni tahlil qilib, xatoni aniqlashga harakat qilaman",
            "Foydalanuvchi nuqtai nazaridan baholayman",
            "Xorijiy manbalardan foydalanaman",
            "Sun’iy intellekt  biznesni rivojlantirish uchun kerak",
            "Dizayn va ko‘rinishlar foydalanuvchiga qulay bo'lishi kerak",
            "Matnni qisqa va tushunarli yozish kerak",
            "Takrorlanadigan ishlarni avtomatiklashtirish kerak",
            "Dasturlash bilan muammoni yechish",
            "Banner, logo yoki vizual postlar qilish",
            "Subtitrsiz xorijiy videoni ko'rish",
            "Ijtimoiy tarmoqlarda maxsulotni reklama qilish",
            "Ko‘rinish, qulaylik va soddalik",
            "Tizim qanday ishlashi",
            "Postdagi sarlavha va matnlar",
            "Ma’lumotlarni to‘g‘ri joyda saqlash",
        ]

        if len(question_ids) * 4 != len(option_texts):
            raise CommandError(
                "❌ Each question must receive exactly 4 options. Ensure 4 x question_count == total_options.")

        created_total = 0

        for i, qid in enumerate(question_ids):
            try:
                question = Question.objects.get(id=qid)
            except Question.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"❌ Question not found: {qid}"))
                continue

            start = i * 4
            for order, text in enumerate(option_texts[start:start + 4], start=1):
                option, created = Option.objects.get_or_create(
                    question=question,
                    text=text,
                    defaults={"order": order}
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Created option: '{text}' (order {order}) for question {qid}"))
                    created_total += 1
                else:
                    self.stdout.write(f"⚠️ Option already exists: '{text}' for question {qid}")

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Total new options created: {created_total}"))
