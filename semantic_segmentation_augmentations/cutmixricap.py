# AUTOGENERATED! DO NOT EDIT! File to edit: ../26_CutMixRICAP.ipynb.

# %% auto 0
__all__ = ['CutMixRICAP']

# %% ../26_CutMixRICAP.ipynb 2
# library
from .holemakertechnique import HoleMakerTechnique, HoleMakerPoint
from .regionmodifier import RegionModifier
from .iholesfilling import HolesFilling

# others
import random
from fastai.basics import *
import numpy as np

# %% ../26_CutMixRICAP.ipynb 4
class CutMixRICAP(HolesFilling):
    "Defines the amount of holes, the technique used to make them and the probability of apply the technique."
    def __init__(self,
                 t: float = 0.0, # The restriction of the central-boundary position. If 0.0, the central point is selected randomly. If not, the central point is restricted into [t * size, (1-t) * size] area.
                 u: float = None, # The restriction of the corner-boundary position. If None, t hparam is used. If not, t hparam is ignored and u hparam is used to restrict the central point into a [0, u * size] U [(1-u) * size, size] area.
                 modifier: "RegionModifier" = None, # The modifier that defines the traditional augments to apply to the selected regions.
                 hole_maker: "HoleMakerTechnique" = None, # The strategy used to make the holes.
                 p = 0.5): # The probability of applying this technique.
        hole_maker = hole_maker if hole_maker else HoleMakerPoint()
        super().__init__(modifier, hole_maker)
        self.t = t
        self.u = u if t == None else None
        self.p = p
                    
    def before_batch(self):
        "Applies the CutMixRICAP technique (divides the image into a grid and shuffles the portions)."
        x, y = tensor(self.x).clone(), tensor(self.y).clone() # tensor is defined in fastai.basics
        for image, mask in zip(self.x, self.y):
            if random.random() < self.p:
                shape = image.shape[1:]
                if self.u == None:
                    h = random.randint(int(self.t * shape[0]), int((1 - self.t) * (shape[0] - 1)))
                    w = random.randint(int(self.t * shape[1]), int((1 - self.t) * (shape[1] - 1)))
                else:
                    h = random.randint(0, int(self.u * shape[0])) if random.random() < 0.5 else random.randint(int((1 - self.u) * shape[0]), shape[0] - 1)
                    w = random.randint(0, int(self.u * shape[1])) if random.random() < 0.5 else random.randint(int((1 - self.u) * shape[1]), shape[1] - 1)
                
                regions = [
                    [slice(0, h), slice(0, w)],
                    [slice(0, h), slice(w, shape[0])],
                    [slice(h, shape[1]), slice(0, w)],
                    [slice(h, shape[1]), slice(w, shape[0])]
                ]

                for xhole, yhole in regions:
                    rand = random.randint(0, x.shape[0] - 1)
                    other_image, other_mask = x[rand], y[rand]
                    sub_image, sub_mask = other_image[:, yhole, xhole], other_mask[yhole, xhole]
                    self.fill_hole(image, mask, xhole, yhole, [sub_image, sub_mask])
