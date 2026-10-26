import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

results = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Aviator statistik botiga xush kelibsiz!\n\n"
        "Natijalarni ko'paytiruvchisi bilan yuboring, masalan: 1.30x\n"
        "/analyze - statistik tahlil\n"
        "/history - natijalar tarixi"
    )

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not results:
        await update.message.reply_text("Avval natijalarni yuboring. Masalan: 1.30x")
        return

    avg = sum(results) / len(results)
    low = sum(x < 2 for x in results)
    mid = sum(2 <= x < 10 for x in results)
    high = sum(x >= 10 for x in results)

    await update.message.reply_text(
        f"Natijalar soni: {len(results)}\n"
        f"O'rtacha ko'paytiruvchi: {avg:.2f}x\n"
        f"2x dan past: {low}\n"
        f"2x–10x: {mid}\n"
        f"10x va yuqori: {high}\n\n"
        "Eslatma: bu o'tgan natijalar statistikasi, keyingi raund bashorati emas."
    )

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not results:
        await update.message.reply_text("Hozircha natijalar yo'q.")
        return
    await update.message.reply_text(
        "Oxirgi natijalar:\n" + ", ".join(f"{x:.2f}x" for x in results[-20:])
    )

async def add_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().replace("x", "").strip()
    try:
        value = float(text)
        if value < 1:
            raise ValueError
        results.append(value)
        await update.message.reply_text(f"Natija saqlandi: {value:.2f}x")
    except ValueError:
        await update.message.reply_text("Raqam yuboring, masalan: 1.30x")

def main():
    token = os.environ["BOT_TOKEN"]
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analyze", analyze))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_result))
    app.run_polling()

if __name__ == "__main__":
    main()
