# Release notes

<!-- do not remove -->

## 0.0.10


### Bugs Squashed

- cv2 resize function ([#2](https://github.com/ruescog/semantic_segmentation_augmentations/issues/2))
  - The call to this function in class CutMixResizeMix is incorrect

- Name random is not defined ([#1](https://github.com/ruescog/semantic_segmentation_augmentations/issues/1))
  - It is needed to add the random module.
