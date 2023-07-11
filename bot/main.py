import os
from dotenv import load_dotenv

from telegram.ext import CommandHandler, InlineQueryHandler, ChosenInlineResultHandler, ChatMemberHandler, Application
from handlers import common_handlers, search_handlers #, admin_handlers
from handlers.delete_handlers import delete_conv_handler
# from videogram.handlers.edit_handlers import edit_conv_handler
from handlers.upload_handlers import upload_conv_handler

load_dotenv()

TOKEN = os.getenv("TOKEN")


def main():
    try:
        application = Application.builder().token(TOKEN).build()
        print('Bot is working')
    except Exception as e:
        print(f"Couldn't find the bot token. Please set the env variable - {e}")
        exit(1)
        
    # Common handlers
    application.add_handler(CommandHandler("start", common_handlers.start))
    application.add_handler(CommandHandler("gt", common_handlers.gt))
    # application.add_handler(CommandHandler("random", common_handlers.get_random_video))

    # Conv handlers
    application.add_handler(upload_conv_handler)
    application.add_handler(delete_conv_handler)    


    # Search & send video
    application.add_handler(InlineQueryHandler(search_handlers.inline_search))
    application.add_handler(ChosenInlineResultHandler(search_handlers.on_chosen_video))

    # Log all errors
    # application.add_error_handler(upload_handlers.error)


    application.run_polling()


if __name__ == '__main__':
    main()