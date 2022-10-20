# AUTOGENERATED! DO NOT EDIT! File to edit: ../05_HoleMakerROI.ipynb.

# %% auto 0
__all__ = ['HoleMakerROI']

# %% ../05_HoleMakerROI.ipynb 3
from .holemakertechnique import *
from .holemakerbounded import HoleMakerBounded
import numpy as np
import cv2
import random

# %% ../05_HoleMakerROI.ipynb 5
class HoleMakerROI(HoleMakerTechnique):
    def __init__(self,
            ROI_class: int = -1, # The class that is going to be targeted to select as a ROI (region of interest).
            ROI_area: int = 25, # The minimum area to be selected as a ROI.
            delta_ratio: float = None # The ratio of pixels of the ROI that are going to be used. A ratio of 1 takes all the ROI pixels, a ratio < 1 crops the ROI and a ratio > 1 adds more pixels to the ROI. A None ratio takes a random value [0.9, 1.1) in each usage.
        ):
        self.ROI_class = ROI_class
        self.ROI_area = ROI_area
        self.delta_ratio = delta_ratio
        self.holes = []
        self.mask = None
    
    def __get_holes__(self,
             mask: np.ndarray): # The mask associated with the image where the holes are going to be made.
        "Defines how to make the hole."
        # Gets the contours of the binary mask
        ROI_class = self.ROI_class if self.ROI_class != -1 else random.randint(1, np.unique(mask).shape[0] - 1)
        _mask = np.copy(mask)
        _mask[_mask != ROI_class] = 0
        contours, _ = cv2.findContours(_mask, cv2.RETR_FLOODFILL, cv2.CHAIN_APPROX_SIMPLE)

        # Extracts the ROIs
        areas = []
        extractions = []
        for c in contours:
            if cv2.contourArea(c) >= self.ROI_area:
                areas.append(cv2.contourArea(c))
                extractions.append(cv2.boundingRect(c))
        if areas:
            extractions = extractions[:np.argmax(areas)]
            # Saves all the possible holes
            maxy, maxx = _mask.shape
            # max and min are needed because sometimes the indexes are negative or greather than the shape
            # the ratio of pixels is calculated here in order to modify the ROI
            delta_ratio = self.delta_ratio if self.delta_ratio else random.random() / 5 + 0.9
            self.holes = [[
                slice(int(1 / delta_ratio * max(0, extraction[0])), int(delta_ratio * min(maxx, extraction[0] + extraction[2]))),
                slice(int(1 / delta_ratio * max(0, extraction[1])), int(delta_ratio * min(maxy, extraction[1] + extraction[3])))]
                for extraction in extractions]
        else:
            self.holes = []
    
    def get_hole(self,
             mask: np.ndarray): # The mask associated with the image where the holes are going to be made.
        "Defines how to make the hole."
        _mask = mask.cpu()
        if np.array_equal(self.mask, _mask) and self.holes:
            return self.holes.pop()
        else:
            self.mask = np.copy(_mask)
            self.__get_holes__(_mask)
            if self.holes:
                return self.get_hole(_mask)
            else:
                return [slice(0), slice(0)]