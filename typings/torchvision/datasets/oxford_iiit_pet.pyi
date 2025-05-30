"""
This type stub file was generated by pyright.
"""

import pathlib
from typing import Any, Callable, Optional, Sequence, Tuple, Union
from .vision import VisionDataset

class OxfordIIITPet(VisionDataset):
    """`Oxford-IIIT Pet Dataset   <https://www.robots.ox.ac.uk/~vgg/data/pets/>`_.

    Args:
        root (str or ``pathlib.Path``): Root directory of the dataset.
        split (string, optional): The dataset split, supports ``"trainval"`` (default) or ``"test"``.
        target_types (string, sequence of strings, optional): Types of target to use. Can be ``category`` (default) or
            ``segmentation``. Can also be a list to output a tuple with all specified target types. The types represent:

                - ``category`` (int): Label for one of the 37 pet categories.
                - ``binary-category`` (int): Binary label for cat or dog.
                - ``segmentation`` (PIL image): Segmentation trimap of the image.

            If empty, ``None`` will be returned as target.

        transform (callable, optional): A function/transform that takes in a PIL image and returns a transformed
            version. E.g, ``transforms.RandomCrop``.
        target_transform (callable, optional): A function/transform that takes in the target and transforms it.
        transforms (callable, optional): A function/transform that takes input sample
            and its target as entry and returns a transformed version.
        download (bool, optional): If True, downloads the dataset from the internet and puts it into
            ``root/oxford-iiit-pet``. If dataset is already downloaded, it is not downloaded again.
    """
    _RESOURCES = ...
    _VALID_TARGET_TYPES = ...
    def __init__(self, root: Union[str, pathlib.Path], split: str = ..., target_types: Union[Sequence[str], str] = ..., transforms: Optional[Callable] = ..., transform: Optional[Callable] = ..., target_transform: Optional[Callable] = ..., download: bool = ...) -> None:
        ...
    
    def __len__(self) -> int:
        ...
    
    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        ...
    


