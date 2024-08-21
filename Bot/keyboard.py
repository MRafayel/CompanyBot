from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import FIELDS
import DB.requests as rq


async def main_kb():
    main = InlineKeyboardBuilder()
    main.add(InlineKeyboardButton(text="Companies", callback_data="company"))
    main.add(InlineKeyboardButton(text="Update", callback_data="update"))

    return main.adjust(1).as_markup()


async def get_companies():
    category_button = InlineKeyboardBuilder()
    for field_id, field_name in FIELDS.items():
        category_button.add(InlineKeyboardButton(text=field_name,
                                                 callback_data=f"showcomp_{field_id}"
                                                 )
                            )

    category_button.add(InlineKeyboardButton(text="👨‍🦯 Back", callback_data="Home"))
    return category_button.adjust(1).as_markup()


async def see_more(field_id, last_comp_id):
    count = rq.see_more_count(field_id=field_id, last_comp_id=last_comp_id)
    see_more_button = InlineKeyboardBuilder()
    see_more_button.add(InlineKeyboardButton(text=f"Show more ({count})",
                                             callback_data=f"more_{field_id}"))

    see_more_button.add(InlineKeyboardButton(text="🏠 Home Page", callback_data="Home"))

    see_more_button.add(InlineKeyboardButton(text="👨‍🦯 Back", callback_data=f"company"))

    return see_more_button.adjust(1).as_markup()


async def go_home():
    home_button = InlineKeyboardBuilder()

    home_button.add(InlineKeyboardButton(text="🏠 Go Home", callback_data="Home"))

    return home_button.adjust(1).as_markup()


async def company_title(company_id):
    title_button = InlineKeyboardBuilder()

    title_button.add(InlineKeyboardButton(text="Description", callback_data=f"title_{company_id}"))

    return  title_button.adjust(1).as_markup()


async def company_title_back(company_id):
    title_button = InlineKeyboardBuilder()

    title_button.add(InlineKeyboardButton(text="👨‍🦯 Back", callback_data=f"titleback_{company_id}"))

    return  title_button.adjust(1).as_markup()

if __name__ == '__main__':
    pass
