# AUTOGENERATED! DO NOT EDIT! File to edit: ../17_CutMixResizeMix.ipynb.

# %% auto 0
__all__ = ['CutMixResizeMix']

# %% ../17_CutMixResizeMix.ipynb 2
from .HoleMakerTechnique import *
from .HoleMakerBounded import *
from .HolesFilling import *
import numpy as np

# %% ../17_CutMixResizeMix.ipynb 4
class CutMixResizeMix(HolesFilling):
    "Defines the amount of holes, the technique used to make them and the probability of apply the technique."
    def __init__(self,
                 holes_num = 1, # The amount of holes to make.
                 hole_maker: "HoleMakerTechnique" = None, # The strategy used to make the holes.
                 p = 1.0): # The probability of applying this technique.
        hole_maker = hole_maker if hole_maker else HoleMakerBounded(hole_size = (64, 64))
        super().__init__(hole_maker)
        self.holes_num = holes_num
        self.p = p

    def before_batch(self):
        "Applies the CutMixResizeMix technique (fills a hole with the whole resized image)."
        if random() < self.p:
            for image, mask in zip(self.x, self.y):
                for _ in range(self.holes_num):
                    xhole, yhole = self.make_hole(mask)
                    sub_image, sub_mask = image[..., tf.newaxis], mask[..., tf.newaxis]
                    hole_size = self.hole_maker.hole_size
                    sub_image = TensorBase(tf.image.resize(sub_image.cpu(), hole_size)[..., 0])
                    sub_mask = TensorBase(tf.image.resize(sub_mask.cpu(), hole_size)[..., 0])
                    self.fill_hole(image, mask, xhole, yhole, [sub_image, sub_mask])
