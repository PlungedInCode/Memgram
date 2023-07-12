import html
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ConversationHandler, MessageHandler,
    CommandHandler, filters, 
    CallbackQueryHandler, ContextTypes
)
from handlers.common_handlers import cancel
from utils.utils import is_admin
import utils.orm as orm
from utils.common import *
from data.messages_en import *

DELETE_GET_ID, DELETE_CHOSEN_OPTION = range(2)


async def delete_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if is_admin(update.effective_user.username):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=DELETE_START)
        return DELETE_GET_ID
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=DELETE_DISABLED)
        return ConversationHandler.END


async def delete_get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update['message']['video']:
        result = orm.session.query(orm.VideoData, orm.ChannelMessages).join(orm.ChannelMessages, isouter=True).filter(
            orm.VideoData.file_unique_id == update['message']['video']['file_unique_id']).first()
    elif update['message']['text']:
        result = orm.session.query(orm.VideoData, orm.ChannelMessages).join(orm.ChannelMessages, isouter=True).filter(
            orm.VideoData.id == update['message']['text']).first()
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=NEED_VID_OR_ID)
        return

    if result:
        context.user_data.update({
            'video': result[0],
            'channel_message': result[1]
        })

        menu_opt = [[InlineKeyboardButton('✅', callback_data='yes'),
                     InlineKeyboardButton('❌', callback_data='no')]]
        await context.bot.send_video(chat_id=update.effective_chat.id, video=context.user_data['video'].file_id,
                                     caption=DELETE_CONFIRM.format(html.escape(context.user_data['video'].title),
                                                                        html.escape(
                                                                            context.user_data['video'].description)),
                                     parse_mode="HTML", reply_markup=InlineKeyboardMarkup(menu_opt))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=ERROR_VID_NOT_FOUND)

    return DELETE_CHOSEN_OPTION


async def on_chosen_delete_option(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()

    if update.callback_query.data == 'yes':
        try:
            orm.session.delete(context.user_data['video'])
            orm.session.delete(context.user_data['channel_message'])

            if context.user_data['channel_message'].msg_id:
                await context.bot.delete_message(chat_id=context.user_data['channel_message'].chat_id,
                                                 message_id=context.user_data['channel_message'].msg_id)

            orm.session.commit()
            await update.callback_query.edit_message_caption(DELETED)
        except Exception as e:
            print(e)
            await update.callback_query.edit_message_caption(ERROR_OCCURED)

    elif update.callback_query.data == 'no':
        await update.callback_query.edit_message_caption(CANCEL_MESSAGE)
    else:
        await update.callback_query.edit_message_caption(UNKNOWN_COMMAND)

    return ConversationHandler.END


# Delete conversation handler
delete_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('delete', delete_start)],
    states={
        DELETE_GET_ID: [MessageHandler((filters.TEXT | filters.VIDEO) & (~filters.COMMAND), delete_get_id)],
        DELETE_CHOSEN_OPTION: [CallbackQueryHandler(on_chosen_delete_option, pattern='^(yes|no)$')],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True,
)
