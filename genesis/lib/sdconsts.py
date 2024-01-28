"""
"""
import os
import requests
from argparse import ArgumentParser
from lib import sdtemplates

DEFAULT_DYNAMIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "sd-dynamic-gen"))
TXT2IMG_URL = "http://192.168.1.234:7860/sdapi/v1/txt2img"

_SAMPLERS = [samp["name"] for samp in requests.get("http://192.168.1.234:7860/sdapi/v1/samplers").json()]
_UPSCALERS = [samp["name"] for samp in requests.get("http://192.168.1.234:7860/sdapi/v1/upscalers").json()]

STYLES = {
    "anime":sdtemplates.ANIME,
    "drawing":sdtemplates.DRAWING,
    "stylized":sdtemplates.STYLIZED,
    "photo":sdtemplates.PHOTO,
    "watercolor":sdtemplates.WATERCOLOR,
    "fantasy":sdtemplates.FANTASY
}

class ArgParseFixer(Exception):
    pass

class ArgumentJustParser(ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        try:
            return super().parse_args(args, namespace)
        except ArgParseFixer as e:
            return str(e)
    def print_help(self, file=None):
        raise ArgParseFixer(self.format_help())
    def error(self, message):
        raise ArgParseFixer("\n".join([self.format_usage(), f'{self.prog}: error: {message}']))
    def exit(self, status, message):
        raise ArgParseFixer("Unexpected error occurred. Congrats.")


ARGPARSER = ArgumentJustParser("Stable-Diffusion A1111 Image Generator")

ARGPARSER.add_argument("prompt", help="Full prompt. Like a unix shell, needs to be in \"quotes\". The add_detail lora is appended.")
ARGPARSER.add_argument("--neg-prompt", "-n", default="", help="Specify negative prompt. A default is appended.")

ARGPARSER.add_argument("--restore-faces", "-rf", action="store_true", default=False, help="Enables the Restore Faces process. Usually bad results.")
ARGPARSER.add_argument("--seed", type=int, default=-1, help="Specify seed. Useful for replication. **XFORMERS IS ACTIVE")
ARGPARSER.add_argument("--iter", "-i", type=int, default=1, dest="n_iter", help="Number of images to generate. 1-4")
ARGPARSER.add_argument("--steps", type=int, default=25, help="Number of sampling steps. Between 20-40 usually.")
ARGPARSER.add_argument("--cfg-scale", "-cfg", type=int, help="Classifier Free Guidance scale. usually between 3-15. Heuristically, determines how closely to the prompt the image must be generated. The SD version of top_p.")
ARGPARSER.add_argument("--sampler", choices=_SAMPLERS, dest="sampler_name", default="DPM++ 2M SDE Karras", help="Specify sampler. Esoteric mostly, but can affect how many steps needed to achieve decent image and how much variation per step.")

ARGPARSER.add_argument("--aspect-ratio", "-ar", choices=["p", "l", 's'], default=None, help="Specify aspect ratio. p for portrait, l for landscape, s for square. Overrides height and width settings.")
ARGPARSER.add_argument("--width", "-wi", type=int, help="Pixel height.")
ARGPARSER.add_argument("--height", "-hi", type=int, help="Pixel width.")

ARGPARSER.add_argument("--no-defaults", "-nd", action="store_true", default=False, help="Flag if you absolutely don't want the default positive/negative prompts.")
ARGPARSER.add_argument("--print-defaults", "-d", action="store_true", default=False, help="Flag to print the default positive/negative prompts. No image generation, other arguments are ignored.")

ARGPARSER.add_argument("--hires", "-hr", action="store_true", default=False, help="Enable Hi-Res fix. Doubles resolution and improves quality at the expense of processing time.")
ARGPARSER.add_argument("--denoising", "-dn", type=float, default=0.3, help="HR FIX - Denoising strength, between 0-1. The higher it is, the further away from the original.")
ARGPARSER.add_argument("--upscaler", "-us", choices=_UPSCALERS, default="8x_NMKD-Superscale_150000_G", help="HR FIX - Hires upscaler. Different sharpness results for different styles.")

ARGPARSER.add_argument("--style", "-s", choices=STYLES.keys(), default=None, help="Setting a style will pick a specific model and VAE. WARNING - Changing loaded model takes time.")

ARGPARSER.add_argument("--model", help="ADMIN - Exact model to use. You probably don't know.")
ARGPARSER.add_argument("--vae", help="ADMIN - Exact VAE to use. You probably don't know.")
ARGPARSER.add_argument("--clipskip", type=int, help="ADMIN - CLIP skip to use. You probably don't know.")


REQUEST_PAYLOAD = {
    "prompt": None,
    "negative_prompt": None,
    "seed": -1,
    "sampler_name": "DPM++ 2M SDE Karras",
    "n_iter": 1,
    "steps": 30,
    "cfg_scale": 3,
    "width": 1024,
    "height": 1024,
    "restore_faces": False,
    "override_settings":{}
}

HR_PAYLOAD = {
    "enable_hr": True,
    "denoising_strength": 0.3,
    "hr_scale": 2,
    "hr_upscaler": "8x_NMKD-Superscale_150000_G",
    "hr_second_pass_steps": 25,
    "hr_sampler_name": "DPM++ SDE Karras",
    "hr_prompt": "",
    "hr_negative_prompt": ""
}

VALID_OVERRIDE_SETTINGS = [
    "sd_model_checkpoint",
    "sd_vae",
    "CLIP_stop_at_last_layers"
]