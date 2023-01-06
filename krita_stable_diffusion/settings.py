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
MODELS = {
    "v1": [
        "runwayml/stable-diffusion-v1-5",
        "runwayml/stable-diffusion-inpainting",
    ],
    "v2": [
        "stabilityai/stable-diffusion-2-1-base",
        "stabilityai/stable-diffusion-x4-upscaler",
        "stabilityai/stable-diffusion-2-inpainting",
        "stabilityai/stable-diffusion-2-depth",
    ]
}
DEFAULT_MODEL = MODELS["v2"][0] if len(MODELS["v2"]) > 0 else None
DEFAULT_SCHEDULER = SCHEDULERS[0]
MIN_SEED = 0
MAX_SEED = 4294967295
CHUNK_SIZE = 1024
DEFAULT_PORT=50006
DEFAULT_HOST="localhost"
