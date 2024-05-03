import os
import logging
import replicate
from PIL import Image
import urllib.request
from io import BytesIO 
from qmenzi import config

logger = logging.getLogger("qmenzi-quizzes-ideogram")

AUTH_TOKEN = config('replicate.api_token')


class ReplicateModel():
        
        def __init__(self, model_name):
             self.model_name = model_name
             self.input = {}

        def __authenticate(self):
            os.environ['REPLICATE_API_TOKEN'] = AUTH_TOKEN

        def set_input(self, input):
            self.input.update(input)

        def _run_model(self):
            self.__authenticate()
            return replicate.run(self.model_name, input = self.input)


class StabilityAI_SDXL(ReplicateModel):

        def __init__(self, 
                     width = 768,
                     height = 768,
                     refine = 'expert_ensemble_refiner',
                     scheduler = 'K_EULER',
                     lora_scale = 0.6,
                     num_outputs = 1,
                     guidance_scale = 7.5,
                     high_noise_frac = 0.8,
                     negative_prompt = "",
                     prompt_strength = 0.8,
                     num_inference_steps = 25
                     ):
               super().__init__('stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b')
               self.set_input({
                     'width': width,
                     'height': height,
                     'refine': refine,
                     'scheduler': scheduler,
                     'lora_scale': lora_scale,
                     'num_outputs': num_outputs,
                     'guidance_scale': guidance_scale,
                     'high_noise_frac': high_noise_frac,
                     'negative_prompt': negative_prompt,
                     'prompt_strength': prompt_strength,
                     'num_inference_steps': num_inference_steps
                     })
               
        def render_image(self, prompt):
            self.set_input({'prompt': prompt})
            return self._run_model()
            
        def get_image(self, url):
            with urllib.request.urlopen(url) as u:
                 return Image.open(BytesIO(u.read()))
