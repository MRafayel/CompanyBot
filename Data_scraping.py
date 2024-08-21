import requests
from bs4 import BeautifulSoup
from config import website_core


class Scraper:
    def __init__(self, url, website_headers, category, website_origin):
        self.URL = url
        self.website_headers = website_headers
        self.category_url = category
        self.website_core = website_origin

    def get_filters(self):
        response = requests.get(url=self.URL, headers=self.website_headers).text
        soup = BeautifulSoup(response, "lxml")

        cashed_categories = soup.find(id="companiesstruct-industry").find_all(name="label")
        categories_values = []

        for index, category in enumerate(cashed_categories):
            categories_values.append((category.text.split()[0], index+1))

        return categories_values

    @staticmethod
    def __get_company_img_url(company_soup):
        return company_soup.find('div', class_='job-inner img').find('img').get('src')

    @staticmethod
    def __get_company_name(company_soup):
        return company_soup.find('div', class_='job-inner job-item-title').find('h4', class_="mrgb0").text.strip()

    @staticmethod
    def __get_company_id(company_soup):
        return company_soup.find('div', class_="hb_list_item clearfix web_item_card radius_changes").get("data-id")

    @staticmethod
    def __get_company_link(company_soup):
        return website_core[:-1] + company_soup.find('a', attrs={"data-pjax": 0}).get("href")

    def scrape_company_by_category(self, company_filter):
        company_data = []
        page_number = 1

        while True:
            # get current page
            response = requests.get(url=self.category_url.format(company_filter=company_filter, page_number=page_number),
                                    headers=self.website_headers,
                                    ).text

            # make soup
            soup = BeautifulSoup(response, "lxml")
            # get all companies
            companies = soup.find("div", class_="list-view").find_all("div", attrs={"data-key": True})

            for company in companies:
                # scraping required data
                company_data.append(
                    (
                        {
                            "company_id": int(self.__get_company_id(company_soup=company)),
                            "company_name": self.__get_company_name(company_soup=company),
                            "company_img": self.__get_company_img_url(company_soup=company),
                            "company_link": self.__get_company_link(company_soup=company)
                        }
                    ))
            # If there is next page scraping next page

            if soup.find("ul", class_="pagination") and \
                    soup.find("ul", class_="pagination").find("li", class_="next disabled") is None:
                page_number += 1
            else:
                # End of page. Returning scraped data
                return company_data

    @staticmethod
    def __get_company_title(company_soup):
        title_checker = company_soup.find("div", class_="hs_text_block mb20 col-xs-12")

        if title_checker:
            return title_checker.get_text().strip()

        return None

    @staticmethod
    def __get_company_location(company_soup):
        location_checker = company_soup.find("p", class_="mb25")

        if location_checker:
            return location_checker.get_text().strip()

        return None

    @staticmethod
    def __get_company_employers_count(company_soup):
        if company_soup.find("span", class_="hs_info_icon hs_info_employer_icon"):
            return company_soup.find("p", class_="mb25").find_previous("p").get_text().strip()

        return None

    @staticmethod
    def __get_company_website_url(company_soup):
        website_checker = company_soup.find("a", class_="btn hs_radius16 hs_min_width150 hs_company_website_btn mb10")
        if website_checker:
            return website_checker.get("href")
        return None

    @staticmethod
    def __get_company_phone(company_soup):
        phone_checker = company_soup.find("i", class_="fa fa-phone", attrs={"aria-hidden": True})

        if phone_checker:
            return phone_checker.find_next().get_text().strip()

        return None

    @staticmethod
    def __get_company_social_sites(company_soup):
        try:
            links = []
            for link in company_soup.find("div", class_="mt15").find_all("a", attrs={"rel": "noreferrer noopener nofollow"}):
                links.append(link.get("href"))
            return links

        except AttributeError:
            return None

    def get_more_info_of_company(self, company_url):
        response = requests.get(url=company_url, headers=self.website_headers).text

        soup = BeautifulSoup(response, "lxml")

        company_info = \
            {
                "company_title": self.__get_company_title(company_soup=soup),
                "company_location": self.__get_company_location(company_soup=soup),
                "company_employees": self.__get_company_employers_count(company_soup=soup),
                "company_phone": self.__get_company_phone(company_soup=soup),
                "company_social": self.__get_company_social_sites(company_soup=soup),
                "company_website": self.__get_company_website_url(company_soup=soup)
            }

        return company_info


if __name__ == "__main__":
    pass