import logging
import re
from typing import Dict

from yt_dlp import YoutubeDL

from .plugin import Plugin


class YouTubeAudioExtractorPlugin(Plugin):
    """
    A plugin to extract audio from a YouTube video using yt-dlp
    """

    def get_source_name(self) -> str:
        return "YouTube Audio Extractor"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "extract_youtube_audio",
            "description": "Extract audio from a YouTube video",
            "parameters": {
                "type": "object",
                "properties": {
                    "youtube_link": {"type": "string", "description": "YouTube video link to extract audio from"}
                },
                "required": ["youtube_link"],
            },
        }]

    async def execute(self, function_name, helper, **kwargs) -> Dict:
        link = kwargs['youtube_link']
        try:
            # Normalize the URL
            clean_link = re.sub(r'&feature=.*', '', link)

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(clean_link, download=True)
                output = ydl.prepare_filename(info).replace('.webm', '.mp3')  # Adjust for mp3 file extension
                return {
                    'direct_result': {
                        'kind': 'file',
                        'format': 'path',
                        'value': output
                    }
                }
        except Exception as e:
            logging.warning(f'Failed to extract audio from YouTube video: {str(e)}')
            return {'result': 'Failed to extract audio'}
