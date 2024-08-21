import aiogram.exceptions
from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
import Bot.keyboard as kb
import DB.requests as rq
from config import FIELDS
from Bot.message_maker import make_product_message


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text="Choose option you need", reply_markup=await kb.main_kb())


@router.callback_query(F.data == "Home")
async def go_home(callback: CallbackQuery):
    await callback.answer(text="Home page 📄")
    await callback.message.edit_text(text="Choose option you need", reply_markup=await kb.main_kb())


@router.callback_query(F.data == "company")
async def choose_company(callback: CallbackQuery):
    await callback.answer(text="Choose company 👀")
    await callback.message.edit_text(text="Choose company you need 👀",
                                     reply_markup=await kb.get_companies()
                                     )


@router.callback_query(F.data == "update")
async def choose_company(callback: CallbackQuery):
    await callback.answer(text="503 Service Unavailable ")
    await callback.message.edit_text(text="The server is currently unable to handle the request due to a temporary "
                                          "overloading or maintenance of the server. The implication is that this is a "
                                          "temporary condition which will be alleviated after some delay.",
                                     reply_markup=await kb.go_home()
                                     )


@router.callback_query(F.data.startswith("showcomp_"))
async def show_companies(callback: CallbackQuery):
    field_id = int(callback.data.split("_")[1])

    await callback.answer(text="Processing 🕔")
    await callback.message.edit_text(text="Searching...")

    last_sent_company_id = rq.get_last_sent_company(field_id=field_id, user_id=callback.from_user.id)

    await callback.message.edit_text(text=f"🔹{hbold(FIELDS.get(str(field_id)))}🔹")
    companies = rq.get_companies(field_id=field_id, last_comp_id=last_sent_company_id)
    for count, company in enumerate(companies):
        try:
            await callback.message.answer_photo(photo=company.photo,
                                                caption=await make_product_message(company=company),
                                                reply_markup=await kb.company_title(company_id=company.company_id)
                                                )
        except aiogram.exceptions.TelegramBadRequest as error:
            print(f"[ERROR] {company.photo} {error}")

    last_comp_id = company.id

    rq.update_user_last_comp(field_id=field_id, last_comp_id=last_comp_id, user_id=callback.from_user.id)

    if rq.check_show_more_ability(field_id=field_id, user_id=callback.from_user.id):
        await callback.message.answer(text="Choose from menu", reply_markup=await kb.see_more(field_id=field_id,
                                                                                              last_comp_id=last_comp_id
                                                                                              )
                                      )
    else:
        # TODO await dont work properly
        rq.clean_user_last_comp_info(user_id=callback.from_user.id, field_id=field_id)
        await callback.message.answer(text="Home page 📄", reply_markup=await kb.main_kb())


@router.callback_query(F.data.startswith("more_"))
async def see_more(callback: CallbackQuery):
    await show_companies(callback)


@router.callback_query(F.data.startswith("title_"))
async def show_title(callback: CallbackQuery):
    company_id = int(callback.data.split("_")[1])

    company = rq.get_company_by_id(company_id=company_id)

    await callback.message.edit_media(media=types.InputMediaPhoto(media=company.photo,
                                                                  caption=company.title[:1000].strip() + "..." if company.title else '🤷‍♂️'
                                                                  ),
                                      reply_markup=await kb.company_title_back(company_id=company_id)
                                      )


@router.callback_query(F.data.startswith("titleback_"))
async def show_title(callback: CallbackQuery):
    company_id = int(callback.data.split("_")[1])

    company = rq.get_company_by_id(company_id=company_id)

    await callback.message.edit_media(media=types.InputMediaPhoto(media=company.photo,
                                                                  caption=await make_product_message(company=company)
                                                                  ),
                                      reply_markup=await kb.company_title(company_id=company_id)
                                      )
if __name__ == '__main__':
    pass
