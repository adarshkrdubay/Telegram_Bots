import os
from pytube import YouTube
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Video
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
LINK, AUDIO, VIDEOLOW, VIDEOHIGH, VIDEOMED, QUALITY = range(6)

def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Video', 'Audio', 'Cancel']]
    update.message.reply_text(
        f'Hay {update.message.from_user.first_name} !!\n'
        'Welcome to youtube download.\n'
        'Send /cancel to cancel any time .\n\n',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Video or Audio ?'
        ),
    )
    return LINK


def link(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Moderate', 'Low', 'Cancel']]
    if update.message.text=="Video":
         update.message.reply_text("Select the Quality", reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Quality?'
        ),)
         return QUALITY
    elif update.message.text=="Audio":
           update.message.reply_text("paste the link", reply_markup=ReplyKeyboardRemove())
           return AUDIO
    elif update.message.text=="Cancel":
         update.message.reply_text("Bye!!!", reply_markup=ReplyKeyboardRemove())
         return ConversationHandler.END
    else :
         update.message.reply_text("Wrong command", reply_markup=ReplyKeyboardRemove())
         return ConversationHandler.END
def quality(update: Update, context: CallbackContext) -> int:
    if update.message.text=="High":
           update.message.reply_text("paste the link", reply_markup=ReplyKeyboardRemove())
           return VIDEOHIGH
    elif update.message.text=="Moderate":
           update.message.reply_text("paste the link", reply_markup=ReplyKeyboardRemove())
           return VIDEOMED
    elif update.message.text=="Low":
           update.message.reply_text("paste the link", reply_markup=ReplyKeyboardRemove())
           return VIDEOLOW
    elif update.message.text=="Cancel":
         update.message.reply_text("Bye!!!", reply_markup=ReplyKeyboardRemove())
         return ConversationHandler.END
    else :
         update.message.reply_text("Wrong command", reply_markup=ReplyKeyboardRemove())
         return ConversationHandler.END
def videomed(update: Update, context: CallbackContext) -> int:
    link = update.message.text
    yt = YouTube(link)
    try:
        update.message.reply_text(f"Downloding {yt.title}")
        yt.streams.get_by_itag(22).download()
        update.message.reply_text(f"Downloded {yt.title}")
        update.message.reply_video(
            video=open(f'{yt.streams.get_by_itag(22).default_filename}', 'rb'))
        os.remove(f"{yt.streams.get_by_itag(22).default_filename}")
        update.message.reply_text(f"Thanks for using ☺☺")
    except:
        update.message.reply_text(
            f"Sorry but either the link is incorrect or there are some error.\n cheek after some time  😞😞")
    return ConversationHandler.END
def videolow(update: Update, context: CallbackContext) -> int:
    link = update.message.text
    yt = YouTube(link)
    try:
        update.message.reply_text(f"Downloding {yt.title}")
        yt.streams.get_by_itag(18).download()
        update.message.reply_text(f"Downloded {yt.title}")
        update.message.reply_video(
            video=open(f'{yt.streams.get_by_itag(18).default_filename}', 'rb'))
        os.remove(f"{yt.streams.get_by_itag(18).default_filename}")
        update.message.reply_text(f"Thanks for using ☺☺")
    except:
        update.message.reply_text(
            f"Sorry but either the link is incorrect or there are some error.\n cheek after some time  😞😞")
    return ConversationHandler.END
def audio(update: Update, context: CallbackContext) -> int:
    link = update.message.text
    yt = YouTube(link)
    try:
        update.message.reply_text(f"Downloding {yt.title}")
        yt.streams.get_by_itag(251).download()
        update.message.reply_text(f"Downloded {yt.title}")
        update.message.reply_audio(
            audio=open(f'{yt.streams.get_by_itag(251).default_filename}', 'rb'))
        os.remove(f"{yt.streams.get_by_itag(251).default_filename}")
        update.message.reply_text(f"Thanks for using ☺☺")
    except:
        update.message.reply_text(
            f"Sorry but either the link is incorrect or there are some error.\n cheek after some time  😞😞")
    return ConversationHandler.END
def cancel(update: Update, context: CallbackContext) -> int:

    update.message.reply_text('Bye!', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main() -> None:
    updater = Updater("your bot api")
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states={
            LINK: [MessageHandler(Filters.text & ~Filters.command, link)],
            AUDIO: [MessageHandler(Filters.text & ~Filters.command, audio)],
            QUALITY: [MessageHandler(Filters.text & ~Filters.command, quality)],
            VIDEOMED: [MessageHandler(Filters.text & ~Filters.command, videomed)],
            VIDEOLOW: [MessageHandler(Filters.text & ~Filters.command, videolow)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    print("bot activated")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
