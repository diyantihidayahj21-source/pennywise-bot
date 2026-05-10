from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

# =====================================================
# MASUKKAN TOKEN BOT TELEGRAM DI SINI
# =====================================================
import os

TOKEN = os.getenv("8769119495:AAEYTAwvz9hsHcuViuTTkC_ijc6mT6iAUDA")

# =====================================================
# MENU MODERN
# =====================================================
def menu_utama():

    keyboard = [
        [
            InlineKeyboardButton(
                "🚨 Darurat",
                callback_data="darurat"
            ),

            InlineKeyboardButton(
                "🎯 Tabung",
                callback_data="tabung"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)

# =====================================================
# START
# =====================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    teks = """
💰 PennyWise
Receh Hari Ini, Sultan Nanti

Halo mahasiswa pejuang tanggal tua 😎

Pilih fitur di bawah buat mulai ngatur uangmu 👇
"""

    await update.message.reply_text(
        teks,
        reply_markup=menu_utama()
    )

# =====================================================
# SAAT TOMBOL DIKLIK
# =====================================================
async def tombol(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    # =================================================
    # 🚨 DARURAT
    # =================================================
    if data == "darurat":

        context.user_data["fitur"] = "darurat_barang"

        await query.message.reply_text(
            "🚨 Mau beli apa nih?\n\n"
            "Contoh:\n"
            "- sepatu\n"
            "- kopi\n"
            "- skincare"
        )

    # =================================================
    # 🎯 TABUNG
    # =================================================
    elif data == "tabung":

        context.user_data["fitur"] = "tabung_target"

        await query.message.reply_text(
            "🎯 Mau nabung buat apa?\n\n"
            "Contoh:\n"
            "- laptop\n"
            "- HP baru\n"
            "- liburan"
        )

# =====================================================
# CHAT INTERAKTIF
# =====================================================
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pesan = update.message.text.lower()

    fitur = context.user_data.get("fitur")

    # =================================================
    # 🚨 DARURAT ATAU GAYA HIDUP
    # =================================================

    # -----------------------------
    # TAHAP 1 -> INPUT BARANG
    # -----------------------------
    if fitur == "darurat_barang":

        context.user_data["barang"] = pesan

        context.user_data["fitur"] = "darurat_harga"

        await update.message.reply_text(
            f"💸 Harga {pesan} berapa?\n\n"
            "Contoh:\n"
            "250000"
        )

        return

    # -----------------------------
    # TAHAP 2 -> INPUT HARGA
    # -----------------------------
    elif fitur == "darurat_harga":

        try:

            harga = int(pesan)

            barang = context.user_data["barang"]

            kebutuhan = [
                "buku",
                "obat",
                "charger",
                "print",
                "ukt",
                "laptop"
            ]

            # KLASIFIKASI
            if barang in kebutuhan:

                hasil = (
                    f"🚨 {barang.capitalize()} termasuk kebutuhan penting.\n"
                    "Masih masuk kategori darurat 😎"
                )

            elif harga >= 500000:

                hasil = (
                    f"👀 Harga {barang} lumayan mahal.\n"
                    "Yakin butuh, bukan cuma lapar mata? 😆"
                )

            else:

                hasil = (
                    f"😎 {barang.capitalize()} masih aman kok kalau budget cukup."
                )

            await update.message.reply_text(
                hasil,
                reply_markup=menu_utama()
            )

            context.user_data.clear()

        except:

            await update.message.reply_text(
                "⚠️ Masukkan angka ya.\n"
                "Contoh: 300000"
            )

        return

    # =================================================
    # 🎯 TABUNG MIMPI
    # =================================================

    # -----------------------------
    # TAHAP 1 -> TARGET
    # -----------------------------
    elif fitur == "tabung_target":

        context.user_data["target"] = pesan

        context.user_data["fitur"] = "tabung_harga"

        await update.message.reply_text(
            f"💰 Harga target {pesan} berapa?\n\n"
            "Contoh:\n"
            "7000000"
        )

        return

    # -----------------------------
    # TAHAP 2 -> HARGA TARGET
    # -----------------------------
    elif fitur == "tabung_harga":

        try:

            harga = int(pesan)

            context.user_data["harga"] = harga

            context.user_data["fitur"] = "tabung_bulan"

            await update.message.reply_text(
                "📅 Mau tercapai dalam berapa bulan?\n\n"
                "Contoh:\n"
                "10"
            )

        except:

            await update.message.reply_text(
                "⚠️ Masukkan angka ya.\n"
                "Contoh: 5000000"
            )

        return

    # -----------------------------
    # TAHAP 3 -> BULAN
    # -----------------------------
    elif fitur == "tabung_bulan":

        try:

            bulan = int(pesan)

            harga = context.user_data["harga"]

            target = context.user_data["target"]

            tabungan = harga // bulan

            hasil = (
                f"🎯 Target: {target.capitalize()}\n\n"
                f"💰 Kamu perlu nabung sekitar:\n"
                f"Rp{tabungan:,}/bulan 🔥\n\n"
                "Receh hari ini, sultan nanti 😎"
            )

            await update.message.reply_text(
                hasil,
                reply_markup=menu_utama()
            )

            context.user_data.clear()

        except:

            await update.message.reply_text(
                "⚠️ Masukkan jumlah bulan ya.\n"
                "Contoh: 12"
            )

        return

    # =================================================
    # DEFAULT
    # =================================================
    await update.message.reply_text(
        "🤔 Pilih fitur dulu dari tombol di atas ya 😎",
        reply_markup=menu_utama()
    )

# =====================================================
# MAIN
# =====================================================
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(tombol))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            reply
        )
    )

    print("🤖 PennyWise aktif...")

    app.run_polling()

# =====================================================
# JALANKAN BOT
# =====================================================
if __name__ == "__main__":
    main()