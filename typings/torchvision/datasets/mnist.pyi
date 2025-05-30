"""
This type stub file was generated by pyright.
"""

import torch
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from .vision import VisionDataset

class MNIST(VisionDataset):
    """`MNIST <http://yann.lecun.com/exdb/mnist/>`_ Dataset.

    Args:
        root (str or ``pathlib.Path``): Root directory of dataset where ``MNIST/raw/train-images-idx3-ubyte``
            and  ``MNIST/raw/t10k-images-idx3-ubyte`` exist.
        train (bool, optional): If True, creates dataset from ``train-images-idx3-ubyte``,
            otherwise from ``t10k-images-idx3-ubyte``.
        transform (callable, optional): A function/transform that  takes in a PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        download (bool, optional): If True, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
    """
    mirrors = ...
    resources = ...
    training_file = ...
    test_file = ...
    classes = ...
    @property
    def train_labels(self): # -> Any | Tensor:
        ...
    
    @property
    def test_labels(self): # -> Any | Tensor:
        ...
    
    @property
    def train_data(self): # -> Any | Tensor:
        ...
    
    @property
    def test_data(self): # -> Any | Tensor:
        ...
    
    def __init__(self, root: Union[str, Path], train: bool = ..., transform: Optional[Callable] = ..., target_transform: Optional[Callable] = ..., download: bool = ...) -> None:
        ...
    
    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        """
        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is index of the target class.
        """
        ...
    
    def __len__(self) -> int:
        ...
    
    @property
    def raw_folder(self) -> str:
        ...
    
    @property
    def processed_folder(self) -> str:
        ...
    
    @property
    def class_to_idx(self) -> Dict[str, int]:
        ...
    
    def download(self) -> None:
        """Download the MNIST data if it doesn't exist already."""
        ...
    
    def extra_repr(self) -> str:
        ...
    


class FashionMNIST(MNIST):
    """`Fashion-MNIST <https://github.com/zalandoresearch/fashion-mnist>`_ Dataset.

    Args:
        root (str or ``pathlib.Path``): Root directory of dataset where ``FashionMNIST/raw/train-images-idx3-ubyte``
            and  ``FashionMNIST/raw/t10k-images-idx3-ubyte`` exist.
        train (bool, optional): If True, creates dataset from ``train-images-idx3-ubyte``,
            otherwise from ``t10k-images-idx3-ubyte``.
        transform (callable, optional): A function/transform that  takes in a PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        download (bool, optional): If True, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
    """
    mirrors = ...
    resources = ...
    classes = ...


class KMNIST(MNIST):
    """`Kuzushiji-MNIST <https://github.com/rois-codh/kmnist>`_ Dataset.

    Args:
        root (str or ``pathlib.Path``): Root directory of dataset where ``KMNIST/raw/train-images-idx3-ubyte``
            and  ``KMNIST/raw/t10k-images-idx3-ubyte`` exist.
        train (bool, optional): If True, creates dataset from ``train-images-idx3-ubyte``,
            otherwise from ``t10k-images-idx3-ubyte``.
        transform (callable, optional): A function/transform that  takes in a PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        download (bool, optional): If True, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
    """
    mirrors = ...
    resources = ...
    classes = ...


class EMNIST(MNIST):
    """`EMNIST <https://www.westernsydney.edu.au/bens/home/reproducible_research/emnist>`_ Dataset.

    Args:
        root (str or ``pathlib.Path``): Root directory of dataset where ``EMNIST/raw/train-images-idx3-ubyte``
            and  ``EMNIST/raw/t10k-images-idx3-ubyte`` exist.
        split (string): The dataset has 6 different splits: ``byclass``, ``bymerge``,
            ``balanced``, ``letters``, ``digits`` and ``mnist``. This argument specifies
            which one to use.
        train (bool, optional): If True, creates dataset from ``training.pt``,
            otherwise from ``test.pt``.
        download (bool, optional): If True, downloads the dataset from the internet and
            puts it in root directory. If dataset is already downloaded, it is not
            downloaded again.
        transform (callable, optional): A function/transform that  takes in a PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
    """
    url = ...
    md5 = ...
    splits = ...
    _merged_classes = ...
    _all_classes = ...
    classes_split_dict = ...
    def __init__(self, root: Union[str, Path], split: str, **kwargs: Any) -> None:
        ...
    
    @property
    def images_file(self) -> str:
        ...
    
    @property
    def labels_file(self) -> str:
        ...
    
    def download(self) -> None:
        """Download the EMNIST data if it doesn't exist already."""
        ...
    


class QMNIST(MNIST):
    """`QMNIST <https://github.com/facebookresearch/qmnist>`_ Dataset.

    Args:
        root (str or ``pathlib.Path``): Root directory of dataset whose ``raw``
            subdir contains binary files of the datasets.
        what (string,optional): Can be 'train', 'test', 'test10k',
            'test50k', or 'nist' for respectively the mnist compatible
            training set, the 60k qmnist testing set, the 10k qmnist
            examples that match the mnist testing set, the 50k
            remaining qmnist testing examples, or all the nist
            digits. The default is to select 'train' or 'test'
            according to the compatibility argument 'train'.
        compat (bool,optional): A boolean that says whether the target
            for each example is class number (for compatibility with
            the MNIST dataloader) or a torch vector containing the
            full qmnist information. Default=True.
        train (bool,optional,compatibility): When argument 'what' is
            not specified, this boolean decides whether to load the
            training set or the testing set.  Default: True.
        download (bool, optional): If True, downloads the dataset from
            the internet and puts it in root directory. If dataset is
            already downloaded, it is not downloaded again.
        transform (callable, optional): A function/transform that
            takes in a PIL image and returns a transformed
            version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform
            that takes in the target and transforms it.
    """
    subsets = ...
    resources: Dict[str, List[Tuple[str, str]]] = ...
    classes = ...
    def __init__(self, root: Union[str, Path], what: Optional[str] = ..., compat: bool = ..., train: bool = ..., **kwargs: Any) -> None:
        ...
    
    @property
    def images_file(self) -> str:
        ...
    
    @property
    def labels_file(self) -> str:
        ...
    
    def download(self) -> None:
        """Download the QMNIST data if it doesn't exist already.
        Note that we only download what has been asked for (argument 'what').
        """
        ...
    
    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        ...
    
    def extra_repr(self) -> str:
        ...
    


def get_int(b: bytes) -> int:
    ...

SN3_PASCALVINCENT_TYPEMAP = ...
def read_sn3_pascalvincent_tensor(path: str, strict: bool = ...) -> torch.Tensor:
    """Read a SN3 file in "Pascal Vincent" format (Lush file 'libidx/idx-io.lsh').
    Argument may be a filename, compressed filename, or file object.
    """
    ...

def read_label_file(path: str) -> torch.Tensor:
    ...

def read_image_file(path: str) -> torch.Tensor:
    ...

