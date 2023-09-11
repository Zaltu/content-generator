
import os
from argparse import ArgumentParser
from typing import NoReturn

DEFAULT_DYNAMIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "sd-dynamic-gen"))
TXT2IMG_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"

_SAMPLERS = [
    "DPM++ SDE Karras",
    "DPM++ 2M Karras",
    "DPM++ 3M SDE Karras",
    "Euler",
    "UniPC",
    "DDIM"
]
_UPSCALERS = [
    "8x_NMKD-Superscale_150000_G",
    "4x-UltraSharp",
    "4x_fatal_Anime_500000_G",
    "Remacri Upscaler",
    "Latent"
]
_STYLES = {
    "anime":("abyssorangemix3AOM3_aom3a1b", "orangemix.vae.pt"),
    "drawing":("revAnimated_v122", "vae-ft-mse-840000-ema-pruned.ckpt"),
    "stylized":("pastelMixStylizedAnime_pastelMixFull", "pastel-waifu-diffusion.vae.pt"),
    "photo":("photon_v1", "orangemix.vae.pt"),
    "watercolor":("threeDelicacyWonton_sanxianwontonmixv1", "vae-ft-mse-840000-ema-pruned.ckpt"),
    "fantasy":("aZovyaRPGArtistTools_v3", "vae-ft-mse-840000-ema-pruned.ckpt")
}

PATTERN = """{prompt}

<lora:add_detail:1>
"""

NEG_PATTERN = """{neg_prompt}

(worst quality, low quality:1.3), simple background, logo, watermark, text, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, bad-hands-5, bad-image-v2-39000, bad_prompt_version2, bad_quality, easynegative, ng_deepnegative_v1_75t, BadDream, UnrealisticDream, black and white, (closeup shot)
"""

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
    def exit(self, status: int = 0, message: str | None = None) -> NoReturn:
        raise ArgParseFixer("Unexpected error occurred. Congrats.")


ARGPARSER = ArgumentJustParser("Stable-Diffusion A1111 Image Generator")

ARGPARSER.add_argument("prompt", help="Full prompt. Like a unix shell, needs to be in \"quotes\". The add_detail lora is appended.")
ARGPARSER.add_argument("--neg-prompt", "-n", default="", help="Specify negative prompt. A default is appended.")

ARGPARSER.add_argument("--restore-faces", "-rf", action="store_true", default=False, help="Enables the Restore Faces process. Usually bad results.")
ARGPARSER.add_argument("--seed", type=int, default=-1, help="Specify seed. Useful for replication. **XFORMERS IS ACTIVE")
ARGPARSER.add_argument("--iter", "-i", type=int, default=1, help="Number of images to generate. 1-4")
ARGPARSER.add_argument("--steps", type=int, default=25, help="Number of sampling steps. Between 20-40 usually.")
ARGPARSER.add_argument("--cfg-scale", "-cfg", type=int, default=-7, help="Classifier Free Guidance scale. usually between 5-15. Heuristically, determines how closely to the prompt the image must be generated. The SD version of top_p.")
ARGPARSER.add_argument("--sampler", choices=_SAMPLERS, default="DPM++ SDE Karras", help="Specify sampler. Esoteric mostly, but can affect how many steps needed to achieve decent image and how much variation per step.")

ARGPARSER.add_argument("--aspect-ratio", "-ar", choices=["p", "l", 's'], default=None, help="Specify aspect ratio. p for portrait, l for landscape, s for square. Overrides height and width settings.")
ARGPARSER.add_argument("--width", "-w", type=int, default=512, help="Pixel height.")
ARGPARSER.add_argument("--height", "-hi", type=int, default=512, help="Pixel width.")

ARGPARSER.add_argument("--no-defaults", "-nd", action="store_true", default=False, help="Flag if you absolutely don't want the default positive/negative prompts.")
ARGPARSER.add_argument("--print-defaults", "-d", action="store_true", default=False, help="Flag to print the default positive/negative prompts. No image generation, other arguments are ignored.")

ARGPARSER.add_argument("--hires", "-hr", action="store_true", default=False, help="Enable Hi-Res fix. Doubles resolution and improves quality at the expense of processing time.")
ARGPARSER.add_argument("--denoising", "-dn", type=float, default=0.35, help="HR FIX - Denoising strength, between 0-1. The higher it is, the further away from the original.")
ARGPARSER.add_argument("--upscaler", "-us", choices=_UPSCALERS, default="8x_NMKD-Superscale_150000_G", help="HR FIX - Hires upscaler. Different sharpness results for different styles.")

ARGPARSER.add_argument("--style", "-s", choices=_STYLES.keys(), default=None, help="Setting a style will pick a specific model and VAE. WARNING - Changing loaded model takes time.")

ARGPARSER.add_argument("--model", default=None, help="ADMIN - Exact model to use. You probably don't know.")
ARGPARSER.add_argument("--vae", default=None, help="ADMIN - Exact VAE to use. You probably don't know.")
ARGPARSER.add_argument("--clipskip", type=int, help="ADMIN - CLIP skip to use. You probably don't know.")


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
    "hr_second_pass_steps": 25,
    "hr_sampler_name": "DPM++ SDE Karras",
    "hr_prompt": "",
    "hr_negative_prompt": ""
}
