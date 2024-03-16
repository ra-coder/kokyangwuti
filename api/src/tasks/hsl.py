import os

import ffmpeg

from ..config import celery

__all__ = [
    'hsl'
]

RESOLUTIONS = [
    (1920, 1080, '5000', '192k'),
    (1280, 720, '2800', '128k'),
    (854, 480, '1400', '128k'),
    (640, 360, '800', '96k'),
]


def analyze_video(input_video):
    """Анализирует исходное видео и возвращает его характеристики."""
    try:
        probe = ffmpeg.probe(input_video)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream is None:
            print("Видеопоток не найден.")
            return None, None
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        return width, height

    except ffmpeg.Error as e:
        return None, None


def convert_to_hls(input_video, output_dir, resolutions, crf=20, preset='medium'):
    original_width, original_height = analyze_video(input_video)
    if not os.path.exists(input_video):
        raise FileNotFoundError(f"Input video '{input_video}' not found.")

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    for width, height, bitrate, audio_bitrate in resolutions:
        output_path = f"{output_dir}/{height}p.m3u8"
        (
            ffmpeg
            .input(input_video)
            .filter('scale', size=f'{width}x{height}', force_original_aspect_ratio='decrease')
            .filter('pad', width='ceil(iw/2)*2', height='ceil(ih/2)*2')
            .output(output_path,
                    acodec='aac', ar='48000', ac='2',
                    vcodec='libx264', crf=crf, preset=preset,
                    video_bitrate=bitrate + 'k',
                    audio_bitrate=audio_bitrate,
                    format='hls', hls_time=4, hls_playlist_type='vod')
            .run(capture_stdout=True, capture_stderr=True)
        )


def create_master_playlist(output_dir, resolutions):
    master_playlist_path = f"{output_dir}/master_playlist.m3u8"
    with open(master_playlist_path, 'w') as m3u8_file:
        m3u8_file.write('#EXTM3U\n')
        for _, height, _, _ in resolutions:
            m3u8_file.write(f'#EXT-X-STREAM-INF:BANDWIDTH={int(height) * 1000},RESOLUTION={height}p\n{height}p.m3u8\n')


@celery.task()
def hsl(input_video, output_dir):
    convert_to_hls(input_video, output_dir, RESOLUTIONS)
    create_master_playlist(output_dir, RESOLUTIONS)
