from flask import Flask, request, jsonify, send_file
from io import BytesIO
from subprocess import getoutput
import os


flask = Flask(__name__)

@flask.route('/generate_video', methods=['POST'])
def generate_video():
    prompt = request.get_json()['prompt']
    negative_prompt = request.get_json()['negative_prompt']
    width = request.get_json()['width']
    height = request.get_json()['height']
    num_steps = request.get_json()['num_steps']
    guidance_scale = request.get_json()['guidance_scale']
    fps = request.get_json()['fps']
    num_frames = request.get_json()['num_frames']
    
    response = getoutput("python Text-To-Video-Finetuning/inference.py -m \"potat1\" -p \"{prompt}\" -n \"{negative_prompt}\" -W {width} -H {height} -o outputs -d cuda -x -s {num_steps} -g {guidance_scale} -f {fps} -T {num_frames}".format(prompt=prompt, negative_prompt=negative_prompt, width=width, height=height, num_steps=num_steps, guidance_scale=guidance_scale, fps=fps, num_frames=num_frames))
    
    
    files = [f for f in os.listdir("outputs") if f.endswith(".mp4")]
    file_name = None
    if len(files) > 0:
        file_name = "outputs/"+files[0]
    else:
        return jsonify({'error': 'Video creation failed. Make sure your prompt is appropriate.'})
        
    
    return_data = BytesIO()
    
    
    with open(file_name, 'rb') as fo:
        return_data.write(fo.read())
    
    return_data.seek(0)

    os.remove(file_name)

    return send_file(return_data, mimetype='video/mp4')

if __name__ == '__main__':
    flask.run(host='0.0.0.0', port=3000)
