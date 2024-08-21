from aiogram.utils.markdown import hbold, hcode, hlink
from DB.Companies import Company
from config import FIELDS
import re


async def make_product_message(company: Company):
    socials = []
    if company.social:
        socials = re.findall(pattern=r'(?<=\.)(\w+)(?=\.)', string=company.social)
    card = f"{hbold('Name:')} {hlink(company.name, company.website)}\n\n" \
           f"{hbold('Field:')} {FIELDS.get(str(company.field_id))}\n\n" \
           f"{hbold('Location:')} {company.location.split(':')[1].strip() if company.location else '🤷‍♂️'}\n\n" \
           f"{hbold('Employees:')} {hcode(company.employees.split('`')[1].strip() if company.employees else '🤷‍♂️')}\n\n" \
           f"{hbold('Phone:')} {hcode(company.phone if company.phone else '🤷‍♂️')}\n\n" \
           f"{hbold('Social accounts:')} {' | '.join([hlink(social, link) for social, link in zip(socials, company.social.split('|'))]) if socials else '🤷‍♂️'}\n\n"

    return card


if __name__ == '__main__':
    pass
