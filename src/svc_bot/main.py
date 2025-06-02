import asyncio

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext

from src.svc_bot import cmd_start
from src.svc_bot import cmd_register
from src.svc_bot import cmd_card
# ----------------------------------------------------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await cmd_start.Start(update.message.from_user, context)
# ----------------------------------------------------------------------------------------------------------------------
async def main_menu(update: Update, context: CallbackContext) -> None:
    await cmd_start.Start(update.callback_query.from_user, context, update.callback_query.message.message_id)
# ----------------------------------------------------------------------------------------------------------------------
async def register_yes(update: Update, context: CallbackContext) -> None:
    await cmd_register.Register(context, update)
# ----------------------------------------------------------------------------------------------------------------------
async def register_no(update: Update, context: CallbackContext) -> None:
    await cmd_register.RegisterCancel(context,
                                      chat_id=update.callback_query.from_user.id,
                                      message_id=update.callback_query.message.message_id)
# ----------------------------------------------------------------------------------------------------------------------
def main() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    bot = Application.builder().token("8116206559:AAEpY3NXGE1KzJTr9VXN0DhY-f66Yz1JEWk").build()

    bot.add_handler(CommandHandler("start", start))

    bot.add_handler(CallbackQueryHandler(pattern='main_menu', callback=main_menu))
    bot.add_handler(CallbackQueryHandler(pattern='register_yes', callback=register_yes))
    bot.add_handler(CallbackQueryHandler(pattern='register_no', callback=register_no))

    loop.run_until_complete(bot.run_polling(allowed_updates=Update.ALL_TYPES))
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
# ----------------------------------------------------------------------------------------------------------------------
