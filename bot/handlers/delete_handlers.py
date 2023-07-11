import html

import utils.orm as orm
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, filters, CallbackQueryHandler
from handlers.common_handlers import cancel
from utils.utils import is_admin
from utils.common import *

DELETE_GET_ID, DELETE_CHOSEN_OPTION = range(2)


async def delete_start(update, context):
    # if not utils.initialized():
        # await context.bot.send_message(chat_id=update.effective_chat.id, text="init_required")
        # return ConversationHandler.END
    # else:
    if is_admin(update.effective_user.username):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="delete_start")
        return DELETE_GET_ID
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="delete_disabled")
        return ConversationHandler.END


async def delete_get_id(update, context):
    if update['message']['video']:
        result = orm.session.query(orm.VideoData, orm.ChannelMessages).join(orm.ChannelMessages, isouter=True).filter(
            orm.VideoData.file_unique_id == update['message']['video']['file_unique_id']).first()
    elif update['message']['text']:
        result = orm.session.query(orm.VideoData, orm.ChannelMessages).join(orm.ChannelMessages, isouter=True).filter(
            orm.VideoData.id == update['message']['text']).first()
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="need_video_or_id")
        return

    if result:
        context.user_data.update({
            'video': result[0],
            'channel_message': result[1]
        })

        menu_opt = [[InlineKeyboardButton('✅', callback_data='yes'),
                     InlineKeyboardButton('❌', callback_data='no')]]
        await context.bot.send_video(chat_id=update.effective_chat.id, video=context.user_data['video'].file_id,
                                     caption="delete_confirm".format(html.escape(context.user_data['video'].title),
                                                                        html.escape(
                                                                            context.user_data['video'].description)),
                                     parse_mode="HTML", reply_markup=InlineKeyboardMarkup(menu_opt))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="error_video_not_found")

    return DELETE_CHOSEN_OPTION


async def on_chosen_delete_option(update, context):
    await update.callback_query.answer()

    if update.callback_query.data == 'yes':
        try:
            orm.session.delete(context.user_data['video'])
            orm.session.delete(context.user_data['channel_message'])

            if context.user_data['channel_message'].msg_id:
                await context.bot.delete_message(chat_id=context.user_data['channel_message'].chat_id,
                                                 message_id=context.user_data['channel_message'].msg_id)

            orm.session.commit()
            await update.callback_query.edit_message_caption("delete_ok")
        except Exception as e:
            print(e)
            await update.callback_query.edit_message_caption("error")

    elif update.callback_query.data == 'no':
        await update.callback_query.edit_message_caption("cancel_command")
    else:
        await update.callback_query.edit_message_caption("unknown_command")

    return ConversationHandler.END


# Conversation handler
delete_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('delete', delete_start)],
    states={
        DELETE_GET_ID: [MessageHandler((filters.TEXT | filters.VIDEO) & (~filters.COMMAND), delete_get_id)],
        DELETE_CHOSEN_OPTION: [CallbackQueryHandler(on_chosen_delete_option, pattern='^(yes|no)$')],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True,
    per_message=True,
)
