import os
import requests

from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    CommandHandler,
)

from helpers import add_handlers, get_logger
from results import get_results

logger = get_logger()


def start(update, context):
    f = open("users.txt", "a")
    user_info = update.message.chat
    print(f"New User: {user_info}")
    f.write(
        f"START PRESSED-----------------------------------\nChat data: {user_info} pressed start\n"
    )
    f.close()
    update.message.reply_text(
        "Lex.uz saytidagi hujjatlar bo'yicha qidiruvni amalga oshirish uchun "
        "hujjat nomidagi so'z yoki jumlani kiriting / "
        "Для поиска документов по сайту Lex.uz введите слово или фразу в наименовании акта:\n\n\n"
        "* Bot serveri o'zgartirishlar kiritish uchun o'chirilib-yoqilishi mumkin, ❗️Bot ishlamasa qayta ♻️/start♻️ bosib koring\n"
        "* Ayni damda sayt maksimum 25tagacha natija olishga imkon beradi\n"
        "Noqulayliklar uchun uzr so'raymiz!"
    )


def delete_result(update, context):
    query = update.callback_query
    context.bot.delete_message(
        chat_id=context.user_data["chat_id"], message_id=query.message.message_id
    )


def get_prev_results(update, context):
    page = context.user_data["current_page"] - 1
    context.user_data["current_page"] = page
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        context.user_data["msgs"][page], reply_markup=context.user_data["markups"][page]
    )


def get_next_results(update, context):
    page = context.user_data["current_page"] + 1
    context.user_data["current_page"] = page
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        context.user_data["msgs"][page], reply_markup=context.user_data["markups"][page]
    )


def send_file(update, context):
    file_link = context.user_data["file_links"][int(update.callback_query.data)]
    file_name = (
        context.user_data["file_names"][int(update.callback_query.data)][:60] + ".doc"
    )

    r = requests.get(file_link, allow_redirects=True)
    open(file_name, "wb").write(r.content)
    print("Downloaded file is being send")
    context.bot.sendDocument(
        chat_id=context.user_data["chat_id"],
        document=open(file_name, "rb"),
        filename=file_name,
        timeout=5,
    )
    os.remove(file_name)


def send_results(update, context):
    context.user_data["keyword"] = update.message.text
    context.user_data["chat_id"] = update.message.chat_id

    msgs, markups = get_results(update, context)

    context.user_data["msgs"] = msgs
    context.user_data["markups"] = markups
    context.user_data["current_page"] = 0

    update.message.reply_text(msgs[0], reply_markup=markups[0])


def main():
    TOKEN = "your token here"
    PORT = os.environ.get("PORT")
    NAME = "lawhunter"

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    handlers = [
        CommandHandler("start", start),
        MessageHandler(Filters.text, send_results),
        CallbackQueryHandler(send_file, pattern="^[0-9]+$"),
        CallbackQueryHandler(get_next_results, pattern="^next$"),
        CallbackQueryHandler(get_prev_results, pattern="^prev$"),
        CallbackQueryHandler(delete_result, pattern="^del$"),
    ]
    add_handlers(dp, handlers)

    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))

    # updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
