# Web Scraper and Bot Automation Project

This project is a comprehensive web scraping and automation solution designed to extract companies information from specific websites, organize the data, and store it in a database. The project also includes a bot that interacts with users and retrieves information from the database.

## Project Structure

The project is organized into the following modules:

### 1. `Data_scraping.py`
This module handles the web scraping functionality. It uses `requests` and `BeautifulSoup` to scrape and parse data from the specified websites.

#### Main Components:
- **Scraper Class**:
  - `__init__(self, url, website_headers, category, website_origin)`: Initializes the scraper with the target URL, headers, category, and origin.
  - `get_filters()`: Retrieves and returns available filters (categories) from the website.
  - `scrape_company_by_category(company_filter)`: Scrapes data for companies based on the selected filter (category).
  - `get_more_info_of_company(company_url)`: Retrieves detailed information about a specific company.

### 2. `Scrape_organizer.py`
This module manages the scraping process and organizes the data by interacting with the database.

#### Main Components:
- **Organizer Class**:
  - `__init__(self, scraper_object, db_session, db_company)`: Initializes the organizer with a scraper object, database session, and company model.
  - `big_cycle()`: Main loop that iterates over all categories, scrapes the company data, and stores it in the database.

### 3. `run.py`
This module is the entry point for running the bot. It initializes the bot and starts polling for user commands.

#### Main Components:
- **main()**: 
  - Initializes the database.
  - Sets up the bot with the provided token.
  - Starts polling for bot commands and interactions.

### 4. `Bot` Package
This package contains the bot's functionality, including handlers for user commands, keyboards for user interactions, and message formatting.

#### Key Modules:
- `handlers.py`: Handles incoming bot commands and user interactions.
- `keyboard.py`: Manages the interactive keyboards presented to the user.
- `message_maker.py`: Formats and generates messages to be sent by the bot.

### 5. `DB` Package
This package handles the database operations, including defining the database schema and managing sessions.

#### Key Modules:
- `Companies.py`: Defines the schema for storing company information.
- `database.py`: Contains functions for database creation and session management.
- `Users.py`: Defines the schema for storing user information.
- `requests.py`: Handles database requests.

## Database
The project uses SQLite as the database backend. The database file is stored with a `.sqlite` extension and contains tables for companies, users, and other relevant information.

## Configuration
The project uses a `config.py` file to store configuration variables such as:
- `website_url`: The base URL of the target website.
- `headers`: HTTP headers for requests.
- `category_url`: URL template for scraping specific categories.
- `TOKEN`: The API token for the bot.

## Running the Project

1. **Set Up Configuration**: Ensure that the `config.py` file is correctly configured with the necessary variables.
2. **Run the Scraper**: You can execute the scraping process by running the `Scrape_organizer.py` file.
3. **Start the Bot**: Run the `run.py` file to start the bot and begin interacting with users.

## TODO
- Update database fields to accommodate new data fields.
- Improve error handling and logging throughout the project.

## Dependencies
The project requires the following Python packages:
- `requests`
- `beautifulsoup4`
- `aiogram`
- `lxml`
- `sqlite3` (Python’s standard library)

Install the dependencies using pip:
```bash
pip install requests beautifulsoup4 aiogram lxml
```
