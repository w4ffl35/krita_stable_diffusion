import torch
from stablediffusion.classes.base import BaseModel
from torch import autocast
from tqdm import tqdm, trange
from contextlib import nullcontext
from stablediffusion.classes.settings import settings

class Txt2Img(BaseModel):
    args = settings["txt2img"]

    def sample(self, options=None):
        super().sample(options)
        torch.cuda.empty_cache()
        opt = self.opt
        model = self.model
        sample_path = self.sample_path
        data = self.data
        batch_size = self.batch_size
        sampler = self.plms_sampler
        start_code = self.start_code
        base_count = self.base_count
        self.set_seed()
        precision_scope = nullcontext
        if opt.precision == "autocast":
            precision_scope = autocast
        saved_files = []
        shape = [opt.C, opt.H // opt.f, opt.W // opt.f]
        with torch.no_grad():
            with precision_scope("cuda"):
                with model.ema_scope():
                    uc = None
                    if opt.scale != 1.0:
                        uc = model.get_learned_conditioning(
                            batch_size * [""]
                        )
                        self.log.info("sample")
                    for _n in trange(opt.n_iter, desc="Sampling"):
                        for prompts in tqdm(data, desc="data"):
                            samples_ddim, _ = sampler.sample(
                                S=opt.ddim_steps,
                                conditioning=model.get_learned_conditioning(
                                    list(prompts) if isinstance(
                                        prompts, tuple
                                    ) else prompts
                                ),
                                batch_size=1,
                                shape=shape,
                                verbose=False,
                                unconditional_guidance_scale=opt.scale,
                                unconditional_conditioning=uc,
                                eta=opt.ddim_eta,
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

        torch.cuda.empty_cache()
        return saved_files

    def handle_save_image(self, image, saved_files, base_count, sample_path, opt):
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
