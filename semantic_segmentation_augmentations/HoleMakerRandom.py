# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_holeMakerRandom.ipynb.

# %% auto 0
__all__ = ['HoleMakerRandom']

# %% ../01_holeMakerRandom.ipynb 3
from .HoleMakerTechnique import *
import numpy as np

# %% ../01_holeMakerRandom.ipynb 5
class HoleMakerRandom(HoleMakerTechnique):
    def __init__(self,
                 hole_size: tuple = (100, 100)): # The size of the hole in a tuple like (y, x).
        "Defines the size of the hole."
        super().__init__(hole_size)

    def get_hole(self,
             mask: np.ndarray): # The mask associated with the image where the hole is going to be made.
        "Defines how to make the hole."
        shape = mask.shape
        randx, randy = randint(0, shape[1]), randint(0, shape[0])
        return [slice(randx, randx + self.hole_size[0]), slice(randy, randy + self.hole_size[1])]
