# Python program to read
# json file
import argparse
import torch
import librosa
from stable_diffusion_videos import StableDiffusionWalkPipeline
import json
import math

def read_json_file(json_filepath):

    # Opening JSON file
    f = open(json_filepath)
      
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
      
    # Iterating through the json
    # list
    text_prompts = []
    for i in data:
        print(i['text'])
        text_prompts.append(i['text'])
      
    # Closing file
    f.close()

    return text_prompts



def read_txt_file(txt_filepath):

    with open(txt_filepath) as f:
        content = f.readlines()[0]
    text_prompts = content.split(".")
    print(text_prompts)
    return text_prompts


def get_video_from_prompt(text_prompts, audio_filepath='audio/audio.mp3'):
 
    pipeline = StableDiffusionWalkPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        torch_dtype=torch.float16,
        revision="fp16",
    ).to("cuda")

    y, sr = librosa.load(audio_filepath)
    duration = librosa.get_duration(y=y, sr=sr)

    # Seconds in the song
    audio_offsets = [0, int(math.ceil(duration))]
    fps = 2

    # Convert seconds to frames
    num_interpolation_steps = [(b-a) * fps for a, b in zip(audio_offsets, audio_offsets[1:])]

    

    video_path = pipeline.walk(
        prompts=text_prompts,
        seeds=[42, 1337],
        num_interpolation_steps=num_interpolation_steps,
        audio_filepath=audio_filepath,
        audio_start_sec=audio_offsets[0],
        height=512,                            # use multiples of 64
        width=512,                             # use multiples of 64
        fps=fps,                               # important to set yourself based on the num_interpolation_steps you defined
        batch_size=1,                          # increase until you go out of memory.
        output_dir='./dreams',                 # Where images will be saved
        name=None,                             # Subdir of output dir. will be timestamp by default
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base_dir', default='./')
    parser.add_argument('-i', '--prompt_input', default='prompt/prompt.txt')
    parser.add_argument('-a', '--audio_input', default='audio/audio.mp3')
    args = parser.parse_args()
    
    input_filepath = os.path.join(args.base_dir, args.prompt_input)

    text_prompts = read_txt_file(input_filepath)
    get_video_from_prompt(text_prompts=text_prompts, audio_filepath=args.audio_input)


if __name__ == "__main__":
    main()


