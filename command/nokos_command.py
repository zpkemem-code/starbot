from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler
from helpers.buttons import ButtonUtils


async def cb_shop(_, callback: CallbackQuery):
    category_id = callback.data.split()
    text, button = await ButtonUtils.nokos(0, category_id[1])
    return await callback.edit_message_text(
          text, reply_markup=button
    )


async def cb_page_shop(_, callback: CallbackQuery):
    data = callback.data.split("_")

    page = int(data[2])
    category_id = data[3]

    if category_id == "all":
        category_id = None

    text, button = await ButtonUtils.nokos(page, category_id)

    return await callback.edit_message_text(
        text,
        reply_markup=button
    )

async def open_nokos(client, message):
    text, button = await ButtonUtils.nokos()

    return await message.reply(
        text,
        reply_markup=button,
    )


async def open_nokos_cb(_, callback: CallbackQuery):
    text, button = await ButtonUtils.nokos()

    return await callback.edit_message_text(
        text,
        reply_markup=button,
    )
