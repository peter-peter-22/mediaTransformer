"""
This type stub file was generated by pyright.
"""

from pathlib import Path
from typing import Any, Callable, Optional, Tuple, Union
from .vision import VisionDataset

class Omniglot(VisionDataset):
    """`Omniglot <https://github.com/brendenlake/omniglot>`_ Dataset.

    Args:
        root (str or ``pathlib.Path``): Root directory of dataset where directory
            ``omniglot-py`` exists.
        background (bool, optional): If True, creates dataset from the "background" set, otherwise
            creates from the "evaluation" set. This terminology is defined by the authors.
        transform (callable, optional): A function/transform that takes in a PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        download (bool, optional): If true, downloads the dataset zip files from the internet and
            puts it in root directory. If the zip files are already downloaded, they are not
            downloaded again.
        loader (callable, optional): A function to load an image given its path.
            By default, it uses PIL as its image loader, but users could also pass in
            ``torchvision.io.decode_image`` for decoding image data into tensors directly.
    """
    folder = ...
    download_url_prefix = ...
    zips_md5 = ...
    def __init__(self, root: Union[str, Path], background: bool = ..., transform: Optional[Callable] = ..., target_transform: Optional[Callable] = ..., download: bool = ..., loader: Optional[Callable[[Union[str, Path]], Any]] = ...) -> None:
        ...
    
    def __len__(self) -> int:
        ...
    
    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        """
        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is index of the target character class.
        """
        ...
    
    def download(self) -> None:
        ...
    


