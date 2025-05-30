"""
This type stub file was generated by pyright.
"""

import pathlib
import torch
from typing import BinaryIO, List, Optional, Tuple, Union

__all__ = ["make_grid", "save_image", "draw_bounding_boxes", "draw_segmentation_masks", "draw_keypoints", "flow_to_image"]
@torch.no_grad()
def make_grid(tensor: Union[torch.Tensor, List[torch.Tensor]], nrow: int = ..., padding: int = ..., normalize: bool = ..., value_range: Optional[Tuple[int, int]] = ..., scale_each: bool = ..., pad_value: float = ...) -> torch.Tensor:
    """
    Make a grid of images.

    Args:
        tensor (Tensor or list): 4D mini-batch Tensor of shape (B x C x H x W)
            or a list of images all of the same size.
        nrow (int, optional): Number of images displayed in each row of the grid.
            The final grid size is ``(B / nrow, nrow)``. Default: ``8``.
        padding (int, optional): amount of padding. Default: ``2``.
        normalize (bool, optional): If True, shift the image to the range (0, 1),
            by the min and max values specified by ``value_range``. Default: ``False``.
        value_range (tuple, optional): tuple (min, max) where min and max are numbers,
            then these numbers are used to normalize the image. By default, min and max
            are computed from the tensor.
        scale_each (bool, optional): If ``True``, scale each image in the batch of
            images separately rather than the (min, max) over all images. Default: ``False``.
        pad_value (float, optional): Value for the padded pixels. Default: ``0``.

    Returns:
        grid (Tensor): the tensor containing grid of images.
    """
    ...

@torch.no_grad()
def save_image(tensor: Union[torch.Tensor, List[torch.Tensor]], fp: Union[str, pathlib.Path, BinaryIO], format: Optional[str] = ..., **kwargs) -> None:
    """
    Save a given Tensor into an image file.

    Args:
        tensor (Tensor or list): Image to be saved. If given a mini-batch tensor,
            saves the tensor as a grid of images by calling ``make_grid``.
        fp (string or file object): A filename or a file object
        format(Optional):  If omitted, the format to use is determined from the filename extension.
            If a file object was used instead of a filename, this parameter should always be used.
        **kwargs: Other arguments are documented in ``make_grid``.
    """
    ...

@torch.no_grad()
def draw_bounding_boxes(image: torch.Tensor, boxes: torch.Tensor, labels: Optional[List[str]] = ..., colors: Optional[Union[List[Union[str, Tuple[int, int, int]]], str, Tuple[int, int, int]]] = ..., fill: Optional[bool] = ..., width: int = ..., font: Optional[str] = ..., font_size: Optional[int] = ..., label_colors: Optional[Union[List[Union[str, Tuple[int, int, int]]], str, Tuple[int, int, int]]] = ...) -> torch.Tensor:
    """
    Draws bounding boxes on given RGB image.
    The image values should be uint8 in [0, 255] or float in [0, 1].
    If fill is True, Resulting Tensor should be saved as PNG image.

    Args:
        image (Tensor): Tensor of shape (C, H, W) and dtype uint8 or float.
        boxes (Tensor): Tensor of size (N, 4) containing bounding boxes in (xmin, ymin, xmax, ymax) format. Note that
            the boxes are absolute coordinates with respect to the image. In other words: `0 <= xmin < xmax < W` and
            `0 <= ymin < ymax < H`.
        labels (List[str]): List containing the labels of bounding boxes.
        colors (color or list of colors, optional): List containing the colors
            of the boxes or single color for all boxes. The color can be represented as
            PIL strings e.g. "red" or "#FF00FF", or as RGB tuples e.g. ``(240, 10, 157)``.
            By default, random colors are generated for boxes.
        fill (bool): If `True` fills the bounding box with specified color.
        width (int): Width of bounding box.
        font (str): A filename containing a TrueType font. If the file is not found in this filename, the loader may
            also search in other directories, such as the `fonts/` directory on Windows or `/Library/Fonts/`,
            `/System/Library/Fonts/` and `~/Library/Fonts/` on macOS.
        font_size (int): The requested font size in points.
        label_colors (color or list of colors, optional): Colors for the label text.  See the description of the
            `colors` argument for details.  Defaults to the same colors used for the boxes.

    Returns:
        img (Tensor[C, H, W]): Image Tensor of dtype uint8 with bounding boxes plotted.

    """
    ...

@torch.no_grad()
def draw_segmentation_masks(image: torch.Tensor, masks: torch.Tensor, alpha: float = ..., colors: Optional[Union[List[Union[str, Tuple[int, int, int]]], str, Tuple[int, int, int]]] = ...) -> torch.Tensor:
    """
    Draws segmentation masks on given RGB image.
    The image values should be uint8 in [0, 255] or float in [0, 1].

    Args:
        image (Tensor): Tensor of shape (3, H, W) and dtype uint8 or float.
        masks (Tensor): Tensor of shape (num_masks, H, W) or (H, W) and dtype bool.
        alpha (float): Float number between 0 and 1 denoting the transparency of the masks.
            0 means full transparency, 1 means no transparency.
        colors (color or list of colors, optional): List containing the colors
            of the masks or single color for all masks. The color can be represented as
            PIL strings e.g. "red" or "#FF00FF", or as RGB tuples e.g. ``(240, 10, 157)``.
            By default, random colors are generated for each mask.

    Returns:
        img (Tensor[C, H, W]): Image Tensor, with segmentation masks drawn on top.
    """
    ...

@torch.no_grad()
def draw_keypoints(image: torch.Tensor, keypoints: torch.Tensor, connectivity: Optional[List[Tuple[int, int]]] = ..., colors: Optional[Union[str, Tuple[int, int, int]]] = ..., radius: int = ..., width: int = ..., visibility: Optional[torch.Tensor] = ...) -> torch.Tensor:
    """
    Draws Keypoints on given RGB image.
    The image values should be uint8 in [0, 255] or float in [0, 1].
    Keypoints can be drawn for multiple instances at a time.

    This method allows that keypoints and their connectivity are drawn based on the visibility of this keypoint.

    Args:
        image (Tensor): Tensor of shape (3, H, W) and dtype uint8 or float.
        keypoints (Tensor): Tensor of shape (num_instances, K, 2) the K keypoint locations for each of the N instances,
            in the format [x, y].
        connectivity (List[Tuple[int, int]]]): A List of tuple where each tuple contains a pair of keypoints
            to be connected.
            If at least one of the two connected keypoints has a ``visibility`` of False,
            this specific connection is not drawn.
            Exclusions due to invisibility are computed per-instance.
        colors (str, Tuple): The color can be represented as
            PIL strings e.g. "red" or "#FF00FF", or as RGB tuples e.g. ``(240, 10, 157)``.
        radius (int): Integer denoting radius of keypoint.
        width (int): Integer denoting width of line connecting keypoints.
        visibility (Tensor): Tensor of shape (num_instances, K) specifying the visibility of the K
            keypoints for each of the N instances.
            True means that the respective keypoint is visible and should be drawn.
            False means invisible, so neither the point nor possible connections containing it are drawn.
            The input tensor will be cast to bool.
            Default ``None`` means that all the keypoints are visible.
            For more details, see :ref:`draw_keypoints_with_visibility`.

    Returns:
        img (Tensor[C, H, W]): Image Tensor with keypoints drawn.
    """
    ...

@torch.no_grad()
def flow_to_image(flow: torch.Tensor) -> torch.Tensor:
    """
    Converts a flow to an RGB image.

    Args:
        flow (Tensor): Flow of shape (N, 2, H, W) or (2, H, W) and dtype torch.float.

    Returns:
        img (Tensor): Image Tensor of dtype uint8 where each color corresponds
            to a given flow direction. Shape is (N, 3, H, W) or (3, H, W) depending on the input.
    """
    ...

