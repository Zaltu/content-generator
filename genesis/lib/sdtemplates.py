"""
Collection of payload templates taken model style into consideration.
Streamlines making higher quality shitposts with minimal effort.
"""
PATTERN = """{prompt}

<lora:add_detail:1.5>"""
PATTERN_XL = """{prompt}

<lora:add-detail-xl:1.5>"""
NEG_PATTERN = """{neg_prompt}

(worst quality, low quality:1.3), simple background, logo, watermark, text, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, bad-hands-5, bad-image-v2-39000, bad_prompt_version2, bad_quality, easynegative, ng_deepnegative_v1_75t, BadDream, black and white, (closeup shot)"""
NEG_PATTERN_XL = """{neg_prompt}, negativeXL_D, FastNegative"""


class SDTemplate():
    """
    Bootleg namespace class.
    I swear I've done this before somewhere.
    """
    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])
    def __getattribute__(self, __name):
        if __name in super().__getattribute__("__dict__"):
            return super().__getattribute__("__dict__")[__name]
        elif __name == "__dict__":
            return super().__getattribute__("__dict__")
        else:
            return None
    def __iter__(self):
        for key, val in self.__dict__.items():
            yield key, val


ANIME = SDTemplate(
    sd_model_checkpoint="XL_explicitFreedomNSFW_beta",
    sd_vae="sdxl_vae.safetensors",
    height=1200,
    width=1024,
    cfg_scale=6,
    CLIP_stop_at_last_layers=1,
    prompt="""{prompt}
    4k, 8k, masterpiece, very high quality, hdr, professional digital artwork, key art, beautiful anime art

    <lora:add-detail-xl:3>""",
    negative_prompt=NEG_PATTERN_XL + ", fused limbs, pussy, nsfw",
)
DRAWING = SDTemplate(
    sd_model_checkpoint="ACTIVE_Drawing_revAnimated_v122",
    sd_vae="vae-ft-mse-840000-ema-pruned.ckpt",
    cfg_scale=7,
    CLIP_stop_at_last_layers=2,
    prompt="""{prompt}

    masterpiece, ultra high quality, sharp lines, perfect body, perfect face, hdr, 4k, 8k, official artwork, soft natural lighting, low contrast,

    <lora:add_detail:0.5>""",
    negative_prompt=NEG_PATTERN,
)
PHOTO = SDTemplate(
    sd_model_checkpoint="ACTIVE_Realism_epicrealism_pureEvolutionV4",
    sd_vae="vae-ft-mse-840000-ema-pruned.ckpt",
    cfg_scale=6,
    CLIP_stop_at_last_layers=2,
    prompt="""{prompt}

    masterpiece, delicate, (intricate details:1.3), (photorealism, best quality), (hyper realistic:1.3), (high detailed:1.2), (intricate detail:1.2), (photo realistic:1.3), (hyper realistic:1.3)

    <lora:add_detail:1>""",
    negative_prompt=NEG_PATTERN + "drawing, frame, paper,  UnrealisticDream",
)
STYLIZED = SDTemplate(
    sd_model_checkpoint="ACTIVE_Stylized_mouseymix",
    sd_vae="pastel-waifu-diffusion.vae.pt",
    cfg_scale=7,
    CLIP_stop_at_last_layers=2,
    prompt="""{prompt}

    <lora:add_detail:1>""",
    negative_prompt="",
)
WATERCOLOR = SDTemplate(
    sd_model_checkpoint="ACTIVE_Drawing_revAnimated_v122",
    sd_vae="vae-ft-mse-840000-ema-pruned.ckpt",
    cfg_scale=7,
    CLIP_stop_at_last_layers=2,
    prompt="""{prompt}

    masterpiece, ultra high quality, sharp lines, perfect body, perfect face, hdr, 4k, 8k, official artwork, soft natural lighting, low contrast,

    <lora:Colorwater_v4:0.8>""",
    negative_prompt=NEG_PATTERN,
)
FANTASY = SDTemplate(
    sd_model_checkpoint="ACTIVE_Fantasy_aZovyaRPGArtistTools_v3",
    sd_vae="vae-ft-mse-840000-ema-pruned.ckpt",
    cfg_scale=7,
    CLIP_stop_at_last_layers=2,
    prompt="""{prompt}

    masterpiece, ultra high quality, sharp lines, perfect body, perfect face, hdr, 4k, 8k, official artwork, soft natural lighting, low contrast,

    <lora:add_detail:1>""",
    negative_prompt=NEG_PATTERN,
)