import os
import time
import subprocess
from text_to_speech import text_to_speech_file  # Gemini TTS function

# Function: Convert text to audio
def text_to_audio(folder):
    # Path to description text inside the folder
    desc_path = f"user_uploads/{folder}/desc.txt"
    
    # Check if desc.txt exists
    if not os.path.exists(desc_path):
        print(f"[ERROR] desc.txt not found in {folder}")
        return False

    # Read the text from desc.txt
    with open(desc_path) as f:
        text = f.read().strip()
    
    # If text is empty, skip
    if not text:
        print(f"[WARNING] desc.txt in {folder} is empty")
        return False

    # Generate audio.mp3 using Gemini TTS
    print(f"[TTA] Generating audio for folder: {folder}")
    text_to_speech_file(text, folder)
    return True

# Function: Create video reel from images + audio
def create_reels(folder):
    folder_path = f"user_uploads/{folder}"
    input_txt = os.path.join(folder_path, "input.txt")  # File listing images for ffmpeg
    audio_file = os.path.join(folder_path, "audio.mp3")  # Generated TTS audio

    # Check required files exist
    if not os.path.exists(input_txt):
        print(f"[ERROR] input.txt not found in {folder}")
        return False
    if not os.path.exists(audio_file):
        print(f"[ERROR] audio.mp3 not found in {folder}")
        return False

    # Path to save final MP4 reel
    output_file = os.path.abspath(f"static/reels/{folder}.mp4")
    os.makedirs("static/reels", exist_ok=True)

    # ffmpeg command to create vertical reel
    command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", "input.txt",
        "-i", "audio.mp3",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-r", "30",
        "-pix_fmt", "yuv420p",
        output_file
    ]

    print(f"[FFMPEG] Running ffmpeg for folder: {folder}")
    print(" ".join(command))

    # Run ffmpeg inside the folder containing input.txt & audio.mp3
    try:
        subprocess.run(command, check=True, cwd=folder_path)
        print(f"[SUCCESS] Reel created: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] ffmpeg failed for folder {folder}")
        print(e)
        return False
# Main loop: Monitor folders and process them
if __name__ == "__main__":
    while True:
        print("Processing Queue...........")
        
        # Ensure done.txt exists to track processed folders
        if not os.path.exists("done.txt"):
            open("done.txt", "w").close()

        # Read already processed folders
        with open("done.txt", "r") as f:
            done_folders = [line.strip() for line in f]

        # List all folders in uploads
        folders = os.listdir("user_uploads")
        for folder in folders:
            # Skip if already done
            if folder in done_folders:
                continue

            print(f"[INFO] Processing folder: {folder}")

            # Step 1: Generate audio from desc.txt
            audio_done = text_to_audio(folder)
            if not audio_done:
                print(f"[SKIP] Skipping folder {folder} due to audio error.")
                continue

            # Step 2: Generate MP4 reel from images + audio
            reel_done = create_reels(folder)
            if reel_done:
                # Mark folder as done
                with open("done.txt", "a") as f:
                    f.write(folder + "\n")
            else:
                print(f"[RETRY] Will retry folder {folder} in next loop.")

        print("[INFO] Waiting 4 seconds before next check...\n")
        time.sleep(4)
