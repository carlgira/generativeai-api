from flask import Flask, request, jsonify, send_file
from audiocraft.models import musicgen
from audiocraft.data.audio import audio_write
import torch
import random
from io import BytesIO
import os


flask = Flask(__name__)

model = musicgen.MusicGen.get_pretrained('small', device='cuda')
model.set_generation_params(duration=8)


@flask.route('/generate_music', methods=['POST'])
def generate_music():
    prompt = request.get_json()['prompt']
    duration = request.get_json()['duration']
      
    model.set_generation_params(duration=duration)
    
    wav = model.generate(prompt)
    
    file_name =  str(random.randint(1000, 10000))
    audio_write(file_name, wav[0].cpu(), model.sample_rate, strategy="loudness")
    
    
    return_data = BytesIO()
    
    
    with open(file_name + '.wav', 'rb') as fo:
        return_data.write(fo.read())
    
    return_data.seek(0)

    os.remove(file_name + '.wav')

    return send_file(return_data, mimetype='audio/x-wav')

if __name__ == '__main__':
    flask.run(host='0.0.0.0', port=3000)
