# AUTOGENERATED! DO NOT EDIT! File to edit: ../17_CutMixResizeMix.ipynb.

# %% auto 0
__all__ = ['CutMixResizeMix']

# %% ../17_CutMixResizeMix.ipynb 2
from .holemakertechnique import *
from .holemakerbounded import *
from .holesfilling import *
import numpy as np
import random
import cv2
from fastai.basics import *

# %% ../17_CutMixResizeMix.ipynb 4
class CutMixResizeMix(HolesFilling):
    "Defines the amount of holes, the technique used to make them and the probability of apply the technique."
    def __init__(self,
                 holes_num = 1, # The amount of holes to make.
                 hole_maker: "HoleMakerTechnique" = None, # The strategy used to make the holes.
                 p = 0.5): # The probability of applying this technique.
        hole_maker = hole_maker if hole_maker else HoleMakerBounded(hole_size = (64, 64))
        super().__init__(hole_maker)
        self.holes_num = holes_num
        self.p = p

    def before_batch(self):
        "Applies the CutMixResizeMix technique (fills a hole with the whole resized image)."
        for image, mask in zip(self.x, self.y):
            if random.random() < self.p:
                for _ in range(self.holes_num):
                    xhole, yhole = self.make_hole(mask)
                    # It is needed to permute the image because opencv works with a (H,W,C) format
                    sub_image, sub_mask = image.permute(1, 2, 0), mask.transpose(1, 0)
                    hole_size = self.hole_maker.hole_size
                    sub_image = TensorBase(cv2.resize(np.array(sub_image.cpu()), hole_size))
                    # It is needed to interpolate the integers without transforming them into floats
                    sub_mask = TensorBase(cv2.resize(np.array(sub_mask.cpu()), hole_size, interpolation = cv2.INTER_LINEAR_EXACT))
                    sub_image, sub_mask = sub_image.permute(2, 0, 1), sub_mask.transpose(1, 0)
                    self.fill_hole(image, mask, xhole, yhole, [sub_image, sub_mask])
