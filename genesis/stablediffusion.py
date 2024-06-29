import os
import io
import copy
import shlex
import base64
import requests
from PIL import Image
from lib import sdconsts as cnt


def __getPayload(args):
    """
    """
    thisPro = copy.deepcopy(cnt.REQUEST_PAYLOAD)
    # Attempt style setting first, allowing for overwrites.
    if args.style:
        for setting, value in cnt.STYLES[args.style]:
            if setting in cnt.VALID_OVERRIDE_SETTINGS:
                thisPro["override_settings"][setting] = value
            else:
                thisPro[setting] = value
    xl = "XL" in thisPro.get("override_settings", {}).get("sd_model_checkpoint", "")

    if not args.old_defaults:
        thisPro["prompt"] = args.prompt
        thisPro["negative_prompt"] = args.neg_prompt
    elif thisPro["prompt"] != None or thisPro["negative_prompt"] != None:
        thisPro["prompt"] = thisPro["prompt"].format(prompt=args.prompt or "")
        thisPro["negative_prompt"] = thisPro["negative_prompt"].format(neg_prompt=args.neg_prompt or "")
    else:
        thisPro["prompt"] = cnt.sdtemplates.PATTERN.format(prompt=args.prompt) if not xl else cnt.sdtemplates.PATTERN_XL.format(prompt=args.prompt)
        thisPro["negative_prompt"] = cnt.sdtemplates.NEG_PATTERN.format(neg_prompt=args.prompt) if not xl else cnt.sdtemplates.NEG_PATTERN_XL.format(neg_prompt=args.prompt)
    args.prompt = None
    args.neg_prompt = None

    for setting, value in args.__dict__.items():
        if setting in thisPro and value:
            thisPro[setting] = value

    if args.aspect_ratio:
        match args.aspect_ratio:
            case 's':
                thisPro["width"] = 1024 if xl else 512
                thisPro["height"] = 1024 if xl else 512
            case 'p':
                thisPro["width"] = 1200 if xl else 600
                thisPro["height"] = 1504 if xl else 752
            case 'l':
                thisPro["width"] = 1920 if xl else 960
                thisPro["height"] = 1080 if xl else 540
    
    if args.hires:
        thisHR = cnt.HR_PAYLOAD.copy()
        thisHR["hr_prompt"] = args.prompt if args.no_defaults else cnt.sdtemplates.PATTERN.format(prompt=args.prompt)
        thisHR["hr_negative_prompt"] = args.neg_prompt if args.no_defaults else cnt.sdtemplates.NEG_PATTERN.format(neg_prompt=args.neg_prompt)
        thisHR["denoising_strength"] = args.denoising
        thisHR["hr_upscaler"] = args.upscaler
        thisHR["hr_second_pass_steps"] = args.steps
        thisPro.update(thisHR)

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


def generate_sd_image(command, saveto=""):
    """
    """
    command = shlex.split(command)
    args = cnt.ARGPARSER.parse_args(command)
    if isinstance(args, str):
        # Custom ArgumentParser returns str on error/help
        return args
    if args.print_defaults:
        return f"POSITIVE PROMPT:{cnt.sdtemplates.PATTERN}\n\nNEGATIVE PROMPT:{cnt.sdtemplates.NEG_PATTERN}"

    print(args)
    data = __getPayload(args)
    print(data)
    return _call_web_api(data, saveto)




if __name__ == "__main__":
    print(generate_sd_image("'black rock shooter' -ar p --style anime"))