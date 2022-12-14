# AUTOGENERATED! DO NOT EDIT! File to edit: ../211_ArtMix.ipynb.

# %% auto 0
__all__ = ['ArtMix']

# %% ../211_ArtMix.ipynb 2
# library
from .holemakertechnique import HoleMakerTechnique, HoleMakerRandom
from .regionmodifier import RegionModifier
from .iholesfilling import HolesFilling

# others
import cv2
import random
from fastai.basics import *
import numpy as np

# %% ../211_ArtMix.ipynb 4
class ArtMix(HolesFilling):
    "Defines the amount of holes, the technique used to make them and the probability of apply the technique."
    def __init__(self,
                 mask_path: str, # The path to the image that is going to be used as mask.
                 holes_num: int = 1, # The amount of holes to make.
                 use_black: bool = True, # Whether to use the black part of the mask or the white part of the mask.
                 modifier: "RegionModifier" = None, # The modifier that defines the traditional augments to apply to the selected regions.
                 hole_maker: "HoleMakerTechnique" = None, # The strategy used to make the holes.
                 p: float = 0.5): # The probability of applying this technique.
        hole_maker = hole_maker if hole_maker else HoleMakerBounded()
        super().__init__(modifier, hole_maker)
        self.holes_num = holes_num
        self.use_black = use_black
        self.p = p
        
        # Converts the mask_img into a mask
        mask_img = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        mask_img = np.array(mask_img)
        
        # It is needed to permute the image because opencv works with a (H,W,C) format
        mask_img = mask_img.transpose(1, 0)
        hole_size = self.hole_maker.hole_size
        # It is needed to interpolate the integers without transforming them into floats
        mask_img = cv2.resize(mask_img, hole_size, interpolation = cv2.INTER_LINEAR_EXACT)
        mask_img = mask_img.transpose(1, 0)
        
        # transforms the mask
        mask_img[mask_img != 0] = 255
        
        self.used_value = 0 if use_black else 255
        self.mask_img = tensor(mask_img).to(device = "cuda")

    def before_batch(self):
        "Applies the CutMix technique."
        
        if not self.training:
            return
        
        for image, mask in zip(self.x, self.y):
            if random.random() < self.p:
                for _ in range(self.holes_num):
                    xhole, yhole = self.make_hole(mask)
                    sub_image, sub_mask = image[:, yhole, xhole], mask[yhole, xhole]
                    # tensor(np.zeros_like(sub_image.cpu())).to(device = "cuda")
                    image[:, yhole, xhole] = torch.where(self.mask_img[np.newaxis, ...] == self.used_value, torch.min(image), sub_image)
                    mask[yhole, xhole] = torch.where(self.mask_img == self.used_value, 0, sub_mask)
