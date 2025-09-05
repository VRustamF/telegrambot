from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

class isDigit(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        return callback.data.isdigit()

class BookmarkPage(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        return callback.data.endswith('page')

class DelBookmark(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        return callback.data.endswith('delete')