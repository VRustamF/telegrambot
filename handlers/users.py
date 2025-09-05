from aiogram import Router, F

from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from keyboards.pagination_kb import create_inline_kb
from keyboards.bookmarks_kb import create_bookmarks_buttons
from lexicon.lexicon import LEXICON
from filters.filters import isDigit, BookmarkPage, DelBookmark

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message, db: dict):
    await message.answer(text=LEXICON['/start'])

    if message.from_user.id not in db['users']:
        db['users'][message.from_user.id] = db['userdata']


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])


@router.message(Command(commands=['beginning', 'continue']))
async def process_beginning_command(message: Message, book: dict, db: dict):
    total_pages = len(book)
    await message.answer(
        text=book[1],
        reply_markup=create_inline_kb(current=1, total=total_pages)
                         )


@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message, book: dict, db: dict):
    if db['users'][message.from_user.id]['bookmarks']:
        bookmarks = db['users'][message.from_user.id]['bookmarks']
        await message.answer(text=LEXICON['/bookmarks'], reply_markup=create_bookmarks_buttons(bookmarks=bookmarks))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(F.data == 'backward')
async def process_backward(callback: CallbackQuery, book: dict, db: dict):
    if db['users'][callback.from_user.id]['page'] == 1:
        await callback.answer()
    else:
        db['users'][callback.from_user.id]['page'] -= 1
        page = db['users'][callback.from_user.id]['page']
        await callback.message.edit_text(
            text=book[page],
            reply_markup=create_inline_kb(current=page, total=len(book))
        )
        await callback.answer()


@router.callback_query(F.data == 'forward')
async def process_forward(callback: CallbackQuery, book: dict, db: dict):
    if db['users'][callback.from_user.id]['page'] == len(book):
        await callback.answer()
    else:
        db['users'][callback.from_user.id]['page'] += 1
        page = db['users'][callback.from_user.id]['page']
        await callback.message.edit_text(
            text=book[page],
            reply_markup=create_inline_kb(current=page, total=len(book))
        )
        await callback.answer()


@router.callback_query(isDigit())
async def process_set_bookmark(callback: CallbackQuery ,book: dict, db: dict):
    page = db['users'][callback.from_user.id]['page']
    db['users'][callback.from_user.id]['bookmarks'].add(f'{page} - {book[page]}')
    await callback.answer('Страница добавлена в закладки!')


@router.callback_query(BookmarkPage())
async def process_get_page_from_bookmark(callback: CallbackQuery, book: dict):
    page = int(callback.data[0])
    await callback.message.edit_text(
        text=book[page],
        reply_markup=create_inline_kb(current=page, total=len(book))
    )


@router.callback_query(F.data == 'del')
async def create_del_bookmark_kb(callback: CallbackQuery, db: dict):
    bookmarks = db['users'][callback.from_user.id]['bookmarks']
    await callback.message.edit_text(
         text=LEXICON['edit_bookmarks'],
         reply_markup=create_bookmarks_buttons(bookmarks=bookmarks, delete='delete')
     )


@router.callback_query(DelBookmark())
async def process_del_bookmark(callback: CallbackQuery, db: dict):
    del_bk = callback.data[0]
    bookmarks = db['users'][callback.from_user.id]['bookmarks']

    for bk in bookmarks.copy():
        if bk.startswith(del_bk):
            bookmarks.remove(bk)

    await callback.message.edit_text(
        text=LEXICON['edit_bookmarks'],
        reply_markup=create_bookmarks_buttons(bookmarks=bookmarks, delete='delete')
    )


@router.callback_query(F.data == 'cancel')
async def process_cancel(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])