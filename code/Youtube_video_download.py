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
LINK = range(1)
def start(update: Update, context: CallbackContext):
        update.message.reply_text(
                f"Hello {update.message.from_user.first_name}, Welcome to the Bot.Please write\n/help for list")
def help(update: Update, context: CallbackContext):
        update.message.reply_text(
                f"list,\n/ytd for youtube downloading ")
def ytd(update: Update, context: CallbackContext) -> int:
    print(f"{update.message.from_user.username} using youtube downloading download")

    update.message.reply_text(
        f'Hello {update.message.from_user.first_name} \nPast the link of the youtube video you want to download \n/cancel to cancel the work ',
    )

    return LINK

def link(update: Update, context: CallbackContext) -> int:
     link=update.message.text
     yt = YouTube(link)
     update.message.reply_text(f"Downloding {yt.title}")
     try:
        yt.streams.get_by_itag(22).download()
        update.message.reply_text(f"Downloded {yt.title}")
        update.message.reply_video(video=open(f'{yt.streams.get_by_itag(22).default_filename}', 'rb'))
     except:
         update.message.reply_text(f"Sorry but there are some error cheek after some time  ")
     return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        'Bye!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
  #Add api token of your bot
    updater = Updater(API Token)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('ytd', ytd)],
        states={
            LINK: [MessageHandler(Filters.text & ~Filters.command, link)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    print("bot activated")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
