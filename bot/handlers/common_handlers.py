import logging
from random import choice
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

import utils.orm as orm
from utils import utils
from utils.common import DB_PATH
from data.messages_en import *


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(text=WELCOME_MESSAGE)
    # await context.bot.send_message(chat_id=CHANNEL_ID, text=WELCOME_MESSAGE)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    # logger.warning('Update "%s" caused error "%s"', update, context.error)
    await print('Update "%s" caused error "%s"', update, context.error)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name) 
    await update.message.reply_text(CANCEL_MESSAGE, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=UNKNOWN_COMMAND)


async def get_random_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        random_result = choice(utils.videos_info.videos_info_list)

        user = orm.Users(
            user_id=update.effective_user.id,
            user_name=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name
        )

        sent_video = orm.SentVideos(
            user_id=update.effective_user.id,
            query='/random',
            video_id=random_result.id
        )    
        orm.session.merge(user)
        orm.session.add(sent_video)
        orm.session.commit()
        await context.bot.send_video(chat_id=update.effective_chat.id, video=random_result.file_id)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=ERROR_OCCURED)


async def get_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if utils.is_admin(update.effective_user.username):
        with open(DB_PATH, 'rb') as db_file:
            await context.bot.sendDocument(chat_id=update.effective_chat.id, document=db_file)
