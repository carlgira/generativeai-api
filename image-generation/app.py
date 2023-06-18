from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
from flask import Flask, request, jsonify, send_file
from io import BytesIO
import os

flask = Flask(__name__)

model_id = os.environ['HUGGINGFACEHUB_MODEL']
scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

@flask.route('/generate_image', methods=['POST'])
def generate_image():
    
    prompt = request.get_json()['prompt']
    image = pipe(prompt).images[0]  
    
    image.save("temp.png")
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    flask.run(host='0.0.0.0', port=3000)
