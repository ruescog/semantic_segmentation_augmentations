# AUTOGENERATED! DO NOT EDIT! File to edit: ../02_HoleMakerBounded.ipynb.

# %% auto 0
__all__ = ['HoleMakerBounded']

# %% ../02_HoleMakerBounded.ipynb 3
from .holemakertechnique import *
import numpy as np
import random

# %% ../02_HoleMakerBounded.ipynb 5
class HoleMakerBounded(HoleMakerTechnique):
    def __init__(self,
                 hole_size: tuple = (100, 100)): # The size of the hole in a tuple like (y, x).
        "Defines the size of the hole."
        super().__init__(hole_size)

    def get_hole(self,
             mask: np.ndarray): # The mask associated with the image where the hole is going to be made.
        "Defines how to make the hole."
        shape = mask.shape
        randx, randy = random.randint(0, shape[1] - self.hole_size[1] - 1), random.randint(0, shape[0] - self.hole_size[0] - 1)
        return [slice(randx, randx + self.hole_size[1]), slice(randy, randy + self.hole_size[0])]
