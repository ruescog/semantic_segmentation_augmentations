# AUTOGENERATED! DO NOT EDIT! File to edit: ../12_CutOutSemantic.ipynb.

# %% auto 0
__all__ = ['CutOutSemantic']

# %% ../12_CutOutSemantic.ipynb 2
from .holemakertechnique import *
from .holemakerrandom import *
from .holesfilling import *
import numpy as np
import random
import torch
from fastai.basics import *

# %% ../12_CutOutSemantic.ipynb 4
class CutOutSemantic(HolesFilling):
    "Defines the amount of holes, the class to be occluded, the technique used to make them and the probability of apply the technique."
    def __init__(self,
                 holes_num = 1, # The amount of holes to make.
                 occlusion_class = -1, # The class to remove. If -1, selects it randomly in each use.
                 hole_maker: "HoleMakerTechnique" = None, # The strategy used to make the holes.
                 p = 0.5): # The probability of applying this technique.
        super().__init__(hole_maker)
        self.holes_num = holes_num
        self.occlusion_class = occlusion_class
        self.p = p

    def before_batch(self):
        "Applies the CutOut technique with semantic information (only applies the CutOut to a selected class)."
        for image, mask in zip(self.x, self.y):
            if random.random() < self.p:
                shape = image.shape[1:]
                for _ in range(self.holes_num):
                    xhole, yhole = self.make_hole(mask)
                    occlusion_value = self.occlusion_class if self.occlusion_class != -1 else random.randint(1, len(mask.unique()))
                    sub_image, sub_mask = TensorBase(image[:, yhole, xhole]), TensorBase(mask[yhole, xhole])
                    replacement_mask = sub_mask == occlusion_value
                    sub_image[:, replacement_mask] = torch.min(image)
                    sub_mask[replacement_mask] = 0
                    self.fill_hole(image, mask, xhole, yhole, [sub_image, sub_mask])
