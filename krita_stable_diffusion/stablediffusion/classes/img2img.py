import os
import random
import numpy as np
import torch
from torch import autocast
from PIL import Image
from contextlib import nullcontext
from tqdm import tqdm, trange
from stablediffusion.classes.base import BaseModel
from einops import repeat
from stablediffusion.classes.settings import settings

SIZE = 16
NUMPY_TYPE = np.float16
DEVICE = "cuda"

def load_img(path):
    image = Image.open(path).convert("RGB")
    w, h = image.size

    print(f"loaded input image of size ({w}, {h}) from {path}")

    w, h = map(lambda x: x - x % SIZE, (w, h))
    image = image.resize((w, h), resample=Image.LANCZOS)
    image = np.array(image, device=DEVICE).astype(NUMPY_TYPE) / 255.0
    image = image[None].transpose(0, 3, 1, 2)
    image = torch.from_numpy(image)
    return 2. * image - 1.


class Img2Img(BaseModel):
    args = settings["img2img"]

    def sample(self, options=None):
        """
        Sample from the model
        :param options: dict of options
        :return: None
        """
        super().sample(options)

        self.clear_cache()

        opt = self.opt
        batch_size = self.batch_size
        model = self.model
        sampler = self.ddim_sampler
        data = self.data
        sample_path = self.sample_path
        base_count = self.base_count
        device = self.device
        self.set_seed()

        assert os.path.isfile(opt.init_img)
        init_image = load_img(opt.init_img).to(device)
        init_image = repeat(init_image, '1 ... -> b ...', b=batch_size)

        # move to latent space
        init_latent = model.get_first_stage_encoding(
            model.encode_first_stage(init_image)
        )

        sampler.make_schedule(
            ddim_num_steps=opt.ddim_steps,
            ddim_eta=opt.ddim_eta,
            verbose=False
        )

        assert 0. <= opt.strength <= 1., 'can only work with strength in [0.0, 1.0]'
        t_enc = int(opt.strength * opt.ddim_steps)
        print(f"target t_enc is {t_enc} steps")

        precision_scope = autocast if opt.precision == "autocast" else nullcontext

        saved_files = []
        with torch.no_grad():
            with precision_scope(DEVICE):
                with model.ema_scope():
                    all_samples = list()
                    uc = None
                    if opt.scale != 1.0:
                        uc = model.get_learned_conditioning(batch_size * [""])
                    for _n in trange(opt.n_iter, desc="Sampling"):
                        for prompts in tqdm(data, desc="data"):
                            if isinstance(prompts, tuple):
                                prompts = list(prompts)

                            # encode (scaled latent)
                            z_enc = sampler.stochastic_encode(
                                init_latent,
                                torch.tensor(
                                    [t_enc] * batch_size,
                                    device=device,
                                )
                            )
                            # decode it
                            samples = sampler.decode(
                                z_enc,
                                model.get_learned_conditioning(prompts),
                                t_enc,
                                unconditional_guidance_scale=opt.scale,
                                unconditional_conditioning=uc
                            )

                            x_samples = self.get_first_stage_sample(
                                model,
                                samples
                            )

                            if not opt.skip_save:
                                file_name = self.save_image(
                                    x_samples,
                                    sample_path,
                                    base_count
                                )
                                saved_files.append({
                                    "file_name": file_name,
                                    "seed": opt.seed,
                                })
                                base_count += 1

                            all_samples.append(x_samples)
                        self.update_seed()

        self.clear_cache()
        return saved_files
