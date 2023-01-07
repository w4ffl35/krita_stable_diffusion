import os
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
    "v1 (community)",
    "v2 (community)",
]
MODELS = {  # Default stable diffusion models
    "v1": [
        {
            "name": "v1-5",
            "path": "runwayml/stable-diffusion-v1-5",
        },
        {
            "name": "Inpainting model",
            "path": "runwayml/stable-diffusion-inpainting",
        }
    ],
    "v2": [
        {
            "name": "v2-1",
            "path": "stabilityai/stable-diffusion-2-1-base",
        },
        {
            "name": "4x upscaler",
            "path": "stabilityai/stable-diffusion-x4-upscaler",
        },
        {
            "name": "Inpainting model",
            "path": "stabilityai/stable-diffusion-2-inpainting",
        },
        {
            "name": "Depth model",
            "path": "stabilityai/stable-diffusion-2-depth",
        }
    ],
}
DEFAULT_MODEL = os.path.join(
    MODELS["v2"][0]["path"],
    MODELS["v2"][0]["name"]
) if len(MODELS["v2"]) > 0 else None
DEFAULT_SCHEDULER = SCHEDULERS[0]
MIN_SEED = 0
MAX_SEED = 4294967295
CHUNK_SIZE = 1024
DEFAULT_PORT=50006
DEFAULT_HOST="localhost"
