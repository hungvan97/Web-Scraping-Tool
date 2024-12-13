from selenium import webdriver
from time import sleep
import argparse
import json
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

## saving method
def save_to_json(videos_data, filename="videos.json") -> None:
    with open(file=filename, mode='w', encoding='utf-8') as f:
        json.dump(obj=videos_data, fp=f, ensure_ascii=True, indent=2)

def save_to_csv(videos_data, filename="videos.csv") -> None:
    with open(file=filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f=f, fieldnames=["url", "duration", "title", "views", "uploaded"])
        writer.writeheader()
        writer.writerows(rowdicts=videos_data)

def main() -> None:
    ## parse script's argument
    parser = argparse.ArgumentParser(description="Youtube Video Scrapping tool")
    parser.add_argument('-f', '--format', choices=['json', 'csv'], default='json', help="Output saved file format")
    parser.add_argument('-u', '--url', default="https://www.youtube.com/@AspenTech/videos", help="Youtube URL to scrape")
    parser.add_argument('-sl', '--sleep', type=int, default=3, help='time interval for complete HTML loading')
    parser.add_argument('-sc', '--scroll', type=int, default=4, help='Stimulate scroll down behaviour number of time')
    args = parser.parse_args() 

    ## scraping method
    # get URL, wait for 3 seconds for complete loading
    driver = webdriver.Chrome()
    driver.get(url=args.url)
    sleep(args.sleep)

    # stimulate scroll down behaviour 4 time, wait for 3 seconds inbetween for complete loading
    html = driver.find_element(by=By.TAG_NAME, value='html')
    for i in range(args.scroll):
        html.send_keys(Keys.END)
        sleep(args.sleep)

    videos_data = []
    video_elements = driver.find_elements(by=By.TAG_NAME, value='ytd-rich-grid-media')
    for vid in video_elements:
        container = vid.find_element(by=By.XPATH, value='.//div[@id="dismissible"]')
        url = container.find_element(by=By.XPATH, value='.//a[@id="video-title-link"]').get_attribute(name='href')
        duration = container.find_element(by=By.XPATH, value='.//div[@id="time-status"]/span').get_attribute(name='aria-label')
        title = container.find_element(by=By.XPATH, value='.//h3/a/yt-formatted-string').text
        metadata = container.find_elements(by=By.XPATH, value='.//div[@id="metadata-line"]/span')
        views = metadata[0].text
        uploaded = metadata[1].text
        videos_data.append(
            {
                "url": url,
                "duration":  duration,
                "title" : title,
                "views": views,
                "uploaded" : uploaded
            }
        )
    driver.close()

    # Modified save logic
    if args.__format__ == 'json':
        save_to_json(videos_data=videos_data)
    else:
        save_to_csv(videos_data=videos_data)


if __name__ == "__main__":
    main()