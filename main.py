from os import getenv

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
TARGET_THREAD_CHANNEL_CHAT_ID = int(getenv('TARGET_THREAD_CHANNEL_CHAT_ID'))
SOURCE_GROUP_CHAT_ID = int(getenv('SOURCE_GROUP_CHAT_ID'))
TRIGGER_WORD = getenv('TRIGGER_WORD')


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.chat_id != SOURCE_GROUP_CHAT_ID:
        return

    if TRIGGER_WORD.lower() not in update.effective_message.text.lower():
        return

    channel_message = await update.effective_message.forward(TARGET_THREAD_CHANNEL_CHAT_ID)
    await update.effective_message.reply_text(
        text=f'Создано новое [обсуждение]({channel_message.link})',
        reply_to_message_id=update.effective_message.id,
        parse_mode=ParseMode.MARKDOWN_V2
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    application.run_polling()


if __name__ == '__main__':
    main()