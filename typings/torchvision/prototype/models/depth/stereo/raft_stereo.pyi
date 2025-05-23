"""
This type stub file was generated by pyright.
"""

import torch.nn as nn
import torchvision.models.optical_flow.raft as raft
from typing import Callable, List, Optional, Tuple
from torch import Tensor
from torchvision.models._api import WeightsEnum, register_model
from torchvision.models._utils import handle_legacy_interface
from torchvision.models.optical_flow.raft import MotionEncoder

__all__ = ("RaftStereo", "raft_stereo_base", "raft_stereo_realtime", "Raft_Stereo_Base_Weights", "Raft_Stereo_Realtime_Weights")
class BaseEncoder(raft.FeatureEncoder):
    """Base encoder for FeatureEncoder and ContextEncoder in which weight may be shared.

    See the Raft-Stereo paper section 4.6 on backbone part.
    """
    def __init__(self, *, block: Callable[..., nn.Module] = ..., layers: Tuple[int, int, int, int] = ..., strides: Tuple[int, int, int, int] = ..., norm_layer: Callable[..., nn.Module] = ...) -> None:
        ...
    


class FeatureEncoder(nn.Module):
    """Feature Encoder for Raft-Stereo (see paper section 3.1) that may have shared weight with the Context Encoder.

    The FeatureEncoder takes concatenation of left and right image as input. It produces feature embedding that later
    will be used to construct correlation volume.
    """
    def __init__(self, base_encoder: BaseEncoder, output_dim: int = ..., shared_base: bool = ..., block: Callable[..., nn.Module] = ...) -> None:
        ...
    
    def forward(self, x: Tensor) -> Tensor:
        ...
    


class MultiLevelContextEncoder(nn.Module):
    """Context Encoder for Raft-Stereo (see paper section 3.1) that may have shared weight with the Feature Encoder.

    The ContextEncoder takes left image as input, and it outputs concatenated hidden_states and contexts.
    In Raft-Stereo we have multi level GRUs and this context encoder will also multi outputs (list of Tensor)
    that correspond to each GRUs.
    Take note that the length of "out_with_blocks" parameter represent the number of GRU's level.
    args:
        base_encoder (nn.Module): The base encoder part that can have a shared weight with feature_encoder's
            base_encoder because they have same architecture.
        out_with_blocks (List[bool]): The length represent the number of GRU's level (length of output), and
            if the element is True then the output layer on that position will have additional block
        output_dim (int): The dimension of output on each level (default: 256)
        block (Callable[..., nn.Module]): The type of basic block used for downsampling and output layer
            (default: ResidualBlock)
    """
    def __init__(self, base_encoder: nn.Module, out_with_blocks: List[bool], output_dim: int = ..., block: Callable[..., nn.Module] = ...) -> None:
        ...
    
    def forward(self, x: Tensor) -> List[Tensor]:
        ...
    


class ConvGRU(raft.ConvGRU):
    """Convolutional Gru unit."""
    def forward(self, h: Tensor, x: Tensor, context: List[Tensor]) -> Tensor:
        ...
    


class MultiLevelUpdateBlock(nn.Module):
    """The update block which contains the motion encoder and grus

    It must expose a ``hidden_dims`` attribute which is the hidden dimension size of its gru blocks
    """
    def __init__(self, *, motion_encoder: MotionEncoder, hidden_dims: List[int]) -> None:
        ...
    
    def forward(self, hidden_states: List[Tensor], contexts: List[List[Tensor]], corr_features: Tensor, disparity: Tensor, level_processed: List[bool]) -> List[Tensor]:
        ...
    


class MaskPredictor(raft.MaskPredictor):
    """Mask predictor to be used when upsampling the predicted disparity."""
    def __init__(self, *, in_channels: int, hidden_size: int, out_channels: int, multiplier: float = ...) -> None:
        ...
    


class CorrPyramid1d(nn.Module):
    """Row-wise correlation pyramid.

    Create a row-wise correlation pyramid with ``num_levels`` level from the outputs of the feature encoder,
    this correlation pyramid will later be used as index to create correlation features using CorrBlock1d.
    """
    def __init__(self, num_levels: int = ...) -> None:
        ...
    
    def forward(self, fmap1: Tensor, fmap2: Tensor) -> List[Tensor]:
        """Build the correlation pyramid from two feature maps.

        The correlation volume is first computed as the dot product of each pair (pixel_in_fmap1, pixel_in_fmap2) on the same row.
        The last 2 dimensions of the correlation volume are then pooled num_levels times at different resolutions
        to build the correlation pyramid.
        """
        ...
    


class CorrBlock1d(nn.Module):
    """The row-wise correlation block.

    Use indexes from correlation pyramid to create correlation features.
    The "indexing" of a given centroid pixel x' is done by concatenating its surrounding row neighbours
    within radius
    """
    def __init__(self, *, num_levels: int = ..., radius: int = ...) -> None:
        ...
    
    def forward(self, centroids_coords: Tensor, corr_pyramid: List[Tensor]) -> Tensor:
        """Return correlation features by indexing from the pyramid."""
        ...
    


class RaftStereo(nn.Module):
    def __init__(self, *, feature_encoder: FeatureEncoder, context_encoder: MultiLevelContextEncoder, corr_pyramid: CorrPyramid1d, corr_block: CorrBlock1d, update_block: MultiLevelUpdateBlock, disparity_head: nn.Module, mask_predictor: Optional[nn.Module] = ..., slow_fast: bool = ...) -> None:
        """RAFT-Stereo model from
        `RAFT-Stereo: Multilevel Recurrent Field Transforms for Stereo Matching <https://arxiv.org/abs/2109.07547>`_.

        args:
            feature_encoder (FeatureEncoder): The feature encoder. Its input is the concatenation of ``left_image`` and ``right_image``.
            context_encoder (MultiLevelContextEncoder): The context encoder. Its input is ``left_image``.
                It has multi-level output and each level will have 2 parts:

                - one part will be used as the actual "context", passed to the recurrent unit of the ``update_block``
                - one part will be used to initialize the hidden state of the recurrent unit of
                  the ``update_block``

            corr_pyramid (CorrPyramid1d): Module to build the correlation pyramid from feature encoder output
            corr_block (CorrBlock1d): The correlation block, which uses the correlation pyramid indexes
                to create correlation features. It takes the coordinate of the centroid pixel and correlation pyramid
                as input and returns the correlation features.
                It must expose an ``out_channels`` attribute.

            update_block (MultiLevelUpdateBlock): The update block, which contains the motion encoder, and the recurrent unit.
                It takes as input the hidden state of its recurrent unit, the context, the correlation
                features, and the current predicted disparity. It outputs an updated hidden state
            disparity_head (nn.Module): The disparity head block will convert from the hidden state into changes in disparity.
            mask_predictor (nn.Module, optional): Predicts the mask that will be used to upsample the predicted flow.
                If ``None`` (default), the flow is upsampled using interpolation.
            slow_fast (bool): A boolean that specify whether we should use slow-fast GRU or not. See RAFT-Stereo paper
                on section 3.4 for more detail.
        """
        ...
    
    def forward(self, left_image: Tensor, right_image: Tensor, flow_init: Optional[Tensor] = ..., num_iters: int = ...) -> List[Tensor]:
        """
        Return disparity predictions on every iteration as a list of Tensor.
        args:
            left_image (Tensor): The input left image with layout B, C, H, W
            right_image (Tensor): The input right image with layout B, C, H, W
            flow_init (Optional[Tensor]): Initial estimate for the disparity. Default: None
            num_iters (int): Number of update block iteration on the largest resolution. Default: 12
        """
        ...
    


class Raft_Stereo_Realtime_Weights(WeightsEnum):
    SCENEFLOW_V1 = ...
    DEFAULT = ...


class Raft_Stereo_Base_Weights(WeightsEnum):
    SCENEFLOW_V1 = ...
    MIDDLEBURY_V1 = ...
    ETH3D_V1 = ...
    DEFAULT = ...


@register_model()
@handle_legacy_interface(weights=("pretrained", None))
def raft_stereo_realtime(*, weights: Optional[Raft_Stereo_Realtime_Weights] = ..., progress=..., **kwargs) -> RaftStereo:
    """RAFT-Stereo model from
    `RAFT-Stereo: Multilevel Recurrent Field Transforms for Stereo Matching <https://arxiv.org/abs/2109.07547>`_.
    This is the realtime variant of the Raft-Stereo model that is described on the paper section 4.7.

    Please see the example below for a tutorial on how to use this model.

    Args:
        weights(:class:`~torchvision.prototype.models.depth.stereo.Raft_Stereo_Realtime_Weights`, optional): The
            pretrained weights to use. See
            :class:`~torchvision.prototype.models.depth.stereo.Raft_Stereo_Realtime_Weights`
            below for more details, and possible values. By default, no
            pre-trained weights are used.
        progress (bool): If True, displays a progress bar of the download to stderr. Default is True.
        **kwargs: parameters passed to the ``torchvision.prototype.models.depth.stereo.raft_stereo.RaftStereo``
            base class. Please refer to the `source code
            <https://github.com/pytorch/vision/blob/main/torchvision/models/optical_flow/raft.py>`_
            for more details about this class.

    .. autoclass:: torchvision.prototype.models.depth.stereo.Raft_Stereo_Realtime_Weights
        :members:
    """
    ...

@register_model()
@handle_legacy_interface(weights=("pretrained", None))
def raft_stereo_base(*, weights: Optional[Raft_Stereo_Base_Weights] = ..., progress=..., **kwargs) -> RaftStereo:
    """RAFT-Stereo model from
    `RAFT-Stereo: Multilevel Recurrent Field Transforms for Stereo Matching <https://arxiv.org/abs/2109.07547>`_.

    Please see the example below for a tutorial on how to use this model.

    Args:
        weights(:class:`~torchvision.prototype.models.depth.stereo.Raft_Stereo_Base_Weights`, optional): The
            pretrained weights to use. See
            :class:`~torchvision.prototype.models.depth.stereo.Raft_Stereo_Base_Weights`
            below for more details, and possible values. By default, no
            pre-trained weights are used.
        progress (bool): If True, displays a progress bar of the download to stderr. Default is True.
        **kwargs: parameters passed to the ``torchvision.prototype.models.depth.stereo.raft_stereo.RaftStereo``
            base class. Please refer to the `source code
            <https://github.com/pytorch/vision/blob/main/torchvision/models/optical_flow/raft.py>`_
            for more details about this class.

    .. autoclass:: torchvision.prototype.models.depth.stereo.Raft_Stereo_Base_Weights
        :members:
    """
    ...

