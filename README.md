# Bus Info Scraper with Selenium & Dynamic Filtering using Streamlit

This project is a comprehensive tool designed to scrape bus route details from the Bus Info Scraper website, store the data in a MySQL database, and provide an interactive dashboard for dynamic filtering and visualization. The project supports scraping bus data for 10 different states in India, making it a versatile solution for analyzing bus routes, fares, seat availability, and other relevant details.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Web Scraping with Selenium:**
  - Scrapes bus details including route names, bus names, arrival times, durations, fares, seat availability, ratings, departure locations, and arrival locations.
  - Implements dynamic scraping logic to handle different state-specific routes and pagination.

- **Data Storage with MySQL:**
  - Stores scraped data in a MySQL database for easy access and persistent storage.
  - Automatically creates tables if they do not exist, ensuring smooth integration.

- **Interactive Dashboard with Streamlit:**
  - Provides an interactive dashboard for exploring and analyzing bus routes.
  - Offers dynamic filtering options by route, fare, and other criteria.
  - Includes graphical representations like bar charts, line charts, and histograms for visual data analysis.

- **Multi-State Support:**
  - Includes scraping logic for 10 different states: Kerala, Karnataka, Rajasthan, Bengal, Himachal Pradesh, Assam, Uttarakhand, Bihar, Punjab, and Chandigarh.
  - Allows users to switch between states and visualize the respective bus data.

- **CSV Export:**
  - Enables users to download the filtered bus details as a CSV file for further analysis or record-keeping.

## Technologies Used

- **Python**: The core programming language for scraping, data processing, and dashboard development.
- **Selenium**: A web scraping tool to interact with web pages and extract data dynamically.
- **MySQL**: Database management system for storing the scraped data.
- **Streamlit**: A Python-based web framework for creating interactive and data-driven dashboards.
- **Pandas**: A data manipulation and analysis library.
- **Matplotlib & Plotly**: Libraries for data visualization and plotting.
