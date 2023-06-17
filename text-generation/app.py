from flask import Flask, request, jsonify, send_file
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

flask = Flask(__name__)

model = "tiiuae/falcon-7b"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
)

@flask.route('/generate_text', methods=['POST'])
def generate_text():
    prompt = request.get_json()['prompt']
    max_length = request.get_json()['max_length']
      
    
    sequences = pipeline(
        prompt,
        max_length=max_length,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
    )
        
    return jsonify({"response": sequences[0]['generated_text']})

if __name__ == '__main__':
    flask.run(host='0.0.0.0', port=3000)
