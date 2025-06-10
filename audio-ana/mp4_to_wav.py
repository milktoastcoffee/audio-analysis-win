import os
import sys
import subprocess

def convert_all_mp4_to_wav(input_dir):
    if not os.path.isdir(input_dir):
        print("❌ Error: Provided path is not a directory.")
        return

    output_dir = os.path.join(input_dir, "converted_wav")
    os.makedirs(output_dir, exist_ok=True)

    mp4_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.mp4')]

    if not mp4_files:
        print("❌ No MP4 files found.")
        return

    for file in mp4_files:
        input_path = os.path.join(input_dir, file)
        output_filename = os.path.splitext(file)[0] + ".wav"
        output_path = os.path.join(output_dir, output_filename)

        print(f"🎧 Converting: {file} → {output_filename}")

        try:
            # Use ffmpeg to extract audio without re-encoding
            subprocess.run([
                "ffmpeg",
                "-y",  # overwrite output if exists
                "-i", input_path,
                "-map", "0:a:0",     # map only the first audio stream
                "-c:a", "copy", # does not compress audio
                output_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        except subprocess.CalledProcessError:
            print(f"❌ Failed to convert: {file}")

    print(f"\n✅ All done! WAV files saved to: {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:\n  python batch_mp4_to_wav.py <directory_with_mp4_files>")
    else:
        convert_all_mp4_to_wav(sys.argv[1])
