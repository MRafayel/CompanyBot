from Data_scraping import Scraper
from config import website_url, headers, category_url

from DB.database import Session
from DB.Companies import Company


# TODO field name fix (update new fields in DB)
class Organizer:
    def __init__(self, scraper_object: type(Scraper), db_session: type(Session), db_company: type(Company)):
        self.scraper = scraper_object(url=website_url, website_headers=headers, category=category_url, website_origin=None)
        self.Session = db_session
        self.Company = db_company

    def big_cycle(self):
        fields = self.scraper.get_filters()

        session = self.Session()

        for field_name, field_index in fields:
            companies_pre_info = self.scraper.scrape_company_by_category(company_filter=field_index)

            if len(companies_pre_info) <= session.query(self.Company).filter(self.Company.field == field_index).count():
                print(f"[INFO] There is nothing to add in {field_name}")
                continue
            else:
                for company in companies_pre_info:
                    comp = session.query(self.Company).filter(self.Company.company_id == company.get("company_id")).first()

                    if comp:
                        print(f"[INFO] Company with ID: {company.get('company_id')} in DB")
                        continue
                    else:
                        company_info = self.scraper.get_more_info_of_company(company_url=company.get("company_link"))
                        comp_to_save = self.Company(company_id=company.get("company_id"),
                                                    field_id=field_index,
                                                    name=company.get("company_name"),
                                                    photo=company.get("company_img"),
                                                    title=company_info.get("company_title"),
                                                    location=company_info.get("company_location"),
                                                    employees=company_info.get("company_employees"),
                                                    website=company_info.get("company_website"),
                                                    phone=company_info.get("company_phone"),
                                                    social=("|".join(company_info.get("company_social"))
                                                            if company_info.get("company_social") is not None
                                                            else company_info.get("company_social"))
                                                    )
                        session.add(comp_to_save)
                        session.commit()
                        print(f"[INFO] {company.get('company_id')} successfully saved in DB")

            session.close()

        return True


if __name__ == "__main__":
    pass
