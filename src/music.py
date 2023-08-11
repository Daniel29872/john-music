import os
import yaml
from youtube_search import YoutubeSearch


class MusicQueue:

    def __init__(self) -> None:
        self.queue = list()

        with open("./config.yaml") as file:
            self.downloads = yaml.safe_load(file)["downloads"]

        if not os.path.isdir(self.downloads):
            os.mkdir(self.downloads)
     

    def add_song(self, search_term: str):
        result = YoutubeSearch(search_terms=search_term, max_results=1).to_dict()[0]

        title = "".join(x if x.isalnum() else "_" for x in result["title"])
        url_suffix = result["url_suffix"].split("&")[0]  # work-around to avoid using perl
        url = "youtube.com" + url_suffix
        
        args = [
            "-x",
            f"-o {self.downloads}/{title}.%(ext)s",
            "--audio-format wav",
            "--no-mtime",
            "--no-playlist",
            "--no-warnings",
            f"--cache-dir {self.downloads}/cache",
        ]

        print(f"youtube-dl {' '.join(args)} {url}")
        status = os.system(f"youtube-dl {' '.join(args)} {url}")
        if status:
            raise RuntimeError(f"Download failed with exit code {status}.")
        
        for filename in os.listdir(self.downloads):
            if all(x in filename for x in title if x.isalpha()):
                self.queue.append(f"{self.downloads}/{filename}")
                break
        else:
            raise FileNotFoundError(f"Unable to retrieve downloaded audio file.")
