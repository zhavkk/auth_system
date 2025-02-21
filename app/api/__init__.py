__all__=(
    "router",
    "admin_router",
    "yandex_router",
    "vk_router"
)

from api.api_v1 import router
from api.api_v1 import admin_router
from api.api_v1 import yandex_router
from api.api_v1 import vk_router