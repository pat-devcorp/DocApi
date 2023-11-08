from collections import namedtuple

StickerDTO = namedtuple("StickerDTO", ["sticker_id", "style", "name", "color", "size"])


class StickerInterface:
    @staticmethod
    def getMock():
        return StickerDTO(
            sticker_id="8901234123457",
            style="MNPA0984",
            name="SPRING JACKET",
            color="DARK CAMEL/#205",
            size="4Y",
        )

    @staticmethod
    def fromDict(params: dict) -> namedtuple:
        return {k: v for k, v in params if k in StickerDTO._fields}
