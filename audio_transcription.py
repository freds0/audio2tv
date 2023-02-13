import json
import requests
import urllib.request
import time
import glob
import os
import argparse

#pasta com músicas
path = 'audio/*'

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

def get_transcription_from_audios_folder(audio_filepath, output_dir):
    musicas = glob.glob(audio_filepath)
    nomes = [os.path.basename(x) for x in glob.glob(path)]
    #pasta de saída
    saida = output_dir

    #ID de usuário
    id = "MOISES_API_ID"

    for musica in musicas:
        # Pega link para upload temporário
        url = "https://developer-api.moises.ai/api/upload"
        
        # Colocar ID de quem for usar 
        headers = {"Authorization": id}
        upload_response = requests.request("GET", url, headers=headers)

        # Faz upload
        url = upload_response.json()['uploadUrl']
        headers = {"content-type": "multipart/form-data"}
        response = requests.request("PUT", url, data=open(musica, 'rb'), headers=headers)

        # Cria Job
        url = "https://developer-api.moises.ai/api/job"
        payload = {
            "name": nomes[0],
            "workflow": "extract_lyrics",
            "params": {"inputUrl": upload_response.json()['downloadUrl']}
        }
        headers = {
            "Authorization": "MOISES_API_ID",
            "Content-Type": "application/json"
        }
        job_response = requests.request("POST", url, json=payload, headers=headers)

        print('SUCESSO: ', musica)

        while True:
            url = "https://developer-api.moises.ai/api/job/" + job_response.json()['id']
            headers = {"Authorization": "MOISES_API_ID"}
            status_response = requests.request("GET", url, headers=headers)

            if status_response.json()['status'] == 'SUCCEEDED':
                break
            elif status_response.json()['status'] == 'FAILED':
                print("FALHA")
                break 
            else:
                time.sleep(1)
        
        try:
            # Pega resultado
            url = "https://developer-api.moises.ai/api/job/" + job_response.json()['id']
            headers = {"Authorization": "MOISES_API_ID"}
            result_response = requests.request("GET", url, headers=headers)
            transcriptions_link = result_response.json()['result']['Transcription']

            output_filepath = os.path.join(saida, nomes[0] + '.json')

            urllib.request.urlretrieve(result_response.json()['result']['Transcription'], output_filepath)

        except: continue

    return read_json_file(output_filepath)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base_dir', default='./')
    parser.add_argument('-o', '--output_folder', default='transcription/')
    parser.add_argument('-i', '--audio_input', default='audio/audio.mp3')
    args = parser.parse_args()

    input_dir=os.path.join(args.base_dir, args.audio_input)
    output_folder=os.path.join(args.base_dir, args.output_folder)
    get_transcription_from_audios_folder(audio_path=input_dir, output_dir=output_folder)


if __name__ == "__main__":
    main()
