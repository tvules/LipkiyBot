from io import BytesIO
from typing import Optional

from aiogram import Bot, types


async def download_user_avatar(
    bot: Bot, user: types.User
) -> Optional[BytesIO]:
    """Download a current user profile photo."""

    avatars = await bot.get_user_profile_photos(user_id=user.id, limit=1)
    if not avatars.total_count:
        return None

    return await bot.download(avatars.photos[-1][-1], destination=BytesIO())
