"""
2-BOSQICH: Skriptni tabiiy ovozga aylantiradi (bepul, Microsoft Edge TTS)
Va so'zlarning vaqt belgilarini (subtitr uchun) chiqaradi.
"""
import asyncio
import edge_tts

# O'zbekcha ovozlar (bepul, Microsoft Edge TTS ichida mavjud)
VOICE_MALE = "uz-UZ-SardorNeural"
VOICE_FEMALE = "uz-UZ-MadinaNeural"


async def _generate(text: str, voice: str, audio_path: str, subs_path: str):
    communicate = edge_tts.Communicate(text, voice, rate="+5%")
    submaker = edge_tts.SubMaker()
    with open(audio_path, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
    with open(subs_path, "w", encoding="utf-8") as f:
        f.write(submaker.get_srt())


def text_to_speech(script: str, out_dir: str, voice: str = VOICE_MALE):
    """
    script -> audio.mp3 + subtitles.srt
    Qaytaradi: (audio_path, subs_path)
    """
    audio_path = f"{out_dir}/narration.mp3"
    subs_path = f"{out_dir}/subtitles.srt"
    asyncio.run(_generate(script, voice, audio_path, subs_path))
    return audio_path, subs_path


if __name__ == "__main__":
    sample = "Assalomu alaykum, bugungi videoda eng qiziqarli o'yin yangiliklarini muhokama qilamiz."
    a, s = text_to_speech(sample, ".")
    print("Audio:", a)
    print("Subtitr:", s)
