from .user import *
from .book import *
from .chat import *
from .deal import *


UserDetailResponse.model_rebuild()
BookDetailResponse.model_rebuild()
ChatWithMessagesResponse.model_rebuild()

DealResponse.model_rebuild()
DealDetailResponse.model_rebuild()

MessageResponse.model_rebuild()