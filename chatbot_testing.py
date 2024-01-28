# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("databricks/dolly-v2-3b")
model = AutoModelForCausalLM.from_pretrained("databricks/dolly-v2-3b")

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
    generated_text = target_postprocessing(
        tokenizer.batch_decode(generated, skip_special_tokens=False),
        special_tokens
    )
    return generated_text

if __name__ == "__main__":
    while True:
        print("Insert a nutrition/health related question: \n")
        prompt = input()
        inputs = tokenizer(prompt, return_tensors="pt")
        generate_ids = model.generate(inputs.input_ids, max_length=30)
        response = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        print(response)
        # for text in generated:
        #     sections = text.split("\n")
        #     for section in sections:
        #         section = section.strip()
        #         if section.startswith("title:"):
        #             section = section.replace("title:", "")
        #             headline = "TITLE"
        #         elif section.startswith("ingredients:"):
        #             section = section.replace("ingredients:", "")
        #             headline = "INGREDIENTS"
        #         elif section.startswith("directions:"):
        #             section = section.replace("directions:", "")
        #             headline = "DIRECTIONS"
#
        #         if headline == "TITLE":
        #             print(f"[{headline}]: {section.strip().capitalize()}")
        #         else:
        #             section_info = [f"  - {i + 1}: {info.strip().capitalize()}" for i, info in
        #                             enumerate(section.split("--"))]
        #             print(f"[{headline}]:")
        #             print("\n".join(section_info))
#
        #     print("-" * 130)