semantic_segmentation_augmentations
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

Data augmentation is a regularisation technique that generates new
training samples from the original dataset by applying colour or
geometric transformations. Although this technique has been applied in
other computer vision fields, such as image classification or object
detection, the application of this technique in semantic segmentation is
not yet widespread.

This library groups some data augmentation techniques for semantic
augmentation, such as `CutOut` or `CutMix`.

# Install

To install the library, run:

``` sh
pip install semantic_segmentation_augmentations
```

# How it works

This data augmentation techniques are defined as `fastai` `callbacks`.
Given this fact, you need to train your models using `fastai`’s API to
use them.

As these techniques modifies the input image changing some pixels
regions for something else, those callbacks have been defined as the
union of two subcomponents: the
[`HoleMakerTechnique`](https://ruescog.github.io/semantic_segmentation_augmentations/iholemakertechnique.html#holemakertechnique),
that defines how to make the hole (how to select the region to replace)
and the
[`HolesFilling`](https://ruescog.github.io/semantic_segmentation_augmentations/iholesfilling.html#holesfilling),
that defines how to fill the region defined below (the way to fill the
region gives the name to the technique used).

The
[`HoleMakerTechnique`](https://ruescog.github.io/semantic_segmentation_augmentations/iholemakertechnique.html#holemakertechnique)
can be replaced in order to change the behavior of the selection of the
region to replace. Doing so, you can use a CutOut technique that select
the region randomly or based on the information bounded in that region.

You can also define your custom techniques defining how to fill a hole.
You just need to extend the
[`HolesFilling`](https://ruescog.github.io/semantic_segmentation_augmentations/iholesfilling.html#holesfilling)
class and define the `before_bacth` (remember: we are using `callbacks`
from `fastai`) abstract method. You will have two methods to simplify
the process: the `make_hole` function, that uses the selected
[`HoleMakerTechnique`](https://ruescog.github.io/semantic_segmentation_augmentations/iholemakertechnique.html#holemakertechnique)
to make the hole and returns two slices (the region boundaries) and the
`fill_hole` function, that fills the hole with something.

# How to use it

In order to use these techniques, you just need to define the `Learner`
from `fastai` with the `Callbacks` that represent the techniques that
you want to use.

For example, if you want to create an `U-net` `Leaner` with `resnet18`
backbone and use the CutOut technique with
[`HoleMakerRandom`](https://ruescog.github.io/semantic_segmentation_augmentations/holemakerrandom.html#holemakerrandom)
as region selection techinique (which is the default one), you just need
to import it:

``` sh
from semantic_segmentation_augmentations.holesfilling import CutOutRandom
```

And add it to your learner:

``` sh
learner = unet_learner(dls, resnet18, cbs = CutOutRandom(hole_maker = HoleMakerRandom()))
```

If you want to change the default behaviour of the CutOutRandom
technique (i. e. to select the region with a
[`HoleMakerAttention`](https://ruescog.github.io/semantic_segmentation_augmentations/holemakerattention.html#holemakerattention)
technique), you just need to define the technique as follows:

``` sh
learner = unet_learner(dls, resnet18, cbs = CutOutRandom(hole_maker = HoleMakerAttention(attention_threshold = 0.25, hole_size = (150, 150))))
```

Finally, you can apply geometrical augments to the selected regions
(using the `Albumentations` augments). Maybe this augmnets are not
useful with the `CutOut` techniques, but with the `CutMix` ones. In
order to do so, you just need to implement a
[`RegionModifier`](https://ruescog.github.io/semantic_segmentation_augmentations/regionmodifier.html#regionmodifier)
with a list with the augments to apply:

``` sh
learner = unet_learner( dls,
                        resnet18,
                        cbs = CutMixRandom( holes_num = 1,
                                            modifier = RegionModifier(A.Compose([A.Blur(), A.GaussNoise()])),
                                            hole_maker = HoleMakerRandom((250, 250)),
                                            p = 1
                        )
                      )
```
