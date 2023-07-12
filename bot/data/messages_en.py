from data.consts import *

# Common handlers
WELCOME_MESSAGE = "Hi. It's TEST"
UNKNOWN_COMMAND = "Don't invent, please..."
ERROR_OCCURED = "An error occured!!!"
CANCEL_MESSAGE = "Bye! I hope can talk again some day."


#Upload handlers 
UPLOAD_VIDEO = "Please upload video."
UPLOAD_DISABLED = "Video upload is disabled."
MAX_VIDEO_LENGTH_ERROR = f"This video exceeds the maximum length allowed \
    {MAX_VIDEO_LENGTH} seconds. Please, trim it down."

UPLOAD_TITLE = f"Send the title of this video {MAX_TITLE_LENGTH}ch"
MAX_TITLE_LENGTH_ERROR = f"This title exceeds the maximum length allowed \
    {MAX_TITLE_LENGTH} seconds. Please, trim it down."

UPLOAD_DESCRP = f"Send the description of this video {MAX_DESCRP_LENGTH}ch"
MAX_DESCRP_LENGTH_ERROR = f"This description exceeds the maximum length allowed \
    {MAX_DESCRP_LENGTH} seconds. Please, trim it down."

UPLOAD_KWORDS = f"Send the keywords of this video {MAX_KWORDS_LENGTH}ch"
MAX_KWORDS_LENGTH_ERROR = f"This keywords exceeds the maximum length allowed \
    {MAX_KWORDS_LENGTH} seconds. Please, trim it down."

VIDEO_UPLD_OK = "Video uploaded successfully! 🎉\n\n(<b>ID:</b> <code>{0}</code>)"
VIDEO_INFO_CAPTION = "<b>ID:</b> <code>{0}</code>\n<b>User:</b> <code>{1}</code>\n<b>Description:</b> <code>{2}</code>\n<b>Keywords:</b> <code>{3}</code>"


# Delete handlers
DELETE_START = "Send me again the video you want to delete (🎥) or its ID (🆔)."
DELETE_DISABLED = "delete_disabled"
NEED_VID_OR_ID = "NEED VIDEO OR ID"
ERROR_VID_NOT_FOUND = "Video with this id not found"
DELETE_CONFIRM = "DELETE? TITILE:{} DESC{}"
DELETED = "DELETED"

# 
INIT_REQUIRED = "Please add the bot to a channel to initialize it first."
# 

# Edit handlers

VIDEO_EDIT_CAPTION = "<b>ID:</b> <code>{0}</code>\n<b>Title:</b> <code>{1}</code>\n<b>Description:</b> <code>{2}</code>\n<b>Keywords:</b> <code>{3}</code>"

EDIT_START="edit_start"
EDIT_DISABLED="edit_disabled"
EDIT_CHOSE_OPTION="edit_choose_option"
EDIT_SEND_TITILE="edit_send_title"
EDIT_SEND_DESCCRP="edit_send_desc"
EDIT_SEND_KWORDS="edit_send_keywords"
EDIT_SEND_VIDEO="edit_send_video"
UNKNOWN_COMMAND = "unknown_command"

EDIT_TITILE_OK="edit_title_ok"
EDIT_NEED_TITILE="edit_need_title"

EDIT_DESC_OK="edit_desc_ok"
EDIT_NEED_DESC="edit_need_desc"

EDIT_KWORDS_OK="edit_keywords_ok"
EDIT_NEED_KWORDS="edit_need_keywords"

EDIT_VIDEO_OK="edit_vide_ok"
EDIT_NEED_VIDEO="edit_need_video"

CHANEL_INFO_CAPTION="channel_info_caption{}{}{}{}{USERNAME,LAST_NAME,DESCRP,KWORDS}"

# Search handlers

