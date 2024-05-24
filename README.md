# Hanze University Class Schedule Scraper

This project is a web scraper designed to fetch class schedules from Hanze University's DigiRooster using Selenium and BeautifulSoup. It provides a command-line interface for users to select the year and class group, and then retrieves and displays the schedule for the selected parameters.

## Features

- Interactive selection of year and class group.
- Fetches current week's schedule and allows selection of different weeks.
- Outputs the schedule in a readable format.

## Prerequisites

- Python 3.x
- Microsoft Edge browser
- Edge WebDriver

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/thatdudeyoudontknow/Class_schedule_tool/blob/main/temptes2.0.py
   cd hanze-scraper

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt


***Configuration***
Ensure that you have Microsoft Edge installed on your system. The WebDriver for Edge will be automatically managed by the webdriver_manager package.

## Usage

4. **Run the scraper:**

    ```bash
    python temptes2.0.py

5. **Follow the on-screen prompts:**

You will be asked to select the year.
You will be asked to select the class group.
You can choose the week for which you want to retrieve the schedule.
Optionally, you can add multiple year/class selections.

6. **View the output:**

The scraper will display the schedule for the selected parameters in the console.

## Troubleshooting
Ensure that Microsoft Edge and Edge WebDriver are correctly installed and match the version.
If you encounter a WebDriverException, make sure your Edge WebDriver is compatible with the installed version of Edge.
If the browser window closes unexpectedly, ensure you keep the browser window open until the script finishes running.
Contributing
Contributions are welcome! Please create an issue first to discuss what you would like to change. You can also fork the repository and submit a pull request.

## License
This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.
