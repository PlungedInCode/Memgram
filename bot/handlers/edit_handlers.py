import html

import utils.orm as orm
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaVideo, Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from handlers.common_handlers import cancel
from utils.utils import is_admin
from utils import utils
from data.messages_en import *

EDIT_GET_ID, EDIT_MENU, EDIT_CHOSEN_OPTION, EDIT_TITLE, EDIT_DESC, EDIT_KEYWORDS, EDIT_VIDEO = range(7)

async def edit_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if is_admin(update.effective_chat.username):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=EDIT_START)
        return EDIT_GET_ID
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=EDIT_DISABLED)
        return ConversationHandler.END

async def edit_get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update['message']['video']:
        result = orm.session.query(orm.VideoData, orm.ChannelMessages, orm.Users).join(
            orm.ChannelMessages, isouter=True).join(orm.Users, isouter=True).filter(
            orm.VideoData.file_unique_id == update['message']['video']['file_unique_id']).first()
    elif update['message']['text']:
        result = orm.session.query(orm.VideoData, orm.ChannelMessages, orm.Users).join(
            orm.ChannelMessages, isouter=True).join(orm.Users, isouter=True).filter(
            orm.VideoData.id == update['message']['text']).first()
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=NEED_VID_OR_ID)
        return
    
    if result:
        context.user_data.update({
            'video': result[0],
            'channel_message': result[1],
            'user': result[2]
        })

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=ERROR_VID_NOT_FOUND)
        return ConversationHandler.END

    await context.bot.send_video(chat_id=update.effective_chat.id,
                                 video=context.user_data['video'].file_id,
                                 caption=VIDEO_EDIT_CAPTION.format(context.user_data['video'].id,
                                                                html.escape(context.user_data['video'].title),
                                                                html.escape(context.user_data['video'].description),
                                                                html.escape(context.user_data['video'].keywords)),
                                 parse_mode="HTML")
    
    menu_opt = [[InlineKeyboardButton("video", callback_data='video'),
                 InlineKeyboardButton("title", callback_data='title')],
                [InlineKeyboardButton("description", callback_data='desc'),
                 InlineKeyboardButton("keywords", callback_data='keywords')],
                [InlineKeyboardButton("cancel", callback_data='cancel')]]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=EDIT_CHOSE_OPTION,
                                   reply_markup=InlineKeyboardMarkup(menu_opt))
    return EDIT_CHOSEN_OPTION

async def on_chosen_edit_option(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()

    if update.callback_query.data == 'title':
        await update.callback_query.edit_message_text("title")
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=EDIT_SEND_TITILE)
        return EDIT_TITLE
    elif update.callback_query.data == 'desc':
        await update.callback_query.edit_message_text("description")
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=EDIT_SEND_DESCCRP)
        return EDIT_DESC
    elif update.callback_query.data == 'keywords':
        await update.callback_query.edit_message_text("keywords")
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=EDIT_SEND_KWORDS)
        return EDIT_KEYWORDS
    elif update.callback_query.data == 'video':
        await update.callback_query.edit_message_text("video")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=EDIT_SEND_VIDEO)
        return EDIT_VIDEO
    elif update.callback_query.data == 'cancel':
        await update.callback_query.edit_message_text("cancel")
        return ConversationHandler.END
    else:
        await update.callback_query.edit_message_text(chat_id=update.effective_chat.id, text=UNKNOWN_COMMAND)
        return ConversationHandler.END



async def edit_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update['message']['text'] and len(update['message']['text']) <= MAX_TITLE_LENGTH:
        try:
            context.user_data['video'].title = update['message']['text']
            orm.session.add(context.user_data['video'])
            orm.session.commit()

            utils.videos_info.update_model()
            await context.bot.send_message(chat_id=update.effective_chat.id, text=EDIT_TITILE_OK)
        except Exception:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=ERROR_OCCURED)

        return ConversationHandler.END
    else:
        if not update['message']['text']:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=EDIT_NEED_TITILE)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=MAX_TITLE_LENGTH_ERROR)
        return EDIT_TITLE



async def edit_desc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update['message']['text'] and len(update['message']['text']) <= MAX_KWORDS_LENGTH:
        try:
            context.user_data['video'].description = update['message']['text']
            orm.session.add(context.user_data['video'])
            orm.session.commit()
            utils.videos_info.update_model()

            if context.user_data['channel_message'].msg_id:
                await context.bot.edit_message_caption(
                    chat_id=context.user_data['channel_message'].chat_id,
                    message_id=context.user_data['channel_message'].msg_id,
                    caption=VIDEO_INFO_CAPTION.format(context.user_data['video'].id,
                                                             html.escape(context.user_data['user'].user_name or
                                                                         context.user_data['user'].last_name),
                                                             html.escape(context.user_data['video'].description),
                                                             html.escape(context.user_data['video'].keywords)),
                    parse_mode="HTML")

            await context.bot.send_message(chat_id=update.effective_chat.id, text=EDIT_DESC_OK)
        except Exception as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=ERROR_OCCURED)
        return ConversationHandler.END

    else:
        if not update['message']['text']:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=EDIT_NEED_DESC)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=MAX_DESCRP_LENGTH_ERROR)
        return EDIT_DESC



async def edit_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update['message']['text'] and len(update['message']['text']) <= MAX_KWORDS_LENGTH:
        try:
            context.user_data['video'].keywords = update['message']['text']
            orm.session.add(context.user_data['video'])
            orm.session.commit()
            utils.videos_info.update_model()

            if context.user_data['channel_message'].msg_id:
                await context.bot.edit_message_caption(
                    chat_id=context.user_data['channel_message'].chat_id,
                    message_id=context.user_data['channel_message'].msg_id,
                    caption=VIDEO_INFO_CAPTION.format(context.user_data['video'].id,
                                                             html.escape(context.user_data['user'].user_name or
                                                                         context.user_data['user'].last_name),
                                                             html.escape(context.user_data['video'].description),
                                                             html.escape(context.user_data['video'].keywords)),
                    parse_mode="HTML")

            await context.bot.send_message(chat_id=update.effective_chat.id, text=EDIT_KWORDS_OK)
        except Exception:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=ERROR_OCCURED)
        return ConversationHandler.END

    else:
        if not update['message']['text']:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=EDIT_NEED_KWORDS)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=MAX_KWORDS_LENGTH_ERROR)
        return EDIT_KEYWORDS


async def edit_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update['message']['video']:
        if update['message']['video']['duration'] > MAX_VIDEO_LENGTH:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=MAX_VIDEO_LENGTH_ERROR)
            return EDIT_VIDEO
        else:
            try:
                context.user_data['video'].file_id = update['message']['video']['file_id']
                context.user_data['video'].file_unique_id = update['message']['video']['file_unique_id']
                context.user_data['video'].width = update['message']['video']['width']
                context.user_data['video'].height = update['message']['video']['height']
                context.user_data['video'].duration = update['message']['video']['duration']

                orm.session.add(context.user_data['video'])
                orm.session.commit()
                utils.videos_info.update_model()

                ch_id = context.user_data['channel_message'].chat_id
                msg_id = context.user_data['channel_message'].msg_id
                video_id = update['message']['video']['file_id']
                if context.user_data['channel_message'].msg_id:
                    await context.bot.edit_message_media(
                        chat_id=ch_id,
                        message_id=msg_id,
                        media=InputMediaVideo(
                            video_id,
                            caption=VIDEO_INFO_CAPTION.format(context.user_data['video'].id,
                                                                     html.escape(context.user_data['user'].user_name or
                                                                                 context.user_data['user'].last_name),
                                                                     html.escape(
                                                                         context.user_data['video'].description),
                                                                     html.escape(context.user_data['video'].keywords)),
                            parse_mode="HTML"))

                await context.bot.send_message(chat_id=update.effective_chat.id, text=EDIT_VIDEO_OK)
            except Exception as e:
                for i in context.user_data:
                    print(i)
                print(f"ERROR - {e}")
                await context.bot.send_message(chat_id=update.effective_chat.id, text=ERROR_OCCURED)

            return ConversationHandler.END
    else:
        if not update['message']['video']:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=EDIT_NEED_VIDEO)
        return EDIT_VIDEO




# Conversation handler
edit_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('edit', edit_start)],
    states={
        EDIT_GET_ID: [MessageHandler((filters.TEXT | filters.VIDEO) & (~filters.COMMAND), edit_get_id)],
        EDIT_CHOSEN_OPTION: [
            CallbackQueryHandler(on_chosen_edit_option, pattern='^(video|title|desc|keywords|cancel)$')],
        EDIT_TITLE: [MessageHandler((filters.TEXT & ~filters.COMMAND), edit_title)],
        EDIT_DESC: [MessageHandler((filters.TEXT & ~filters.COMMAND), edit_desc)],
        EDIT_KEYWORDS: [MessageHandler((filters.TEXT & ~filters.COMMAND), edit_keywords)],
        EDIT_VIDEO: [MessageHandler((filters.VIDEO & ~filters.COMMAND), edit_video)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True
)