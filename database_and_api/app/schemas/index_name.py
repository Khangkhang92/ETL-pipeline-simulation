from .base import BaseORMResponse
from .index_frame_h1 import IndexFrameH1Response
from .index_frame_m1 import IndexFrameM1Response
from typing import List, Optional


class IndexNameResponse(BaseORMResponse):
    id: Optional[int]
    index_id: Optional[str]
    frame_h1: Optional[List[IndexFrameH1Response]]
    # frame_m1: Optional[List[IndexFrameM1Response]]
