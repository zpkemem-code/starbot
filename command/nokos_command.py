import re

from pyrogram import Client, filters
from pyrogram.helpers import ikb, kb
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler
from helpers.buttons import ButtonUtils


async def cb_shop(_, callback: CallbackQuery):
    category_id = callback.data.split()[1]

    text, button = await ButtonUtils.nokos(
        0,
        category_id
    )

    return await callback.edit_message_text(
        text,
        reply_markup=button
    )


async def cb_page_shop(_, callback: CallbackQuery):
    data = callback.data.split("_")

    page = int(data[2])
    category_id = data[3]

    if category_id == "all":
        category_id = None

    text, button = await ButtonUtils.nokos(
        page,
        category_id
    )

    return await callback.edit_message_text(
        text,
        reply_markup=button
    )


async def open_nokos(client, message):
    text = """
<blockquote><b>📱 Beli Akun Telegram</b></blockquote>

📦 <b>Cek Stok</b> — Ketersediaan per tipe ID
📋 <b>Peraturan</b> — Baca sebelum beli
🧾 <b>Riwayat</b> — Histori transaksi Anda
🛒 <b>Order Akun</b> — Beli sekarang

<i>Beli akun Telegram siap pakai.</i>
"""

    buttons = kb(
        [
            [
                "📦 Cek Stok",
                "📋 Peraturan",
            ],
            [
                "🧾 Riwayat",
                "🛒 Order Akun",
            ],
            [
                "🏠 Beranda"
            ]
        ],
        resize_keyboard=True
    )

    return await message.reply(
        text,
        reply_markup=buttons,
    )


async def open_nokos_cb(_, callback: CallbackQuery):
    text = """
<blockquote><b>📱 Beli Akun Telegram</b></blockquote>

📦 <b>Cek Stok</b> — Ketersediaan per tipe ID
📋 <b>Peraturan</b> — Baca sebelum beli
🧾 <b>Riwayat</b> — Histori transaksi Anda
🛒 <b>Order Akun</b> — Beli sekarang

<i>Beli akun Telegram siap pakai.</i>
"""

    return await callback.edit_message_text(text)



async def get_otp_nokos(_: Client, callback: CallbackQuery):
    list_nokos = await db.get_nokos()

    nokos_id = callback.data.split()[1]

    for x in list_nokos:
        if str(x) == str(nokos_id):
            ph = x.get('phone')
    
    await callback.edit_message_text(
        f"login nokos menggunakan phone number {ph}!\n setelah login baru pencet tombol otp",
        reply_markup=ikb([[("get otp", f"notp {nokos_id}")]]),
    )


async def otp_nokos(_: Client, callback: CallbackQuery):
    list_nokos = await db.get_nokos()

    nokos_id = callback.data.split()[1]

    for x in list_nokos:
        if str(x) == str(nokos_id):
            ss = x.get('session')

    nk = Client(
        name=nokos_id,
        session_string=ss,
        in_memory=True
    )

    await nk.start()

    otp_code = None
    async for msg in nk.get_chat_history(777000, limit=5):
        if msg.text:
            match = re.search(r'\b\d{5}\b', msg.text)
            if match:
                raw_otp = match.group(0)
                otp_code = " ".join(raw_otp)
                break 
        
    if otp_code:
        await callback.message.edit_text(
            f"Kode OTP Anda (Amankan!):\n\n"
            f"`{otp_code}`\n\n"
            "Segera masukkan kode di atas sebelum kedaluwarsa."
        )
    else:
        await callback.answer("Kode OTP tidak ditemukan dalam pesan terbaru.", show_alert=True)        
    
    


