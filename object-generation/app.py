from flask import Flask, request, jsonify, send_file
import torch
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import create_pan_cameras, decode_latent_images
from shap_e.util.notebooks import decode_latent_mesh
import random
import zipfile
from io import BytesIO
import os


flask = Flask(__name__)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

xm = load_model('transmitter', device=device)
model = load_model('text300M', device=device)
diffusion = diffusion_from_config(load_config('diffusion'))


@flask.route('/generate_3d_object', methods=['POST'])
def generate_3d_object():
    prompt = request.get_json()['prompt']
    return_type = request.get_json()['return_type']

    batch_size = 1
    guidance_scale = 15.0

    latents = sample_latents(
        batch_size=batch_size,
        model=model,
        diffusion=diffusion,
        guidance_scale=guidance_scale,
        model_kwargs=dict(texts=[prompt] * batch_size),
        clip_denoised=True,
        use_fp16=True,
        use_karras=True,
        karras_steps=64,
        sigma_min=1e-3,
        sigma_max=160,
        s_churn=0,
    )

    file_name = str(random.randint(1000, 10000))

    if return_type == 'zip' or return_type == 'gif':
        render_mode = 'nerf'
        size = 64
        cameras = create_pan_cameras(size, device)
        images = decode_latent_images(xm, latents[0], cameras, rendering_mode=render_mode)
        images[0].save(file_name + '.gif',
                    save_all=True, append_images=images[1:], optimize=False, duration=3, loop=0)

    if return_type != 'gif':
        t = decode_latent_mesh(xm, latents[0]).tri_mesh()
        if return_type == 'zip' or return_type == 'obj':
            with open(file_name + '.obj', 'w') as f:
                t.write_obj(f)

    if return_type == 'zip':
        list_files = [file_name + '.gif', file_name + '.obj']
        with zipfile.ZipFile(file_name + '.zip', 'w') as zipMe:
            for file in list_files:
                zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)

    return_data = BytesIO()

    with open(file_name + '.' + return_type, 'rb') as fo:
        return_data.write(fo.read())

    return_data.seek(0)

    mime_type = {'gif': 'image/gif', 'zip': 'application/zip',
                 'obj': 'text/plain'}

    for ext in mime_type.keys():
        if os.path.exists(file_name + '.' + ext):
            os.remove(file_name + '.' + ext)

    return send_file(return_data, mimetype=mime_type[return_type])

if __name__ == '__main__':
    flask.run(host='0.0.0.0', port=3000)