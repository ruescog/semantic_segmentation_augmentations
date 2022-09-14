# AUTOGENERATED! DO NOT EDIT! File to edit: ../03_HoleMakerAttention.ipynb.

# %% auto 0
__all__ = ['HoleMakerAttention']

# %% ../03_HoleMakerAttention.ipynb 3
from .holemakertechnique import *
import numpy as np

# %% ../03_HoleMakerAttention.ipynb 5
class HoleMakerAttention(HoleMakerTechnique):
    def __init__(self,
                 attention_threshold: float = 0.1, # The ratio of relevant pixels in the selected region.
                 hole_size: tuple = (100, 100)): # The size of the hole in a tuple like (y, x).
        "Defines the size of the hole."
        super().__init__(hole_size)
        self.attention_threshold = attention_threshold

    def get_hole(self,
             mask: np.ndarray): # The mask associated with the image where the hole is going to be made.
        "Defines how to make the hole."
        shape = mask.shape
        sub_mask_information = 0
        while sub_mask_information / (self.hole_size[0] * self.hole_size[1]) < self.attention_threshold:
            randx, randy = randint(0, shape[1] - self.hole_size[1]), randint(0, shape[0] - self.hole_size[0])
            sub_mask = mask[[slice(randy, randy + self.hole_size[1]), slice(randx, randx + self.hole_size[0])]]
            sub_mask_information = sub_mask[sub_mask != 0].size().numel()

        return [slice(randx, randx + self.hole_size[0]), slice(randy, randy + self.hole_size[1])]