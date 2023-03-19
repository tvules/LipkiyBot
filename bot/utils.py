from io import BytesIO
from typing import Optional, Union

import shortuuid
from aiogram import Bot
from aiogram.types import User

from bot.config import settings


async def download_user_avatar(bot: Bot, user: User) -> Optional[BytesIO]:
    """Download a current user profile photo."""

    avatars = await bot.get_user_profile_photos(user_id=user.id, limit=1)
    if not avatars.total_count:
        return None

    return await bot.download(avatars.photos[-1][-1], destination=BytesIO())


def create_uuid_from_user_id(user_id: Union[int, str]) -> str:
    """Create a short URL-safe uuid5 from user_id."""

    return shortuuid.uuid(str(user_id) + settings.secret.get_secret_value())
