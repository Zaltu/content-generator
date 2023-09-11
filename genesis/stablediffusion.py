import os
import io
import shlex
import base64
import requests
from PIL import Image
from lib import sdconsts as cnt


def __getPayload(args):
    """
    """
    thisPro = cnt.REQUEST_PAYLOAD.copy()
    thisPro["prompt"] = cnt.PATTERN.format(prompt=args.prompt)
    thisPro["negative_prompt"] = cnt.NEG_PATTERN.format(neg_prompt=args.neg_prompt)
    thisPro["seed"]: args.seed
    thisPro["sampler_name"]: args.sampler
    thisPro["n_iter"]: args.iter
    thisPro["steps"]: args.steps
    thisPro["cfg_scale"]: args.cfg_scale
    thisPro["restore_faces"]: args.restore_faces
    if args.aspect_ratio:
        match args.aspect_ratio:
            case 's':
                thisPro["width"] = 512
                thisPro["height"] = 512
            case 'p':
                thisPro["width"] = 600
                thisPro["height"] = 752
            case 'l':
                thisPro["width"] = 960
                thisPro["height"] = 540
    else:
        thisPro["width"] = args.width
        thisPro["height"] = args.height
    
    if args.hires:
        thisHR = cnt.HR_PAYLOAD.copy()
        thisHR["hr_prompt"] = cnt.PATTERN.format(prompt=args.prompt)
        thisHR["hr_negative_prompt"] = cnt.NEG_PATTERN.format(neg_prompt=args.neg_prompt)
        thisHR["denoising_strength"] = args.denoising
        thisHR["hr_upscaler"] = args.upscaler
        thisHR["hr_second_pass_steps"]: args.steps
        thisPro.update(thisHR)
    
    if args.style:
        args.model = cnt._STYLES[args.style][0]
        args.vae = cnt._STYLES[args.style][1]

    if args.model or args.vae or args.clipskip:
        thisPro["override_settings"] = {}
        if args.model:
            thisPro["override_settings"]["sd_model_checkpoint"] = args.model
        if args.vae:
            thisPro["override_settings"]["sd_vae"] = args.vae
        if args.clipskip:
            thisPro["override_settings"]["CLIP_stop_at_last_layers"] = args.clipskip
    return thisPro


def _call_web_api(payload, saveto=""):
    """
    """
    gotbits = requests.post(cnt.TXT2IMG_URL, json=payload).json()
    files = []
    n=1
    for i in gotbits['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        image.save(os.path.join(saveto, f"output{n}.png"))
        files.append(os.path.join(saveto, f"output{n}.png"))
        n+=1
    return files


def generate_sd_image_simple(prompt, hr_fix=False, saveto=""):
    """
    """
    fauxcommand = [prompt]
    if hr_fix:
        fauxcommand.append("-hr")
    args = cnt.ARGPARSER.parse_args(fauxcommand)
    data = __getPayload(args)
    return _call_web_api(data, saveto)


def generate_sd_image(prompt, saveto=""):
    """
    """
    command = shlex.split(prompt)
    args = cnt.ARGPARSER.parse_args(command)
    if isinstance(args, str):
        # Custom ArgumentParser returns str on error/help
        return args
    if args.print_defaults:
        return f"POSITIVE PROMPT:{cnt.PATTERN}\n\nNEGATIVE PROMPT:{cnt.NEG_PATTERN}"

    print(args)
    data = __getPayload(args)
    print(data)
    return _call_web_api(data, saveto="")




if __name__ == "__main__":
    print(generate_sd_image("'black rock shooter' -ar p -s drawing"))