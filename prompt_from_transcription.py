import openai
import torch
import json
import os
import argparse
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

API_KEY = "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"

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
        #print(i['text'])
        text_prompts.append(i['text'])
      
    # Closing file
    f.close()

    return text_prompts


def get_prompt_from_transcription(lyrics, output_prompt):


    # Define OpenAI API key 
    openai.api_key = API_KEY

    # Set up the model and prompt
    model_engine = "text-davinci-003"
    # prompt = "I want you to act as an illustrator. I will provide you with the lyrics song. Your goal is to create json file with a creative and captivating five frames continuous description that representing this song in a video. Start with describing the ambient, ilumination and details. My First request is  'I'm tired of being what you want me to be Feeling so faithless, lost under the surface Don't know what you're expecting of me Put under the pressure of walking in your shoes'"



    # ESTA OK
    # prompt = "I want you to act as an artist. I will provide you with the music name. Your goal is to describe a creative and captivating frames continuous description that representing this song in a video. Start with describing the ambient, ilumination and details. My First request is  'viva la vida coldplay'"
    prompt = "I want you to act as an artist. I will provide you with the lyrics song. Your goal is to describe a creative and captivating frames continuous description that representing this song in a video. Start with describing the ambient, ilumination and details. My First request is: '{}'".format(lyrics)


    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    output = completion.choices[0].text
    # output = json.loads(output)

    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base_dir', default='./')
    parser.add_argument('-o', '--output_folder', default='prompt/')
    parser.add_argument('-i', '--input_transcription', default='transcription/audio.mp3.json')
    args = parser.parse_args()

    input_file=os.path.join(args.base_dir, args.input_transcription)

    lyrics_content = read_json_file(input_file)

    output_folder=os.path.join(args.base_dir, args.output_folder)
    get_prompt_from_transcription(lyrics_content, output_folder)


if __name__ == "__main__":
    main()

