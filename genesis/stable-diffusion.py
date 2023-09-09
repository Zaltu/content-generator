import os
import io
import re
import base64
import random
import requests
from PIL import Image
from glob import glob
from pprint import pprint as pp

DEFAULT_DYNAMIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "sd-dynamic-gen"))
TXT2IMG_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"


PATTERN = """
{prompt}

<lora:add_detail:1>
"""

NEG_PATTERN = """
(worst quality, low quality:1.3), simple background, logo, watermark, text, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, bad-hands-5, bad-image-v2-39000, bad_prompt_version2, bad_quality, easynegative, ng_deepnegative_v1_75t, BadDream, UnrealisticDream, black and white, (closeup shot), GS-DeMasculate-neg, solo, umbrella
"""

REQUEST_PAYLOAD = {
    "prompt": "",
    "negative_prompt": "",
    "seed": -1,
    "sampler_name": "DPM++ SDE Karras",
    "n_iter": 1,
    "steps": 25,
    "cfg_scale": 7,
    "width": 512,
    "height": 512,
    "restore_faces": False
}

HR_PAYLOAD = {
    "enable_hr": True,
    "denoising_strength": 0.35,
    "hr_scale": 2,
    "hr_upscaler": "8x_NMKD-Superscale_150000_G",
    "hr_second_pass_steps": 20,
    "hr_sampler_name": "DPM++ SDE Karras",
    "hr_prompt": "",
    "hr_negative_prompt": ""
}

def __getPayload(prompt, neg_prompt, hr_fix=False):
    """
    """
    thisPro = REQUEST_PAYLOAD.copy()
    thisPro["prompt"] = prompt
    thisPro["negative_prompt"] = neg_prompt
    if hr_fix:
        thisHR = HR_PAYLOAD.copy()
        thisHR["hr_prompt"] = prompt
        thisHR["hr_negative_prompt"] = neg_prompt
        thisPro.update(thisHR)
    return thisPro


def _call_web_api(prompt, neg_prompt, hr_fix=False):
    """
    """
    payload = __getPayload(prompt, neg_prompt, hr_fix)
    gotbits = requests.post(TXT2IMG_URL, json=payload).json()
    n=1
    for i in gotbits['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        image.save(f"output{n}.png")
        n+=1


def generate_sd_image(prompt):
    """
    """
    _call_web_api(prompt, NEG_PATTERN)


if __name__ == "__main__":
    generate_sd_image("Black rock shooter")