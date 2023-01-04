APPLICATION_ID = "krita_stable_diffusion"
SCHEDULERS = [
    "euler_a",
    "euler",
    "ddpm",
    "ddim",
    "plms",
    "lms",
    "dpm"
]
UPSCALERS = ["None", "Lanczos"]
MODEL_VERSIONS = [
    "v1",
    "v2",
]
MODELS = {
    "v1": [
        # "stable-diffusion-v1-5",
        # "stable-diffusion-inpainting",
    ],
    "v2": [
        # "stable-diffusion-2-1-base",
        # "stable-diffusion-x4-upscaler",
        # "stable-diffusion-2-inpainting",
        # "stable-diffusion-2-depth",
    ]
}
DEFAULT_MODEL = MODELS["v2"][0] if len(MODELS["v2"]) > 0 else None
DEFAULT_SCHEDULER = SCHEDULERS[0]
MIN_SEED = 4294967295#0
MAX_SEED = 4294967295