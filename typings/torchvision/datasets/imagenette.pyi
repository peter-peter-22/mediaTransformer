"""
This type stub file was generated by pyright.
"""

from pathlib import Path
from typing import Any, Callable, Optional, Tuple, Union
from .vision import VisionDataset

class Imagenette(VisionDataset):
    """`Imagenette <https://github.com/fastai/imagenette#imagenette-1>`_ image classification dataset.

    Args:
        root (str or ``pathlib.Path``): Root directory of the Imagenette dataset.
        split (string, optional): The dataset split. Supports ``"train"`` (default), and ``"val"``.
        size (string, optional): The image size. Supports ``"full"`` (default), ``"320px"``, and ``"160px"``.
        download (bool, optional): If ``True``, downloads the dataset components and places them in ``root``. Already
            downloaded archives are not downloaded again.
        transform (callable, optional): A function/transform that takes in a PIL image or torch.Tensor, depends on the given loader,
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the target and transforms it.
        loader (callable, optional): A function to load an image given its path.
            By default, it uses PIL as its image loader, but users could also pass in
            ``torchvision.io.decode_image`` for decoding image data into tensors directly.

     Attributes:
        classes (list): List of the class name tuples.
        class_to_idx (dict): Dict with items (class name, class index).
        wnids (list): List of the WordNet IDs.
        wnid_to_idx (dict): Dict with items (WordNet ID, class index).
    """
    _ARCHIVES = ...
    _WNID_TO_CLASS = ...
    def __init__(self, root: Union[str, Path], split: str = ..., size: str = ..., download=..., transform: Optional[Callable] = ..., target_transform: Optional[Callable] = ..., loader: Callable[[str], Any] = ...) -> None:
        ...
    
    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        ...
    
    def __len__(self) -> int:
        ...
    


