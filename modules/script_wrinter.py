"""
1-BOSQICH: Mavzuni oladi -> internetdan ma'lumot izlaydi -> AI skript yozadi
Bepul: DuckDuckGo qidiruv (API key kerak emas) + Groq AI (bepul tier, tez Llama modellari)
"""
import os
from ddgs import DDGS
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # groq.com dan bepul olinadi


def search_topic(topic: str, max_results: int = 6) -> str:
    """Mavzu haqida internetdan qisqa ma'lumotlar to'playdi."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(topic, max_results=max_results):
            title = r.get("title", "")
            body = r.get("body", "")
            results.append(f"- {title}: {body}")
    return "\n".join(results) if results else "Internetdan ma'lumot topilmadi."


def write_script(topic: str, style: str = "gaming", duration_minutes: int = 5) -> str:
    """
    Topilgan ma'lumotlar asosida YouTube skript yozadi.
    style: 'gaming' (o'yin yangiliklari/sharh) yoki 'tutorial' (qo'llanma)
    """
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY topilmadi. .env fayliga GROQ_API_KEY=... qo'shing. "
            "Bepul key: https://console.groq.com/keys"
        )

    research = search_topic(topic)
    client = Groq(api_key=GROQ_API_KEY)

    system_prompt = (
        "Sen professional o'zbek tilida YouTube uchun kompyuter o'yinlari skript "
        "yozuvchisisan. Skript jonli, qiziqarli, gaming auditoriyasiga mos bo'lishi kerak. "
        "Har doim quyidagi tuzilmani ishlat:\n"
        "1) HOOK (birinchi 10 soniya - diqqatni tortadigan savol yoki fakt)\n"
        "2) ASOSIY QISM (faktlar, tahlil, o'z fikri bilan)\n"
        "3) YAKUN (like/subscribe chaqirig'i, keyingi video haqida ishora)\n"
        "Skript FAQAT gapiriladigan matn bo'lsin (ovozga o'qish uchun), "
        "qavs ichida rejissyorlik izohlari yozma."
    )

    user_prompt = (
        f"Mavzu: {topic}\n\n"
        f"Internetdan topilgan so'nggi ma'lumotlar:\n{research}\n\n"
        f"Shu ma'lumotlar asosida taxminan {duration_minutes} daqiqalik "
        f"(≈{duration_minutes * 130} so'z) o'zbek tilida video skript yoz."
    )

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,
    )
    return completion.choices[0].message.content.strip()


if __name__ == "__main__":
    topic = input("Video mavzusini kiriting: ")
    script = write_script(topic)
    print("\n--- TAYYOR SKRIPT ---\n")
    print(script)
