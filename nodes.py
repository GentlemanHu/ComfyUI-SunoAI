import os
import datetime
from .suno.suno import *

# Assuming folder_paths module with get_save_image_path function is available
import folder_paths 

class SunoAIGenerator:

    def __init__(self):
        self.suno_client = Suno()
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'suno_ai_songs')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Enter your song idea here"}),
                "custom": ("BOOLEAN", {"default": False}),
                "tags": ("STRING", {"default": ""}),
                "instrumental": ("BOOLEAN", {"default": True}),
                "filename_prefix": ("STRING", {"default": "SunoAI_"}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("MP3 URL 1", "MP3 URL 2", "Local Path 1", "Local Path 2")
    FUNCTION = "generate_songs"
    OUTPUT_NODE = True
    CATEGORY = "Gentle_SunoAI"

    def generate_songs(self, prompt, custom, tags, instrumental,filename_prefix):
        try:
            generated_songs = self.suno_client.songs.generate(
                prompt, custom, tags, instrumental
            )

            # if len(generated_songs) < 2:
            #     raise Exception("Suno API returned less than 2 songs.")

            song1, song2 = generated_songs[:2]
            url1, url2 = song1.audio_url, song2.audio_url

            # Get output path information
            full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
            _datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            custom_suffix = "_sunoai"  # Use "_sunoai" suffix

            # Download and rename songs
            audio_paths = {}  # Dictionary to store audio paths

            for i, song in enumerate([song1, song2]):
                file = f"{filename}_{_datetime}_{custom_suffix}_{i+1}.mp3"
                audio_path = os.path.join(full_output_folder, file) 

                download(song, root=full_output_folder, name=file)
                audio_paths[song.id] = audio_path  # Store path with song ID as key

            # ... rest of your code

            return url1, url2, audio_paths[song1.id], audio_paths[song2.id]

        except Exception as e:
            print(f"Error generating songs: {e}")
            return "", "", "", ""




class SunoAIGeneratorNotSafe:

    def __init__(self):
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'suno_ai_songs')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Enter your song idea here"}),
                "custom": ("BOOLEAN", {"default": False}),
                "tags": ("STRING", {"default": ""}),
                "instrumental": ("BOOLEAN", {"default": True}),
                "filename_prefix": ("STRING", {"default": "SunoAI_"}),
                "suno_cookie":("STRING", {"multiline": True,}),
            },
            "optional": {},
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("MP3 URL 1", "MP3 URL 2", "Local Path 1", "Local Path 2")
    FUNCTION = "generate_songs"
    OUTPUT_NODE = True
    CATEGORY = "Gentle_SunoAI"

    def generate_songs(self, prompt, custom, tags, instrumental,filename_prefix,suno_cookie):
        try:
            suno_client = Suno(cookie=suno_cookie)
            generated_songs = suno_client.songs.generate(
                prompt, custom, tags, instrumental
            )

            # if len(generated_songs) < 2:
            #     raise Exception("Suno API returned less than 2 songs.")

            song1, song2 = generated_songs[:2]
            url1, url2 = song1.audio_url, song2.audio_url

            # Get output path information
            full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
            _datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            custom_suffix = "_sunoai"  # Use "_sunoai" suffix

# Download and rename songs
            audio_paths = {}  # Dictionary to store audio paths

            for i, song in enumerate([song1, song2]):
                file = f"{filename}_{_datetime}_{custom_suffix}_{i+1}.mp3"
                audio_path = os.path.join(full_output_folder, file) 

                download(song, root=full_output_folder, name=file)
                audio_paths[song.id] = audio_path  # Store path with song ID as key

            # ... rest of your code

            return url1, url2, audio_paths[song1.id], audio_paths[song2.id]

        except Exception as e:
            print(f"Error generating songs: {e}")
            return "", "", "", ""



NODE_CLASS_MAPPINGS = {
    "GentlemanHu_SunoAI": SunoAIGenerator,
    "GentlemanHu_SunoAI_NotSafe" :SunoAIGeneratorNotSafe
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GentlemanHu_SunoAI": "SunoAIGenerator",
    "GentlemanHu_SunoAI_NotSafe":"SunoAIGeneratorNotSafe"
}
