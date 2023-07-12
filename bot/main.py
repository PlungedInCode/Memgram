import os
import logging
from dotenv import load_dotenv

from telegram.ext import CommandHandler, InlineQueryHandler, ChosenInlineResultHandler, Application
from handlers import common_handlers, search_handlers
from handlers.delete_handlers import delete_conv_handler
from handlers.edit_handlers import edit_conv_handler
from handlers.upload_handlers import upload_conv_handler


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv("TOKEN")

def main() -> None:
    try:
        application = Application.builder().token(TOKEN).build()
        print('Bot is working')
    except Exception as e:
        print(f"Couldn't find the bot token. Please set the env variable - {e}")
        exit(1)
        
    # Common handlers
    application.add_handler(CommandHandler("start", common_handlers.start))
    application.add_handler(CommandHandler("random", common_handlers.get_random_video))
    application.add_handler(CommandHandler("get_db", common_handlers.get_db))

    # Conv handlers
    application.add_handler(upload_conv_handler)
    application.add_handler(edit_conv_handler)
    application.add_handler(delete_conv_handler)  

    # Search & send video
    application.add_handler(InlineQueryHandler(search_handlers.inline_search))
    application.add_handler(ChosenInlineResultHandler(search_handlers.on_chosen_video))

    # Log all errors
    application.add_error_handler(common_handlers.error)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == '__main__':
    # print(videos_info.videos_info_list)
    main()  


#TODO admins can add new admins