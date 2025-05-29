from icecream import ic

def format_as_html(result):
    if not result:
        return "Yangi javob to'liq emas."

    response = f"""Test natijangiz:
       
{result.first.title} - {result.first.title}
{result.second.title} - {result.second.percentage}

Bepul maslahat + chegirma olish uchun:
+998 99 600 77 07
"""
    ic(response)

    return response