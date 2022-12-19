APPLICATION_ID = "krita_stable_diffusion"
SAMPLERS = ["DDIM", "PLMS",]# 'k_dpm_2_a', 'k_dpm_2', 'k_euler_a', 'k_euler', 'k_heun', 'k_lms']
UPSCALERS = ["None", "Lanczos"]
MODELS = [
    "stable-diffusion-2-1-base",
    "stable-diffusion-2-base",
    "stable-diffusion-v1-5",
    "stable-diffusion-v1-4",
    "stable-diffusion-v1-3",
    "stable-diffusion-v1-2",
    "stable-diffusion-v1-1",
    "w4ffl35/kqz",
]
DEFAULT_MODEL = MODELS[0]
DEFAULT_SCHEDULER = SCHEDULERS[0]
MIN_SEED = 0
MAX_SEED = 4294967295
