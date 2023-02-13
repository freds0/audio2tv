import os
import argparse
from create_video_from_prompt import get_video_from_prompt
from audio_transcription import get_transcription_from_audios_folder
from prompt_from_transcription import get_prompt_from_transcription


def execute_pipeline(input_audio_filepath):

    print("Executing get_transcription..." )
    os.makedirs('transcription/', exist_ok=True)
    transcription = get_transcription_from_audios_folder(input_audio_filepath, output_dir='transcription/')

    print("Executing get_prompt..." )
    os.makedirs('prompt/', exist_ok=True)
    prompt = get_prompt_from_transcription(transcription, 'prompt/')

    print("Executing video_generation..." )
    get_video_from_prompt(text_prompts=prompt, audio_filepath=input_audio_filepath)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base_dir', default='./')
    parser.add_argument('-i', '--input_file', default='audio/audio.mp3')
    args = parser.parse_args()

    input_file=os.path.join(args.base_dir, args.input_file)

    execute_pipeline(input_file)


if __name__ == "__main__":
    main()

