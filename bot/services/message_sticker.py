from io import BytesIO
from operator import itemgetter
from pathlib import Path
from typing import Optional

from aiogram import Bot
from aiogram.types import User
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pilmoji import Pilmoji
from pilmoji.source import AppleEmojiSource
from pydantic import BaseModel, NonNegativeInt, PositiveInt
from pydantic.color import Color

from bot.utils import download_user_avatar


class FontProperties(BaseModel):
    path: Path
    size: PositiveInt
    fill: Color
    spacing: int = 4


class AvatarProperties(BaseModel):
    image_size: tuple[PositiveInt, PositiveInt] = (85, 85)
    font: FontProperties = FontProperties(
        path=Path("assets/fonts/SF-Pro-Display-Semibold.otf"),
        size=40,
        fill=Color("#8e9092"),
    )
    fill: Color = Color("#dfdfdf")


class TitleProperties(BaseModel):
    font: FontProperties = FontProperties(
        path=Path("assets/fonts/SF-Pro-Display-Semibold.otf"),
        size=34,
        fill=Color("#212529"),
    )


class TextProperties(BaseModel):
    font: FontProperties = FontProperties(
        path=Path("assets/fonts/SF-Pro-Display-Regular.otf"),
        size=36,
        fill=Color("#212529"),
    )
    indent: int = -4


class BodyProperties(BaseModel):
    title: TitleProperties = TitleProperties()
    text: TextProperties = TextProperties()
    x_offset: PositiveInt = 15


class MsgStickerProperties(BaseModel):
    """Configuration for drawing a common"""

    width: PositiveInt = 512
    height: Optional[PositiveInt]
    fill: Color = Color("#f5f5f5")
    padding: NonNegativeInt = 15
    radius: NonNegativeInt = 30
    avatar: AvatarProperties = AvatarProperties()
    body: BodyProperties = BodyProperties()


class MessageAuthor(BaseModel):
    first_name: str
    last_name: Optional[str]
    avatar: Optional[BytesIO]

    class Config:
        arbitrary_types_allowed = True


class MsgSticker:
    text: str
    author: MessageAuthor
    _properties: MsgStickerProperties = MsgStickerProperties()

    def __init__(
        self,
        text: str,
        author: MessageAuthor,
        *,
        properties: Optional[MsgStickerProperties] = None,
    ) -> None:
        if properties is not None:
            self._properties = properties
        self.author = author
        self.text = text

    @property
    def _title_font(self) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(
            font=str(self._properties.body.title.font.path),
            size=self._properties.body.title.font.size,
        )

    @property
    def _text_font(self) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(
            font=str(self._properties.body.text.font.path),
            size=self._properties.body.text.font.size,
        )

    @property
    def _avatar_font(self) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(
            font=str(self._properties.avatar.font.path),
            size=self._properties.avatar.font.size,
        )

    @property
    def _author_name(self) -> str:
        if not self.author.last_name:
            return self.author.first_name
        return f"{self.author.first_name} {self.author.last_name}"

    def _make_circular(self, image: Image.Image) -> Image.Image:
        _size = min(image.size)
        mask = Image.new(mode="L", size=(_size * 2, _size * 2), color=0)
        ImageDraw.Draw(mask).ellipse(
            xy=(0, 0, mask.size[0] - 1, mask.size[1] - 1), fill=255
        )
        mask = mask.resize(size=(_size, _size), resample=Image.LANCZOS)

        image = ImageOps.fit(image=image, size=mask.size, centering=(0.5, 0.5))
        image.putalpha(alpha=mask)

        return image

    def _generate_default_avatar(self) -> Image.Image:
        image = Image.new(
            mode="RGBA",
            size=self._properties.avatar.image_size,
            color=self._properties.avatar.fill.as_hex(),
        )
        author_initials = "".join(
            map(itemgetter(0), self._author_name.split())
        ).upper()
        ImageDraw.Draw(image).text(
            xy=(image.size[0] // 2, image.size[1] // 2),
            text=author_initials,
            font=self._avatar_font,
            fill=self._properties.avatar.font.fill.as_hex(),
            anchor="mm",
        )
        return image

    def _get_circular_avatar(self) -> Image.Image:
        if not self.author.avatar:
            image = self._generate_default_avatar()
        else:
            image = Image.open(self.author.avatar).resize(
                self._properties.avatar.image_size
            )
        return self._make_circular(image)

    def _get_wrapped_text(
        self, text: str, font: ImageFont.FreeTypeFont, line_length: int
    ) -> str:
        lines = [""]
        for word in text.split():
            line = f"{lines[-1]} {word}".strip()
            if font.getlength(text=line) <= line_length:
                lines[-1] = line
            else:
                lines.append(word)
        return "\n".join(lines)

    def _create_base(self, size: tuple[int, int]) -> Image.Image:
        image = Image.new("RGBA", size=(size[0] * 2, size[1] * 2))
        ImageDraw.Draw(image).rounded_rectangle(
            xy=((0, 0), (image.size[0] - 1, image.size[1] - 1)),
            radius=self._properties.radius * 2,
            fill=self._properties.fill.as_hex(),
            width=0,
        )
        return image.resize(size)

    def _get_text_bbox(
        self, text: str, font: ImageFont.FreeTypeFont, spacing=4
    ) -> tuple[int, int, int, int]:
        _draw = ImageDraw.Draw(Image.new(mode="L", size=(0, 0), color=0))
        return _draw.textbbox(xy=(0, 0), text=text, font=font, spacing=spacing)

    def draw(self) -> Image.Image:
        avatar = self._get_circular_avatar()

        body_width = self._properties.width - (
            self._properties.padding * 2
            + avatar.size[0]
            + self._properties.body.x_offset
        )

        title = self._author_name
        text = self._get_wrapped_text(self.text, self._text_font, body_width)
        title_height = sum(self._title_font.getmetrics())
        text_height = self._get_text_bbox(text, self._text_font)[3]

        body_height = (
            title_height + text_height + self._properties.body.text.indent + 5
        )
        min_height = self._properties.padding * 2
        height = max(min_height + avatar.size[1], min_height + body_height)
        sticker = self._create_base((self._properties.width, height))

        body_x_offset = self._properties.padding
        body_y_offset = self._properties.padding

        sticker.alpha_composite(
            avatar, (body_x_offset, sticker.size[1] // 2 - avatar.size[1] // 2)
        )
        body_x_offset += avatar.size[0] + self._properties.body.x_offset

        with Pilmoji(
            sticker, source=AppleEmojiSource, emoji_position_offset=(0, 5)
        ) as pilmoji:
            pilmoji.text(
                xy=(body_x_offset, body_y_offset),
                text=title,
                fill=self._properties.body.title.font.fill.as_hex(),
                font=self._title_font,
            )
            body_y_offset += title_height + self._properties.body.text.indent

            pilmoji.text(
                xy=(body_x_offset, body_y_offset),
                text=text,
                fill=self._properties.body.text.font.fill.as_hex(),
                font=self._text_font,
            )

        return sticker


async def create_sticker_image(bot: Bot, author: User, text: str) -> BytesIO:
    """Create a sticker from"""

    avatar = await download_user_avatar(bot=bot, user=author)
    author = MessageAuthor(
        first_name=author.first_name, last_name=author.last_name, avatar=avatar
    )
    sticker = MsgSticker(author=author, text=text)

    file = BytesIO()
    sticker.draw().save(fp=file, format="png")
    file.seek(0)

    return file
