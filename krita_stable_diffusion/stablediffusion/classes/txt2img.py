import torch
from stablediffusion.classes.base import BaseModel
from torch import autocast
from tqdm import tqdm, trange
from contextlib import nullcontext
from stablediffusion.classes.settings import settings

DEVICE="cuda"


class Txt2Img(BaseModel):
    args = settings["txt2img"]

    def sample(self, options=None):
        super().sample(options)
        self.clear_cache()
        opt = self.opt
        model = self.model
        sample_path = self.sample_path
        data = self.data
        sampler = self.plms_sampler
        start_code = self.start_code
        base_count = self.base_count
        self.set_seed()
        precision_scope = nullcontext
        if opt.precision == "autocast":
            precision_scope = autocast
        saved_files = []
        shape = [opt.C, opt.H // opt.f, opt.W // opt.f]
        scale = opt.scale
        ddim_eta = opt.ddim_eta
        is_verbose_sample = False
        with torch.no_grad():
            with precision_scope(DEVICE):
                with model.ema_scope():
                    uncon_conditioning = None
                    if opt.scale != 1.0:
                        uncon_conditioning = model.get_learned_conditioning(
                            self.batch_size * [""]
                        )
                        self.log.info("sample")
                    for _n in trange(opt.n_iter, desc="Sampling"):
                        for prompts in tqdm(data, desc="data"):
                            conditioning = model.get_learned_conditioning(
                                list(prompts) if isinstance(
                                    prompts, tuple
                                ) else prompts
                            )
                            samples_ddim, _ = sampler.sample(
                                S=opt.ddim_steps,
                                conditioning=conditioning,
                                batch_size=self.batch_size,
                                shape=shape,
                                verbose=is_verbose_sample,
                                unconditional_guidance_scale=scale,
                                unconditional_conditioning=uncon_conditioning,
                                eta=ddim_eta,
                                x_T=start_code
                            )
                            image = self.prepare_image(model, samples_ddim)
                            saved_files, base_count = self.handle_save_image(
                                image,
                                saved_files,
                                base_count,
                                sample_path,
                                opt
                            )
                        self.update_seed()

        self.clear_cache()
        return saved_files

    def handle_save_image(
            self,
            image,
            saved_files,
            base_count,
            sample_path,
            opt
    ):
        if not opt.skip_save:
            file_name = self.save_image(
                image,
                sample_path,
                base_count
            )
            saved_files.append({
                "file_name": file_name,
                "seed": opt.seed,
            })
            base_count += 1
        return saved_files, base_count

    def prepare_image(self, model, samples_ddim):
        x_samples_ddim = self.get_first_stage_sample(model, samples_ddim)
        return self.filter_nsfw_content(x_samples_ddim)
