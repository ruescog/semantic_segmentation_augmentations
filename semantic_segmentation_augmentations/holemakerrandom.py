# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_HoleMakerRandom.ipynb.

# %% auto 0
__all__ = ['HoleMakerRandom']

# %% ../01_HoleMakerRandom.ipynb 3
#library
from .iholemakertechnique import HoleMakerTechnique

# others
import random
import numpy as np

# %% ../01_HoleMakerRandom.ipynb 5
class HoleMakerRandom(HoleMakerTechnique):
    def __init__(self,
                 hole_size: tuple = (100, 100)): # The size of the hole in a tuple like (y, x).
        "Defines the size of the hole."
        super().__init__(hole_size)

    def get_hole(self,
             mask: np.ndarray): # The mask associated with the image where the hole is going to be made.
        "Defines how to make the hole."
        shape = mask.shape
        randx, randy = random.randint(0, shape[1] - 1), random.randint(0, shape[0] - 1)
        return [slice(randx, randx + self.hole_size[1]), slice(randy, randy + self.hole_size[0])]
