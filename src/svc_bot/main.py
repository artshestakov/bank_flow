import asyncio
# ----------------------------------------------------------------------------------------------------------------------
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext
# ----------------------------------------------------------------------------------------------------------------------
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
async def card_list(update: Update, context: CallbackContext) -> None:
    await cmd_card.CardList(update, context)
# ----------------------------------------------------------------------------------------------------------------------
async def card_create(update: Update, context: CallbackContext) -> None:
    res = await cmd_card.CardCreate(update, context)
    if res is True:
        await card_list(update, context)
# ----------------------------------------------------------------------------------------------------------------------
async def card_click(update: Update, context: CallbackContext) -> None:
    await cmd_card.CardClick(update, context)
# ----------------------------------------------------------------------------------------------------------------------
async def card_delete(update: Update, context: CallbackContext) -> None:
    res = await cmd_card.CardDelete(update, context)
    if res is True:
        await card_list(update, context)
# ----------------------------------------------------------------------------------------------------------------------
def main() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    bot = Application.builder().token("8116206559:AAEpY3NXGE1KzJTr9VXN0DhY-f66Yz1JEWk").build()

    bot.add_handler(CommandHandler("start", start))

    bot.add_handler(CallbackQueryHandler(pattern="main_menu", callback=main_menu))
    bot.add_handler(CallbackQueryHandler(pattern="register_yes", callback=register_yes))
    bot.add_handler(CallbackQueryHandler(pattern="register_no", callback=register_no))
    bot.add_handler(CallbackQueryHandler(pattern="card_list", callback=card_list))
    bot.add_handler(CallbackQueryHandler(pattern="card_create", callback=card_create))
    bot.add_handler(CallbackQueryHandler(pattern="card_click", callback=card_click))
    bot.add_handler(CallbackQueryHandler(pattern="card_delete", callback=card_delete))

    loop.run_until_complete(bot.run_polling(allowed_updates=Update.ALL_TYPES))
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
# ----------------------------------------------------------------------------------------------------------------------
