import os
import sys
import subprocess

def convert_all_mp4_to_wav(input_dir):
    if not os.path.isdir(input_dir):
        print("❌ Error: Provided path is not a directory.")
        sys.exit(1)

    output_dir = os.path.join(input_dir, "converted_wav")
    os.makedirs(output_dir, exist_ok=True)

    mp4_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.mp4')]

    if not mp4_files:
        print("❌ No MP4 files found.")
        sys.exit(1)

    for file in mp4_files:
        input_path = os.path.join(input_dir, file)
        output_filename = os.path.splitext(file)[0] + ".wav"
        output_path = os.path.join(output_dir, output_filename)

        print(f"🎧 Converting: {file} → {output_filename}")

        try:
            subprocess.run([
                "ffmpeg",
                "-y",
                "-i", input_path,
                "-vn",
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                output_path
            ], check=True)
        
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to convert {file}")
            continue
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user. Exiting cleanly.")
            sys.exit(130)
        except Exception as e:
            print(f"❌ Unexpected error with {file}: {e}")
            continue

    print(f"\n✅ All done! WAV files saved to: {output_dir}")
    sys.exit(0)  # Clean exit

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print("Usage:\n  python batch_mp4_to_wav.py <directory_with_mp4_files>")
            sys.exit(1)
        convert_all_mp4_to_wav(sys.argv[1])
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user during directory validation.")
        sys.exit(130)
