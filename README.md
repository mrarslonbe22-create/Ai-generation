# 🎮 Gaming Video AI

Mavzuni kiritasiz → AI internetdan ma'lumot izlab skript yozadi → AI ovozga aylantiradi →
sizning gameplay videongiz bilan avtomatik montaj qilib, tayyor YouTube videosini beradi.

**Narx: 100% bepul** (agar cheklovlarga rioya qilsangiz — pastda tushuntirilgan).

## Qanday ishlaydi (3 bosqich)

1. **Skript yozish** — `modules/script_writer.py`
   DuckDuckGo orqali (bepul, kalit kerak emas) internetdan mavzu bo'yicha so'nggi
   ma'lumot izlaydi, so'ng Groq AI (bepul, tez Llama 3.3 70B modeli) orqali
   o'zbek tilida tayyor skript yozadi.

2. **Ovozga aylantirish** — `modules/tts_generator.py`
   Microsoft Edge TTS (butunlay bepul, cheksiz) orqali skriptni tabiiy
   o'zbekcha ovozga aylantiradi va subtitr (SRT) fayl yaratadi.

3. **Video montaj** — `modules/video_editor.py`
   Siz yuklagan gameplay videoni kerakli uzunlikka moslaydi (kesadi/takrorlaydi),
   ustiga ovozni va avtomatik subtitrlarni qo'yib, tayyor `.mp4` fayl chiqaradi.

Veb-interfeys (`app.py` + `templates/index.html`) — brauzerda mavzu yozib,
gameplay faylni yuklab, "Video yaratish" tugmasini bosasiz — 2-5 daqiqada
tayyor video pastga tushadi.

## O'rnatish

```bash
git clone <sizning-repo-havolangiz>
cd game-video-ai
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Tizimda `ffmpeg` o'rnatilgan bo'lishi kerak (video montaj uchun):
```bash
# Ubuntu/Debian
sudo apt install ffmpeg
# Mac
brew install ffmpeg
# Windows: ffmpeg.org dan yuklab, PATH'ga qo'shing
```

### Bepul API kalitini olish (faqat 1 ta kerak)

1. https://console.groq.com/keys ga kiring, ro'yxatdan o'ting (bepul)
2. API key yarating
3. Loyiha papkasida `.env` fayl yarating (`.env.example`dan nusxa oling):
   ```
   GROQ_API_KEY=sizning_kalitingiz
   ```

Groq'ning bepul tarifi kuniga yetarlicha so'rov beradi — kichik/o'rta kanal uchun yetadi.

## Ishga tushirish

```bash
python app.py
```

Brauzerda oching: `http://localhost:5000`

Yoki terminal orqali (veb-saytsiz) sinab ko'rish:
```bash
python modules/script_writer.py
```

## GitHub'ga joylash

```bash
git init
git add .
git commit -m "Gaming video AI - boshlang'ich versiya"
git branch -M main
git remote add origin https://github.com/FOYDALANUVCHI_NOMI/REPO_NOMI.git
git push -u origin main
```

⚠️ `.env` faylini hech qachon GitHub'ga yuklamang — u `.gitignore`da allaqachon
istisno qilingan, unutmang tekshirib ko'ring.

## Bepul qolishi uchun cheklovlar

| Qism | Bepul limit |
|---|---|
| DuckDuckGo qidiruv | Cheklovsiz (lekin haddan tashqari tez-tez so'rov yubormang) |
| Groq AI (skript) | Kuniga bir necha ming so'rov (bepul tier) |
| Edge TTS (ovoz) | Cheksiz bepul |
| Video montaj (ffmpeg/moviepy) | Sizning kompyuteringiz protsessoridan foydalanadi — narxi yo'q |

Agar kanal katta bo'lib, Groq limitiga tegib qolsangiz, boshqa bepul
muqobillar: Google Gemini (bepul tier), yoki OpenRouter'dagi bepul modellar.
`modules/script_writer.py` faylidagi `client`ni almashtirish kifoya.

## Render'ga joylash

1. Loyihani GitHub'ga joylang (yuqoridagi bo'limga qarang)
2. https://render.com ga kiring, GitHub akkauntingiz bilan ro'yxatdan o'ting
3. **New +** → **Web Service** → repo'ingizni tanlang
4. Render `Dockerfile`ni avtomatik taniydi (environment: **Docker** deb tanlang)
5. **Environment** bo'limida `GROQ_API_KEY` o'zgaruvchisini qo'shing (qiymatini kiriting)
6. **Instance type**: Free tanlang → **Create Web Service**
7. Birinchi build 5-10 daqiqa davom etadi (ffmpeg o'rnatilishi kerak)

Deploy tugagach, sizga `https://sizning-loyiha.onrender.com` ko'rinishidagi doimiy havola beriladi.

### Bepul tarifning cheklovlari (bilib qo'ying)

- **Uxlab qolish**: 15 daqiqa faoliyatsizlikdan keyin sayt "uxlaydi", keyingi kirishda 30-60 soniya kutasiz (bu normal, xato emas)
- **Vaqtinchalik fayllar**: Bepul tarifda doimiy disk yo'q — agar servis qayta ishga tushsa (redeploy yoki uzoq vaqt uxlab, qayta uyg'onganda), oldingi yaratilgan videolar o'chib ketishi mumkin. Shuning uchun video yaratilgach, **darhol yuklab oling**, keyinga qoldirmang
- **RAM cheklovi**: Bepul tarifda 512MB RAM bor — juda uzun yoki og'ir gameplay videolar (masalan 4K, 10+ daqiqa) xotira yetishmasligiga olib kelishi mumkin. Shunday xato chiqsa, gameplay videoni qisqaroq yoki past sifatli qilib yuklang

Agar bular halaqit bersa, keyinchalik $7/oy'lik "Starter" tarifga o'tsangiz, uxlash va disk muammolari yo'qoladi.

## Keyingi qadamlar (ixtiyoriy yaxshilashlar)

- Avtomatik YouTube'ga yuklash (YouTube Data API orqali)
- Thumbnail generatori qo'shish
- Ko'p tilli ovoz tanlash
- Video tarixini saqlaydigan bazaga ulash
