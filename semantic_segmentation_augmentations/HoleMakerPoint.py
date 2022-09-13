# AUTOGENERATED! DO NOT EDIT! File to edit: ../04_holeMakerPoint.ipynb.

# %% auto 0
__all__ = ['HoleMakerPoint']

# %% ../04_holeMakerPoint.ipynb 3
from .HoleMakerTechnique import *
import numpy as np

# %% ../04_holeMakerPoint.ipynb 5
class HoleMakerPoint(HoleMakerTechnique):
    def __init__(self,
                 hole_size: tuple = (100, 100)): # The size of the hole in a tuple like (y, x).
        "Defines the size of the hole."
        super().__init__(hole_size)
        self.x = 0
        self.y = 0

    def get_hole(self,
             mask: np.ndarray): # The mask associated with the image where the hole is going to be made.
        "Defines how to make the hole."
        return [slice(self.x, self.x + self.hole_size[0]), slice(self.y, self.y + self.hole_size[1])]
