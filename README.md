# Job Listings, Crime Rates, and Cost of Living by U.S. States

## Overview
This project fetches job listings for a user-specified keyword (e.g., a major or job title) across multiple randomly selected U.S. states, then augments this data with crime rates and cost of living indices for each state. This can provided a valuable source of data to someone intending to move to a different state based on their job, so they can easily access some of the openings in their field all over the US, while also having data related to how expensive it is to live there and what the statistics related to safety look like. The data is gathered using APIs and web scraping, and presented in a clean, structured format. 

### Key Features:
- **Job Listings**: Uses the Jooble API to collect job listings based on user input.
- **Crime Rates**: Scrapes data from the World Population Review to get crime rates by state.
- **Cost of Living**: Scrapes cost of living index data by state from World Population Review.
- **Structured Data**: Outputs all relevant data (job title, location, crime rates, cost of living) in a pandas DataFrame.

## Table of Contents
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Sources](#data-sources)
- [Contributing](#contributing)
- [License](#license)

## Technologies Used
- **Python 3.x**: Core programming language.
- **Requests**: For making API calls.
- **BeautifulSoup (bs4)**: For web scraping.
- **Pandas**: For data manipulation and presentation.


## Usage
1. Run the script:
   ```bash
   python job_listing_scraper.py
   ```

2. Enter a keyword when prompted (e.g., "Software Engineer" or "Marketing").

3. The program will:
   - Randomly select 10 U.S. states.
   - Fetch job listings related to the keyword in each state.
   - Scrape crime rates and cost of living index data for the job listing states.
   - Display and store the final data in a pandas DataFrame.

## Project Structure
```
📁 job-listings-and-state-data
│
├── README.md               # Project documentation
├── ETHICS.md               # Ethical considerations
├── job_listing_scraper.py   # Main script
├── requirements.txt        # Dependencies
└── data                    # (Optional) Output data files
```

## Data Sources
- **Jooble API**: For fetching job listings.
- **World Population Review**: For scraping crime rates and cost of living indices.
