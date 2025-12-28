import telebot
from bot_instance import bot


def update_message_media(
    chat_id, message_id, photo_path, caption, parse_mode, reply_markup=None
):
    with open(file=photo_path, mode="rb") as photo:
        media = telebot.types.InputMediaPhoto(
            media=photo, caption=caption, parse_mode=parse_mode
        )

        bot.edit_message_media(
            chat_id=chat_id,
            message_id=message_id,
            media=media,
            reply_markup=reply_markup,
        )
