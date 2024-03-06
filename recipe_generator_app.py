import uuid

from flask import Flask, jsonify, request
from transformers import FlaxAutoModelForSeq2SeqLM
from transformers import AutoTokenizer
from IPython.display import Image, display

import torch
import io
from PIL import Image
from base64 import encodebytes

import clip
import os.path as osp
import os, sys
import torchvision.utils as vutils
sys.path.insert(0, '../')
from GALIP_Sampling.code.lib.utils import load_model_weights,mkdir_p
from GALIP_Sampling.code.models.GALIP import NetG, CLIP_TXT_ENCODER

device = 'cpu' # 'cpu' # 'cuda:0'
CLIP_text = "ViT-B/32"
clip_model, preprocess = clip.load("ViT-B/32", device=device)
clip_model = clip_model.eval()

text_encoder = CLIP_TXT_ENCODER(clip_model).to(device)
netG = NetG(64, 100, 512, 256, 3, False, clip_model).to(device)
path = 'GALIP_Sampling/code/saved_models/pretrained/pre_cc12m.pth'
checkpoint = torch.load(path, map_location=torch.device('cpu'))
netG = load_model_weights(netG, checkpoint['model']['netG'], multi_gpus=False)

batch_size = 8
noise = torch.randn((batch_size, 100)).to(device)

MODEL_NAME_OR_PATH = "flax-community/t5-recipe-generation"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME_OR_PATH, use_fast=True)
model = FlaxAutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME_OR_PATH)

prefix = "items: "
# generation_kwargs = {
#     "max_length": 512,
#     "min_length": 64,
#     "no_repeat_ngram_size": 3,
#     "early_stopping": True,
#     "num_beams": 5,
#     "length_penalty": 1.5,
# }
generation_kwargs = {
    "max_length": 512,
    "min_length": 64,
    "no_repeat_ngram_size": 3,
    "do_sample": True,
    "top_k": 60,
    "top_p": 0.95
}

special_tokens = tokenizer.all_special_tokens
tokens_map = {
    "<sep>": "--",
    "<section>": "\n"
}


def skip_special_tokens(text, special_tokens):
    for token in special_tokens:
        text = text.replace(token, "")

    return text


def target_postprocessing(texts, special_tokens):
    if not isinstance(texts, list):
        texts = [texts]

    new_texts = []
    for text in texts:
        text = skip_special_tokens(text, special_tokens)

        for k, v in tokens_map.items():
            text = text.replace(k, v)

        new_texts.append(text)

    return new_texts


def generation_function(texts):
    _inputs = texts if isinstance(texts, list) else [texts]
    inputs = [prefix + inp for inp in _inputs]
    inputs = tokenizer(
        inputs,
        max_length=256,
        padding="max_length",
        truncation=True,
        return_tensors="jax"
    )

    input_ids = inputs.input_ids
    attention_mask = inputs.attention_mask

    output_ids = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        **generation_kwargs
    )
    generated = output_ids.sequences
    generated_recipe = target_postprocessing(
        tokenizer.batch_decode(generated, skip_special_tokens=False),
        special_tokens
    )
    return generated_recipe


app = Flask(__name__)


@app.route('/generate_recipe', methods=['GET'])
def get_recipe():
    items = request.args.getlist('ingredients')
    generated = generation_function(items)
    generated_recipe = {}
    for text in generated:
        sections = text.split("\n")
        for section in sections:
            section = section.strip()
            if section.startswith("title:"):
                section = section.replace("title:", "")
                headline = "TITLE"
            elif section.startswith("ingredients:"):
                section = section.replace("ingredients:", "")
                headline = "INGREDIENTS"
            elif section.startswith("directions:"):
                section = section.replace("directions:", "")
                headline = "DIRECTIONS"

            if headline == "TITLE":
                generated_recipe["title"] = section.strip().capitalize()
            elif headline == "INGREDIENTS":
                generated_recipe["ingredients"] = [f"  - {i + 1}: {info.strip().capitalize()}" for i, info in
                                enumerate(section.split("--"))]
            else:
                generated_recipe["directions"] = [f"  - {i + 1}: {info.strip().capitalize()}" for i, info in
                                enumerate(section.split("--"))]

            generated_recipe["id"] = uuid.uuid4().hex

    return jsonify(generated_recipe)


@app.route('/generate_recipe_and_image', methods=['GET'])
def get_recipe_and_image():
    items = request.args.getlist('ingredients')
    generated = generation_function(items)
    generated_recipe = {}
    for text in generated:
        sections = text.split("\n")
        for section in sections:
            section = section.strip()
            if section.startswith("title:"):
                section = section.replace("title:", "")
                headline = "TITLE"
            elif section.startswith("ingredients:"):
                section = section.replace("ingredients:", "")
                headline = "INGREDIENTS"
            elif section.startswith("directions:"):
                section = section.replace("directions:", "")
                headline = "DIRECTIONS"

            if headline == "TITLE":
                generated_recipe["title"] = section.strip().capitalize()
                captions = [generated_recipe["title"]]
            elif headline == "INGREDIENTS":
                generated_recipe["ingredients"] = [f"  - {i + 1}: {info.strip().capitalize()}" for i, info in
                                enumerate(section.split("--"))]
            else:
                generated_recipe["directions"] = [f"  - {i + 1}: {info.strip().capitalize()}" for i, info in
                                enumerate(section.split("--"))]

            generated_recipe["id"] = uuid.uuid4().hex
    with torch.no_grad():
        for i in range(len(captions)):
            caption = captions[i]
            tokenized_text = clip.tokenize([caption]).to(device)
            sent_emb, word_emb = text_encoder(tokenized_text)
            sent_emb = sent_emb.repeat(batch_size, 1)
            fake_imgs = netG(noise, sent_emb, eval=True).float()
            name = f'{captions[i].replace(" ", "-")}'
            vutils.save_image(fake_imgs.data, 'GALIP_Sampling/code/src/samples/%s.png' % (name), nrow=8, value_range=(-1, 1), normalize=True)
        pil_img = Image.open('GALIP_Sampling/code/src/samples/%s.png' % (name), mode='r')  # reads the PIL image
        byte_arr = io.BytesIO()
        pil_img.save(byte_arr, format='PNG')
        encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
        generated_recipe['image']=encoded_img
    return jsonify(generated_recipe)
    #return pil_img

if __name__ == '__main__':
    app.run()
