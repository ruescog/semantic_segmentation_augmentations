# AUTOGENERATED! DO NOT EDIT! File to edit: ../200_IHolesFilling.ipynb.

# %% auto 0
__all__ = ['HolesFilling']

# %% ../200_IHolesFilling.ipynb 2
# library
from .holemakertechnique import HoleMakerTechnique, HoleMakerRandom
from .regionmodifier import RegionModifier

# others
import torch
import numpy as np
from fastai.vision.all import Callback, TensorBase

# typedpython
from typing import Union, Callable

# %% ../200_IHolesFilling.ipynb 5
class HolesFilling(Callback):
    "Defines the strategy used to make the holes."
    def __init__(self,
                 modifier: "RegionModifier" = None, # The modifier that defines the traditional augments to apply to the selected regions.
                 hole_maker: "HoleMakerTechnique" = None # The strategy used to make the holes.
        ):
        self.modifier = modifier if modifier else RegionModifier()
        self.hole_maker = hole_maker if hole_maker else HoleMakerRandom()
        self.training = False

    def make_hole(self,
                  mask): # The mask associated with the image where the hole is going to be made.
        "Makes the holes in the mask."
        return self.hole_maker.get_hole(mask)

    def fill_hole(self,
                  image: np.ndarray, # The image where the hole is going to be made.
                  mask: np.ndarray, # The mask associated with the image where the hole is going to be made.
                  xhole: slice, # The slice that defines the x-region where the hole is.
                  yhole: slice, # The slice that defines the y-region where the hole is.
                  fill_values: Union[Callable[[np.ndarray], np.ndarray], np.ndarray, float], # The value to fill the hole (a function to apply or a constant).
                  transparence: bool = False # Whether the fill_values must be added to the image in a transparent form. fill_value if fill_value else image for each value in fill_values
                 ): 
        "Fills a specific hole with something."
        
        # If the values are matrixes, we can apply the modifier to them
        if isinstance(fill_values[0], TensorBase) and isinstance(fill_values[1], TensorBase):
            fill_values = self.modifier.apply(*list(map(lambda array: np.array(array.cpu()), fill_values)))
            fill_values = list(map(lambda array: torch.from_numpy(array).float().cuda(), fill_values))
    
        image[:, yhole, xhole] = torch.where(fill_values[1][np.newaxis, ...] != 0, fill_values[0], image[:, yhole, xhole]) if transparence else fill_values[0]
        mask[yhole, xhole] = torch.where(fill_values[1] != 0, fill_values[1], mask[yhole, xhole]) if transparence else fill_values[1]
        
    # augmentations must only be applied on training set, so we will change the value of 'training' flag before validating to avoid the aplication of the augments.
    def before_train(self):
        "Sets the training flag to True"
        self.training = True
    
    def after_train(self):
        "Sets the training flag to False"
        self.training = False
