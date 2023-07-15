from data.consts import *

# Common handlers
WELCOME_MESSAGE = "Welcome to MemGram! How can I make you laugh today? 😄🎉"
UNKNOWN_COMMAND = "Oops! I didn't understand that command. Let's try something funny instead! 🤷‍♂️😅"
ERROR_OCCURED = "Uh-oh! An error occurred. Don't worry, I'll fix it while you enjoy some memes(/random). 😬🔧"
CANCEL_MESSAGE = "Goodbye! Remember, laughter is the best medicine! Take care and keep smiling! 🙌😄"
ACCESS_ERROR = "Only admins can add new admin."
USERNAME_NOT_FOUND = "Oops! We cant find such user."
ADMIN_ADDED = "New admin successfully added."

# Upload handlers
UPLOAD_VIDEO = "Please share a hilarious video with me. I promise to keep it safe and bring more laughter to the world! 🎥🤣"
UPLOAD_DISABLED = "Oops! Video upload is temporarily disabled. It seems like the memes are on strike. 😔🚫"
MAX_VIDEO_LENGTH_ERROR = f"Uh-oh! This video exceeds the maximum allowed duration of {MAX_VIDEO_LENGTH} seconds. Don't worry, we can still find a shorter one! 😅⏰"

UPLOAD_TITLE = f"Awesome! Now, give me a catchy title for this masterpiece (up to {MAX_TITLE_LENGTH} characters). Let's make it memorable! 📝🌟"
MAX_TITLE_LENGTH_ERROR = f"Oops! The title exceeds the maximum allowed length of {MAX_TITLE_LENGTH} characters. Remember, brevity is the soul of wit! ✂️🎭"

UPLOAD_DESCRP = f"Great! Now, describe the video in your own words (up to {MAX_DESCRP_LENGTH} characters). Let's set the stage for laughter! 📝🎬"
MAX_DESCRP_LENGTH_ERROR = f"Oh no! The description exceeds the maximum allowed length of {MAX_DESCRP_LENGTH} characters. Remember, it's a punchline, not a novel! 📏😄"

UPLOAD_KWORDS = f"Almost there! Provide a few keywords that capture the essence of this video (up to {MAX_KWORDS_LENGTH} characters). Let's make it searchable! 📝🔍"
MAX_KWORDS_LENGTH_ERROR = f"Oops! The keywords exceed the maximum allowed length of {MAX_KWORDS_LENGTH} characters. Keep them short and snappy! 📏🔎"

VIDEO_UPLD_OK = "Video uploaded successfully! 🎉\n\n<b>ID:</b> <code>{0}</code> 🆔"
VIDEO_INFO_CAPTION = "<b>ID:</b> <code>{0}</code>\n<b>User:</b> <code>{1}</code>\n<b>Description:</b> <code>{2}</code>\n<b>Keywords:</b> <code>{3}</code>"

# Delete handlers
DELETE_START = "Please send me the video you want to delete (🎥) or its ID (🆔). Let's bid farewell to some laughs! 😢🗑️"
DELETE_DISABLED = "Sorry, but deleting videos is temporarily disabled. The jokes are just too good to let go! 😄🚫"
NEED_VID_OR_ID = "Oops! Looks like you forgot to provide a video or its ID. Let's try again with some comic timing! 😅"
ERROR_VID_NOT_FOUND = "Uh-oh! Video with this ID was not found. It must have joined a secret comedy club! 🤷‍♂️😄"
DELETE_CONFIRM = "Are you sure you want to delete this video?\n\n<b>Title:</b> {0}\n<b>Description:</b> {1} ⁉️"
DELETED = "Video deleted successfully! Now it's time to spread more laughter! 🗑️🤣"


INIT_REQUIRED = "Please add the bot to a channel to initialize it first. Let's get the laughter rolling! 📢😄"

# Edit handlers
VIDEO_EDIT_CAPTION = "<b>ID:</b> <code>{0}</code>\n<b>Title:</b> <code>{1}</code>\n<b>Description:</b> <code>{2}</code>\n<b>Keywords:</b> <code>{3}</code>"

EDIT_START = "Sent ID or VIDEO of mem you'd like to edit."
EDIT_DISABLED = "Editing videos is currently disabled. These memes have a mind of their own! 😄🚫"
EDIT_CHOSE_OPTION = "edit_choose_option"
EDIT_SEND_TITLE = "Please send the new title for the video. Let's give it a funny twist! 📝🎭"
EDIT_SEND_DESCCRP = "Please send the new description for the video. Let's add some humor to the script! 📝😄"
EDIT_SEND_KWORDS = "Please send the new keywords for the video. Let's make it more searchable and shareable! 📝🔍"
EDIT_SEND_VIDEO = "Please send the new video. Let's bring in some fresh comedy material! 🎥😄"

EDIT_TITILE_OK = "Title updated successfully! Now it's even funnier! ✅😄"
EDIT_NEED_TITILE = "Please provide a new title for the video. Let's keep the laughter rolling! 📝😄"

EDIT_DESC_OK = "Description updated successfully! The laughs just got an upgrade! ✅😄"
EDIT_NEED_DESC = "Please provide a new description for the video. Let's add some more humor! 📝🤣"

EDIT_KWORDS_OK = "Keywords updated successfully! Now it's easier to discover the fun! ✅🔍😄"
EDIT_NEED_KWORDS = "Please provide new keywords for the video. Let's make it viral! 📝🔥😄"

EDIT_VIDEO_OK = "Video updated successfully! Get ready for some fresh laughs! ✅🤣🎥"
EDIT_NEED_VIDEO = "Please provide a new video. Let's make everyone ROFL! 🎥🤣"

# Search handlers