# AUTOGENERATED! DO NOT EDIT! File to edit: ../14_CutMixRandom.ipynb.

# %% auto 0
__all__ = ['CutMixRandom']

# %% ../14_CutMixRandom.ipynb 2
from .HoleMakerTechnique import *
from .HoleMakerRandom import *
from .HolesFilling import *
import numpy as np

# %% ../14_CutMixRandom.ipynb 4
class CutMixRandom(HolesFilling):
    "Defines the amount of holes, the technique used to make them and the probability of apply the technique."
    def __init__(self,
                 holes_num = 1, # The amount of holes to make.
                 hole_maker: "HoleMakerTechnique" = None, # The strategy used to make the holes.
                 p = 1.0): # The probability of applying this technique.
        super().__init__(hole_maker)
        self.holes_num = holes_num
        self.p = p

    def before_batch(self):
        "Applies the CutMix technique."
        if random() < self.p:
            for index, (image, mask) in enumerate(zip(self.x, self.y)):
                for _ in range(self.holes_num):
                    rand = randint(0, image.shape[0])
                    other_image, other_mask = self.x[rand], self.y[rand]
                    xhole, yhole = self.make_hole(mask)
                    sub_image, sub_mask = other_image[:, yhole, xhole], other_mask[yhole, xhole]
                    self.fill_hole(image, mask, xhole, yhole, [sub_image, sub_mask])