# AUTOGENERATED! DO NOT EDIT! File to edit: ../11_CutOutRandom.ipynb.

# %% auto 0
__all__ = ['CutOutRandom']

# %% ../11_CutOutRandom.ipynb 2
from .holemakertechnique import *
from .holemakerrandom import *
from .holesfilling import *
import numpy as np

# %% ../11_CutOutRandom.ipynb 4
class CutOutRandom(HolesFilling):
    "Defines the amount of holes, the technique used to make them and the probability of apply the technique."
    def __init__(self,
                 holes_num: int = 1, # The amount of holes to make.
                 hole_maker: "HoleMakerTechnique" = None, # The strategy used to make the holes.
                 p = 1.0): # The probability of applying this technique.
        super().__init__(hole_maker)
        self.holes_num = holes_num
        self.p = p

    def before_batch(self):
        "Applies the CutOut technique."
        if random() < self.p:
            for image, mask in zip(self.x, self.y):
                min_image = torch.min(image)
                for _ in range(self.holes_num):
                    xhole, yhole = self.make_hole(mask)
                    self.fill_hole(image, mask, xhole, yhole, [min_image, 0])