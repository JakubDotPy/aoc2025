import os
from pathlib import Path

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def setup_driver(cookie_value: str) -> webdriver.Chrome:
    """Set up a headless Chrome WebDriver and authenticate with a session cookie.

    Args:
        cookie_value (str): The session cookie value for authentication.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.

    """
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.get('https://adventofcode.com')
    driver.add_cookie(
        {
            'name': 'session',
            'value': cookie_value.removeprefix('session='),
            'domain': 'adventofcode.com',
        }
    )
    return driver


def crop_image(
    input_path: str, output_path: str, crop_box: tuple[int, int, int, int] = (0, 0, 640, 621)
) -> None:
    """Crop an image to the specified dimensions and save it to the output path.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the cropped image.
        crop_box (Tuple[int, int, int, int], optional):
            The cropping box defined as (left, upper, right, lower).
            Defaults to (0, 0, 640, 621).

    """
    with Image.open(input_path) as img:
        cropped = img.crop(crop_box)
        cropped.save(output_path)


def take_screenshot(driver: webdriver.Chrome, url: str, selector: str, output_name: str) -> None:
    """Capture a screenshot of a web element specified by a CSS selector and crop it.

    Args:
        driver (webdriver.Chrome): The WebDriver instance used to navigate and take screenshots.
        url (str): The URL of the web page to capture.
        selector (str): The CSS selector of the element to capture.
        output_name (str): Path to save the screenshot.

    """
    driver.get(url)
    element = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
    element.screenshot(output_name)
    crop_image(output_name, output_name)


def get_year() -> str:
    """Determine the year based on the parent folder name.

    Returns:
        str: The year extracted from the folder name.

    """
    folder_name = Path(__file__).parents[2].name
    return folder_name.split('aoc')[1]


def main() -> None:
    """Set up environment, capture screenshot, and ensure proper cleanup of resources."""
    Path('screenshots').mkdir(parents=True, exist_ok=True)
    cookie = os.getenv('COOKIE')
    if not cookie:
        msg = 'COOKIE environment variable is not set.'
        raise ValueError(msg)

    driver = setup_driver(cookie)
    year = get_year()
    try:
        take_screenshot(
            driver,
            f'https://adventofcode.com/{year}',
            'body > main > pre',
            'screenshots/aoc-screenshot.png',
        )
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
