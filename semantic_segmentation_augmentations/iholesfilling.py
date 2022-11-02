# AUTOGENERATED! DO NOT EDIT! File to edit: ../20_IHolesFilling.ipynb.

# %% auto 0
__all__ = ['HolesFilling']

# %% ../20_IHolesFilling.ipynb 2
# library
from .holemakertechnique import HoleMakerTechnique, HoleMakerRandom
from .regionmodifier import RegionModifier

# others
import torch
import numpy as np
from fastai.vision.all import Callback

# typedpython
from typing import Union, Callable

# %% ../20_IHolesFilling.ipynb 5
class HolesFilling(Callback):
    "Defines the strategy used to make the holes."
    def __init__(self,
                 modifier: "RegionModifier" = None, # The modifier that defines the traditional augments to apply to the selected regions.
                 hole_maker: "HoleMakerTechnique" = None # The strategy used to make the holes.
        ):
        self.modifier = modifier if modifier else RegionModifier()
        self.hole_maker = hole_maker if hole_maker else HoleMakerRandom()

    def make_hole(self,
                  mask): # The mask associated with the image where the hole is going to be made.
        "Makes the holes in the mask."
        return self.hole_maker.get_hole(mask)

    def fill_hole(self,
                  image: np.ndarray, # The image where the hole is going to be made.
                  mask: np.ndarray, # The mask associated with the image where the hole is going to be made.
                  xhole: slice, # The slice that defines the x-region where the hole is.
                  yhole: slice, # The slice that defines the y-region where the hole is.
                  fill_values: Union[Callable[[np.ndarray], np.ndarray], np.ndarray, float]): # The value to fill the hole (a function to apply or a constant).
        "Fills a specific hole with something."
        
        # If the values are matrixes, we can apply the modifier to them
        if not callable(fill_values[0]) and type(fill_values[0]) is not float \
           and not callable(fill_values[1]) and type(fill_values[1]) is not float:
            fill_values = self.modifier.apply(*list(map(lambda array: np.array(array.cpu()), fill_values)))
            fill_values = list(map(lambda array: torch.from_numpy(array).float().cuda(), fill_values))

        image[:, yhole, xhole] = fill_values[0](image) if callable(fill_values[0]) else fill_values[0]
        mask[yhole, xhole] = fill_values[1](mask) if callable(fill_values[1]) else fill_values[1]
