import logging
from random import choice

import utils.orm as orm
from utils.common import DB_PATH
from telegram import Update, ReplyKeyboardRemove
from utils import utils
# from videogram.utils.common import settings, LOGS_PATH
from data.messages import *
from utils.utils import videos_info

from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(text=WELCOME_MESSAGE)

    await context.bot.send_message(chat_id=CHANNEL_ID, text=WELCOME_MESSAGE)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    # logger.warning('Update "%s" caused error "%s"', update, context.error)
    await print('Update "%s" caused error "%s"', update, context.error)

async def gt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    # logger.warning('Update "%s" caused error "%s"', update, context.error)
    print(videos_info.videos_info_list)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name) 
    await update.message.reply_text(
        CANCEL_MESSAGE , reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=UNKNOWN_COMMAND)


async def get_random_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if not (update.effective_user.username in settings['admin_usernames'] or not settings['closed_circle'] or
    #         update.effective_user.username in settings['closed_circle']):
    #     return
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


async def get_db(update, context):
    if utils.is_admin(update.effective_user.username):
        with open(DB_PATH, 'rb') as db_file:
            await context.bot.sendDocument(chat_id=update.effective_chat.id, document=db_file)
