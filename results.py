import re
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from helpers import get_logger

logger = get_logger()

# noinspection PyTypeChecker
def create_markups(update, context):
    total = context.user_data['total']
    kb1 = []
    kb2 = []
    kb3 = []

    if total < 11:
        if total <= 5:
            kb1 = [[], [InlineKeyboardButton("❌", callback_data="del")]]
            for j in range(total):
                kb1[0].append(InlineKeyboardButton(f"{j + 1}", callback_data=f"{j}"))
        elif total > 5:
            kb1 = [[], [], [InlineKeyboardButton("❌", callback_data="del")]]
            for j in range(5):
                kb1[0].append(InlineKeyboardButton(f"{j + 1}", callback_data=f"{j}"))
            for j in range(5, total):
                kb1[1].append(InlineKeyboardButton(f"{j + 1}", callback_data=f"{j}"))

    if 10 < total < 21:
        kb1 = [
            [
                InlineKeyboardButton("1", callback_data="0"),
                InlineKeyboardButton("2", callback_data="1"),
                InlineKeyboardButton("3", callback_data="2"),
                InlineKeyboardButton("4", callback_data="3"),
                InlineKeyboardButton("5", callback_data="4")
            ],
            [
                InlineKeyboardButton("6", callback_data="5"),
                InlineKeyboardButton("7", callback_data="6"),
                InlineKeyboardButton("8", callback_data="7"),
                InlineKeyboardButton("9", callback_data="8"),
                InlineKeyboardButton("10", callback_data="9")
            ],
            [
                InlineKeyboardButton("❌", callback_data="del"),
                InlineKeyboardButton("➡", callback_data="next")
            ]
        ]

        if total <= 15:
            kb2 = [[], [
                InlineKeyboardButton("⬅", callback_data="prev"),
                InlineKeyboardButton("❌", callback_data="del"),
            ]]
            for j in range(10, total):
                kb2[0].append(InlineKeyboardButton(f"{j + 1}", callback_data=f"{j}"))
        elif total > 15:
            kb2 = [[], [], [
                InlineKeyboardButton("⬅", callback_data="prev"),
                InlineKeyboardButton("❌", callback_data="del"),
            ]]
            for j in range(10, 15):
                kb2[0].append(InlineKeyboardButton(f"{j + 1}", callback_data=f"{j}"))
            for j in range(15, total):
                kb2[1].append(InlineKeyboardButton(f"{j + 1}", callback_data=f"{j}"))

    if total > 20:
        kb1 = [
            [
                InlineKeyboardButton("1", callback_data="0"),
                InlineKeyboardButton("2", callback_data="1"),
                InlineKeyboardButton("3", callback_data="2"),
                InlineKeyboardButton("4", callback_data="3"),
                InlineKeyboardButton("5", callback_data="4")
            ],
            [
                InlineKeyboardButton("6", callback_data="5"),
                InlineKeyboardButton("7", callback_data="6"),
                InlineKeyboardButton("8", callback_data="7"),
                InlineKeyboardButton("9", callback_data="8"),
                InlineKeyboardButton("10", callback_data="9")
            ],
            [
                InlineKeyboardButton("❌", callback_data="del"),
                InlineKeyboardButton("➡", callback_data="next")
            ]
        ]
        kb2 = [
            [
                InlineKeyboardButton("11", callback_data="10"),
                InlineKeyboardButton("12", callback_data="11"),
                InlineKeyboardButton("13", callback_data="12"),
                InlineKeyboardButton("14", callback_data="13"),
                InlineKeyboardButton("15", callback_data="14")
            ],
            [
                InlineKeyboardButton("16", callback_data="15"),
                InlineKeyboardButton("17", callback_data="16"),
                InlineKeyboardButton("18", callback_data="17"),
                InlineKeyboardButton("19", callback_data="18"),
                InlineKeyboardButton("20", callback_data="19")
            ],
            [
                InlineKeyboardButton("⬅", callback_data="prev"),
                InlineKeyboardButton("❌", callback_data="del"),
                InlineKeyboardButton("➡", callback_data="next")
            ]
        ]
        kb3 = [[], [
                InlineKeyboardButton("⬅", callback_data="prev"),
                InlineKeyboardButton("❌", callback_data="del"),
            ]]
        for j in range(20, total):
            kb3[0].append(InlineKeyboardButton(f"{j + 1}", callback_data=f"{j}"))

    return [InlineKeyboardMarkup(kb1), InlineKeyboardMarkup(kb2), InlineKeyboardMarkup(kb3)]


def create_messages(update, context):
    total = context.user_data['total']
    print('Total number of results: ', total)
    msg1 = ""
    msg2 = ""
    msg3 = ""
    ending = "\n\nKerakli hujjatni topa olmagan bo'lsangiz:"\
    "\n1. Tekshirib ko'ring:\n"\
    "- yetarlicha kalit so'zlar mavjudligi, so'zlarning aniq to'g'riligi\n"\
    "- so'zlarda x-h harflar, ', (ъ, ь) kabi belgilar to'g'riligi\n"\
    "- hujjat nomi кириллчада (русчада) bo'lishi mumkin"\
    "\n2. Lex.uz sayti profilaktika holatida bo'lishi mumkin"\
    "\n3. {}".format(context.user_data['src_link'])

    if total <= 10:
        msg1 = f"Qidiruv natijlari \\ Результаты поиска: {1}-{total}, {total}\n\n"
        for idx1 in range(total):
            msg1 += "{}. {}\n\n".format(idx1 + 1, context.user_data['file_names'][idx1])

        msg1 += ending

    if 10 < total < 21:
        msg1 = f"Qidiruv natijlari: {1}-{10}, {total}\n\n"
        msg2 = f"Qidiruv natijlari: {11}-{total}, {total}\n\n"
        for idx2 in range(10):
            msg1 += "{}. {}\n\n".format(idx2 + 1, context.user_data['file_names'][idx2])
        for idx3 in range(10, total):
            msg2 += "{}. {}\n\n".format(idx3 + 1, context.user_data['file_names'][idx3])

        msg2 += ending

    if total > 20:
        msg1 = f"Qidiruv natijlari: {1}-{10}, {total}\n\n"
        msg2 = f"Qidiruv natijlari: {11}-{20}, {total}\n\n"
        msg3 = f"Qidiruv natijlari: {21}-{total}, {total}\n\n"
        for idx4 in range(10):
            msg1 += "{}. {}\n\n".format(idx4 + 1, context.user_data['file_names'][idx4])
        for idx5 in range(10, 20):
            msg2 += "{}. {}\n\n".format(idx5 + 1, context.user_data['file_names'][idx5])
        for idx6 in range(20, total):
            msg3 += "{}. {}\n\n".format(idx6 + 1, context.user_data['file_names'][idx6])

        msg3 += ending

    return [msg1, msg2, msg3]


def get_results(update, context):
    title = context.user_data.get("keyword", "")
    keyword = quote(title)
    print('Search phrase: ', keyword)

    link = "https://lex.uz/search/nat?searchtitle={}&exact2=1&status=Y".format(keyword)

    context.user_data['src_link'] = link

    print('Generated link for search phrase: ', link)
    html = requests.get(link).content.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    titles = []
    temp_title1 = title.replace(' ', '%20')
    temp_title2 = temp_title1.replace('\'', "%27")
    temp_title3 = temp_title2.replace('’', "%E2%80%99")
    t = temp_title3.replace('‘', "%E2%80%98")
    print('keyword == title check result: ', t)
    if keyword == t:
        print('uzbek')
        for title in soup.find_all("a", {"href": re.compile("^/docs/-[0-9]+"), "target": "_blank"}):
            if title.parent.name == 'td':
                titles.append(title)
        # titles = soup.find_all("a", {"href": re.compile("^/docs/-[0-9]+"), "target": "_blank"})
    else:
        print('russian')
        for title in soup.find_all("a", {"href": re.compile("^/docs/[0-9]+"), "target": "_blank"}):
            if title.parent.name == 'td':
                titles.append(title)

    links = soup.find_all("a", {"title": "WORD шаклида юклаш"})

    starting_titles = list(map((lambda t: t.text.strip()), titles))
    doc_links = list(map((lambda l: f"https://lex.uz{l['href']}"), links))

    context.user_data["file_links"] = doc_links
    context.user_data["file_names"] = starting_titles
    context.user_data['total'] = len(doc_links)

    msgs = create_messages(update, context)
    markups = create_markups(update, context)

    return msgs, markups
