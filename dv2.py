import os
import yt_dlp
import platform


def download_videos(url_file, output_directory):
    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Read the URLs from the text file
    with open(url_file, "r") as file:
        urls = file.readlines()

    # Download each video
    for url in urls:
        url = url.strip()
        try:
            ydl_opts = {
                "outtmpl": os.path.join(output_directory, "%(title)s.%(ext)s"),
                "format": "best",
                "noprogress": True,
                "nooverwrites": True,
                "merge_output_format": "mp4",
            }
            # Check if the video file already exists
            video_info = yt_dlp.YoutubeDL().extract_info(url, download=False)
            output_path = os.path.join(output_directory, f"{video_info['title']}.mp4")
            if os.path.exists(output_path):
                print(f"Already downloaded: {url}\n")
                continue

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"Downloaded: {url}\n")
        except yt_dlp.utils.DownloadError as e:
            print(f"Failed to download {url}: {e}\n")


if __name__ == "__main__":
    url_file = input("Enter the path to the text file containing video URLs: ")
    system_platform = platform.system().lower()
    default_directory = ""

    if system_platform == "darwin":  # macOS
        default_directory = os.path.join(os.path.expanduser("~"), "Desktop", "youtube")
    elif system_platform == "windows":
        default_directory = os.path.join(os.path.expanduser("~"), "Desktop", "youtube")

    use_default = (
        input(
            "Do you want to use the default output directory ({}): (yes/no) ".format(
                default_directory
            )
        )
        .strip()
        .lower()
    )
    if use_default == "yes":
        output_directory = default_directory
    else:
        output_directory = input("Enter the directory to save downloaded videos: ")

    download_videos(url_file, output_directory)
