__all__=(
    "router",
    "admin_router",
    "yandex_router",
    "vk_router"
)

from .router import router
from .admin_router import admin_router
from .yandex_router import router as yandex_router
from .vk_router import router as vk_router