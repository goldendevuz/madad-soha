from django.core.management.base import BaseCommand
from icecream import ic

from main.models import Quiz, Option, Specialty, Score


class Command(BaseCommand):
    help = "Add 113 scores based on predefined mappings"

    def handle(self, *args, **kwargs):
        quiz = Quiz.objects.get(title="Madad IT Qobiliyat")  # Adjust as needed

        # Columns as specialties (must match the Specialty.title exactly)
        specialties = [
            "Frontend", "Backend", "Grafik dizayn", "SMM",
            "Kompyuter savodxonligi", "AI savodxonligi", "Til qobiliyati"
        ]

        # Each row: [question_order, question_text, f, b, gd, smm, k, ai, ti]
        data = [
            ("Chiroyli va tartibli ko'rinishiga", 1, 0, 1, 0, 0, 0, 0),
            ("Qanchalik ishlashiga", 0, 1, 0, 0, 0, 0, 0),
            ("Qulaylik va tartibga", 1, 1, 0, 0, 1, 0, 0),
            ("Axborot tushunarliligiga", 0, 0, 0, 1, 1, 0, 1),
            ("Tashqi dizayn bilan ishlash", 1, 0, 1, 0, 0, 0, 0),
            ("Tizimini yaratish", 0, 1, 0, 0, 0, 1, 0),
            ("Matnlar va postlar tayyorlash", 0, 0, 0, 1, 0, 0, 1),
            ("Ma'lumotlarni boshqarish", 0, 1, 0, 0, 1, 0, 0),
            ("Sayt tuzilmasini yaratish", 1, 0, 0, 0, 0, 1, 0),
            ("Grafik interfeysga ishlov berish", 1, 0, 1, 1, 0, 0, 0),
            ("Matnlar va tarjimalar ustida ishlash", 0, 0, 0, 1, 0, 0, 1),
            ("Ijtimoiy tarmoqlarga kontent tayyorlash", 0, 0, 0, 1, 0, 1, 0),
            ("Tahliliy hisob-kitob qilish", 0, 1, 0, 0, 1, 1, 0),
            ("Yaratuvchanlik, dizaynlar qilish", 1, 0, 1, 0, 0, 1, 0),
            ("Post va hikoyalar yozish", 0, 0, 0, 1, 0, 1, 1),
            ("Rejali tizim qurish", 0, 1, 0, 0, 1, 1, 0),
            ("Jarayonni avtomatlashtirish", 0, 1, 0, 0, 1, 1, 0),
            ("Chizmalarda ifodalash", 1, 0, 1, 0, 0, 1, 0),
            ("Formulalar bilan soddalashtirish", 0, 1, 0, 0, 1, 1, 0),
            ("Tarjima qilish", 0, 0, 0, 0, 0, 0, 1),
            ("Sahifani mobil qurilmaga moslash", 1, 0, 1, 0, 0, 0, 0),
            ("Katta hajmdagi ma'lumotni soddalashtirish", 0, 1, 0, 0, 1, 0, 0),
            ("Ishlarni jadvalga asosida boshqarish", 0, 1, 0, 0, 1, 0, 0),
            ("So'z boyligimni oshirish", 0, 0, 0, 0, 0, 0, 1),
            ("Figma yoki Canva'da dizayn qilganman", 1, 0, 1, 1, 0, 0, 0),
            ("Python yoki boshqa kodlarni sinab ko'rganman", 1, 1, 0, 0, 0, 0, 0),
            ("Telegram yoki WhatsApp bot ishlatib ko'rganman", 0, 1, 0, 0, 0, 1, 0),
            ("Duolingo, LingQ kabi ilovalar orqali til o'rganganman", 0, 0, 0, 0, 0, 0, 1),
            ("Dizayner yoki SMMchi bo'lishni xohlayman", 0, 0, 1, 1, 0, 0, 0),
            ("Frontend yoki backend dasturchi bo'lishni xohlayman", 1, 1, 0, 0, 0, 0, 0),
            ("AI (suniy idrok) bilan ishlashni xohlayman", 0, 0, 0, 0, 0, 1, 0),
            ("Tarjima bilan shug'ullanishni xohlayman", 0, 0, 0, 0, 0, 0, 1),
            ("Telegram postlar yozganman", 0, 0, 0, 1, 0, 1, 1),
            ("Excel'da formulalar yozganman", 0, 0, 0, 0, 1, 0, 0),
            ("Canva'da dizayn qilganman", 1, 0, 1, 1, 0, 0, 0),
            ("Chet tillaridagi darslarni eshitganman", 0, 0, 0, 0, 0, 0, 1),
            ("HTML orqali oddiy veb sahifa tuzganman", 1, 1, 0, 0, 0, 0, 0),
            ("Kompyuterdagi fayllarni tartibli saqlayman", 0, 0, 0, 0, 1, 0, 0),
            ("Sun'iy intellektdan foydalanaman", 0, 0, 1, 0, 0, 1, 0),
            ("O'zbek tilida grammatik jihatdan to'g'ri yozaman", 0, 0, 0, 1, 0, 0, 1),
            ("Boshidan qayta boshlayman", 1, 0, 1, 0, 0, 0, 0),
            ("Kodni tahlil qilib, xatoni aniqlashga harakat qilaman", 0, 1, 0, 0, 0, 1, 0),
            ("Foydalanuvchi nuqtai nazaridan baholayman", 0, 0, 0, 1, 0, 0, 1),
            ("Xorijiy manbalardan foydalanaman", 0, 0, 0, 0, 0, 0, 1),
            ("Sun'iy intellekt biznesni rivojlantirish uchun kerak", 0, 0, 0, 1, 0, 1, 0),
            ("Dizayn va ko'rinishlar foydalanuvchiga qulay bo'lishi kerak", 1, 0, 1, 0, 0, 0, 0),
            ("Matnni qisqa va tushunarli yozish kerak", 0, 0, 0, 1, 0, 0, 1),
            ("Takrorlanadigan ishlarni avtomatiklashtirish kerak", 0, 0, 0, 0, 1, 1, 0),
            ("Dasturlash bilan muammoni yechish", 0, 1, 0, 0, 0, 0, 0),
            ("Banner, logo yoki vizual postlar qilish", 1, 0, 1, 0, 0, 0, 0),
            ("Subtitrsiz xorijiy videoni ko'rish", 0, 0, 0, 0, 0, 0, 1),
            ("Ijtimoiy tarmoqlarda maxsulotni reklama qilish", 0, 0, 0, 1, 0, 1, 1),
            ("Ko'rinish, qulaylik va soddalik", 1, 0, 1, 0, 0, 0, 0),
            ("Tizim qanday ishlashi", 0, 1, 0, 0, 0, 0, 0),
            ("Postdagi sarlavha va matnlar", 0, 0, 0, 1, 0, 0, 1),
            ("Ma'lumotlarni to'g'ri joyda saqlash", 0, 1, 0, 0, 1, 0, 0),
        ]

        # Process each row
        created = 0
        for row in data:
            o_text, *spec_flags = row

            try:
                ic(o_text)
                option = Option.objects.get(text=o_text)  # Adjust if dynamic
            except Option.DoesNotExist:
                self.stderr.write(f"❌ Option not found - {o_text}")
                continue

            for idx, flag in enumerate(spec_flags):
                if flag:
                    specialty_title = specialties[idx]
                    try:
                        specialty = Specialty.objects.get(title=specialty_title)
                        _, created_obj = Score.objects.get_or_create(
                            quiz=quiz,
                            option=option,
                            specialty=specialty
                        )
                        if created_obj:
                            created += 1
                    except Specialty.DoesNotExist:
                        self.stderr.write(f"❌ Specialty not found: {specialty_title}")

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully created {created} scores."))
