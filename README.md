# 496_CookBuddyProject
This part of the project is mostly used for testing end searching purposes. The architecture is composed of the following modules:

GALIP_sampling -> This part is for text to image generation, image is returned as bytearray to get response. To use pretrained generator models you should download pretrained models:
  GALIP for COCO. Download and save it to ./code/saved_models/pretrained/
  GALIP for CC12M. Download and save it to ./code/saved_models/pretrained/
Use GALIP_Sampling/code/src/sample.ipynb to create see images as displayed in notebook.

recipe_generator_app.py -> Flask App (Used as an endpoint for querying the flax-community/t5-recipe-generation LLM)

The works under the LLMPractice directory are first trys of LLM implementations.
