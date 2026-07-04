"""
3-BOSQICH: Sizning screen-record qilgan gameplay videongizni +
AI ovozli hikoya + subtitrlarni birlashtirib, tayyor YouTube videosini yasaydi.
"""
import re
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
)


def _parse_srt(srt_path: str):
    """SRT faylini [(start_sec, end_sec, text), ...] ro'yxatiga aylantiradi."""
    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    def to_sec(ts: str) -> float:
        h, m, rest = ts.split(":")
        s, ms = rest.split(",")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    blocks = content.strip().split("\n\n")
    subs = []
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        times = lines[1]
        match = re.match(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)", times)
        if not match:
            continue
        start, end = to_sec(match.group(1)), to_sec(match.group(2))
        text = " ".join(lines[2:])
        subs.append((start, end, text))
    return subs


def _prepare_gameplay(gameplay_path: str, target_duration: float) -> VideoFileClip:
    """Gameplay videoni kerakli uzunlikka moslaydi (kesadi yoki qaytadan aylantiradi)."""
    clip = VideoFileClip(gameplay_path)
    if clip.duration >= target_duration:
        return clip.subclip(0, target_duration)
    # Video qisqa bo'lsa, uni takrorlab, kerakli uzunlikka yetkazamiz
    loops_needed = int(target_duration // clip.duration) + 1
    looped = concatenate_videoclips([clip] * loops_needed)
    return looped.subclip(0, target_duration)


def build_video(
    gameplay_path: str,
    narration_audio_path: str,
    subtitles_srt_path: str,
    output_path: str,
    resolution=(1080, 1920),  # standart: vertikal Shorts uchun. Gorizontal uchun (1920,1080)
):
    """Hammasini birlashtirib, tayyor mp4 videoni chiqaradi."""
    narration = AudioFileClip(narration_audio_path)
    gameplay = _prepare_gameplay(gameplay_path, narration.duration)
    gameplay = gameplay.resize(height=resolution[1]).set_audio(narration)

    subtitle_clips = []
    for start, end, text in _parse_srt(subtitles_srt_path):
        txt_clip = (
            TextClip(
                text,
                fontsize=54,
                color="white",
                stroke_color="black",
                stroke_width=2,
                method="caption",
                size=(resolution[0] * 0.85, None),
                font="DejaVu-Sans-Bold",
            )
            .set_start(start)
            .set_end(end)
            .set_position(("center", "bottom"))
        )
        subtitle_clips.append(txt_clip)

    final = CompositeVideoClip([gameplay, *subtitle_clips])
    final.write_videofile(
        output_path, fps=30, codec="libx264", audio_codec="aac", threads=4
    )
    return output_path


if __name__ == "__main__":
    build_video(
        gameplay_path="uploads/my_gameplay.mp4",
        narration_audio_path="output/narration.mp3",
        subtitles_srt_path="output/subtitles.srt",
        output_path="output/final_video.mp4",
    )
