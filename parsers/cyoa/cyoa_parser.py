import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Настройки драйвера
chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


def story_list():
    story_list = []
    driver.get("https://chooseyourstory.com/Stories/")
    story_genres_block_list = driver.find_elements(By.CLASS_NAME, "dark1border")[:-2]
    story_genres_link_list = []
    for story_genre_block in story_genres_block_list:
        story_genres_link_list.append(
            story_genre_block.find_elements(By.CLASS_NAME, "categoryBoxExtras")[1]
            .find_element(By.TAG_NAME, "a")
            .get_attribute("href")
        )

    for story_genre_link in story_genres_link_list:
        driver.get(story_genre_link)
        genre_story_table = driver.find_elements(By.TAG_NAME, "tbody")[
            -1
        ].find_elements(By.TAG_NAME, "tr")
        story_genre = (
            driver.find_element(By.TAG_NAME, "h1")
            .find_element(By.TAG_NAME, "span")
            .text[2:]
        )
        for story_row in genre_story_table[1:]:
            story_title = story_row.find_elements(By.TAG_NAME, "td")[0].text
            story_href = (
                story_row.find_elements(By.TAG_NAME, "td")[0]
                .find_element(By.TAG_NAME, "a")
                .get_attribute("href")
            )
            story_author = story_row.find_elements(By.TAG_NAME, "td")[1].text
            story_author_href = (
                story_row.find_elements(By.TAG_NAME, "td")[1]
                .find_element(By.TAG_NAME, "a")
                .get_attribute("href")
            )
            story_difficulty = (
                story_row.find_elements(By.TAG_NAME, "td")[3]
                .find_element(By.TAG_NAME, "img")
                .get_attribute("alt")
            ).split(" - ")[0]
            story_raiting = story_row.find_elements(By.TAG_NAME, "td")[4].text
            story_list.append(
                [
                    story_genre,
                    story_title,
                    story_href,
                    story_author,
                    story_author_href,
                    story_difficulty,
                    story_raiting,
                ]
            )
    return story_list


# df = pd.DataFrame(
#     story_list(),
#     columns=[
#         "genre",
#         "title",
#         "href",
#         "author",
#         "author_href",
#         "difficulty",
#         "raiting",
#     ],
# )
# df.to_csv("output/stories.csv", index=False)


def story():
    pass


def story_data():
    pass
