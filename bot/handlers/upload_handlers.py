# TODO recursion call if there's an error
import logging
from uuid import uuid4

from telegram import Update, InlineQueryResultCachedVideo
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from handlers.common_handlers import cancel
from data.messages import *
import utils.utils as utils
import utils.orm as orm

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


UPLD_GET_VID, UPLD_TITLE, UPLD_DESC, UPLD_KEYWORDS = range(4)

async def upload_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # if  not utils.initialized():
    #     await context.bot.send_message(chat_id=update.effective_chat.id, text=INIT_REQUIRED)
    #     return ConversationHandler.END
    if utils.is_admin(update.effective_user.username):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=UPLOAD_VIDEO)
        return UPLD_GET_VID
    else :
        await context.bot.send_message(chat_id=update.effective_chat.id, text=UPLOAD_DISABLED)
        return ConversationHandler.END
    

async def upload_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.update({
        'upld': {
            'id': str(uuid4()),
            'file_id': update['message']['video']['file_id'],
            'file_unique_id': update['message']['video']['file_unique_id'],
            'width': update['message']['video']['width'],
            'height': update['message']['video']['height'],
            'duration': update['message']['video']['duration'],
            'user_id': update.effective_user.id,
            'user_name': update.effective_user.username,
            'first_name': update.effective_user.first_name,
        }
    })

    if context.user_data['upld']['duration'] > MAX_VIDEO_LENGTH:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=MAX_VIDEO_LENGTH_ERROR)
        return ConversationHandler.END
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=UPLOAD_TITLE)
        return UPLD_TITLE


async def upload_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(update['message']['text']) <= MAX_TITLE_LENGTH:
        context.user_data['upld'].update({'title': update['message']['text']})
        await context.bot.send_message(chat_id=update.effective_chat.id, text=UPLOAD_DESCRP)
        return UPLD_DESC
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=MAX_TITLE_LENGTH_ERROR)
        return ConversationHandler.END


async def upload_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(update['message']['text']) <= MAX_DESCRP_LENGTH:
        context.user_data['upld'].update({'desc': update['message']['text']})
        await context.bot.send_message(chat_id=update.effective_chat.id, text=UPLOAD_KWORDS)
        return UPLD_KEYWORDS
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=MAX_DESCRP_LENGTH)
        return ConversationHandler.END


async def upload_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(update['message']['text']) <= MAX_KWORDS_LENGTH:
        context.user_data['upld'].update({'keywords': update['message']['text']})

        print("We are here")
        if context.user_data['upld']['user_name']:
            user = context.user_data['upld']['user_name']
        else:
            user = context.user_data['upld']['first_name']

        video_msg = await context.bot.send_video(chat_id=CHANNEL_ID, video=context.user_data['upld']['file_id'],
                caption=VIDEO_INFO_CAPTION.format(context.user_data['upld']['id'],
                        user,context.user_data['upld']['desc'],context.user_data['upld']['keywords']), parse_mode="HTML")
        
        try:
            user = orm.Users(
                user_id=update.effective_user.id,
                user_name=update.effective_user.username,
                first_name=update.effective_user.first_name,
                last_name=update.effective_user.last_name
            )
            orm.session.merge(user)
            video = orm.VideoData(
                video_id=context.user_data['upld']['id'],
                title=context.user_data['upld']['title'],
                description=context.user_data['upld']['desc'],
                keywords=context.user_data['upld']['keywords'],
                file_id=video_msg['video']['file_id'],
                file_unique_id=video_msg['video']['file_unique_id'],
                width=video_msg['video']['width'],
                height=video_msg['video']['height'],
                duration=video_msg['video']['duration'],
                user_id=context.user_data['upld']['user_id']
            )
            orm.session.add(video)
            channel_message = orm.ChannelMessages(
                msg_id=video_msg['message_id'],
                chat_id=video_msg['chat']['id'],
                video_id=context.user_data['upld']['id']
            )
            orm.session.add(channel_message)
            orm.session.commit()
            utils.videos_info.update_model()
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=VIDEO_UPLD_OK.format(context.user_data['upld']['id']),
                parse_mode="HTML")
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                text=ERROR_OCCURED)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=MAX_KWORDS_LENGTH_ERROR)


upload_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("upload", upload_start)],
    states={
        UPLD_GET_VID: [MessageHandler(filters.VIDEO, upload_video)],
        UPLD_TITLE: [MessageHandler((filters.TEXT & ~filters.COMMAND), upload_title)],
        UPLD_DESC: [MessageHandler((filters.TEXT & ~filters.COMMAND), upload_description)],
        UPLD_KEYWORDS: [MessageHandler((filters.TEXT & ~filters.COMMAND), upload_keywords)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True,
)
