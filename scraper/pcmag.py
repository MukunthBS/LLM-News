from bs4 import BeautifulSoup
import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

urls = []

# parent pages

for i in range(1, 3):
    url = "https://www.pcmag.com/news?page=" + str(i)
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    link_tags = soup.findAll("h2", class_="text-base font-bold md:text-xl")

    for tag in link_tags:
        a_tag = tag.find("a")
        if a_tag:
            if a_tag["href"][:5] == "/news":
                urls.append("https://www.pcmag.com" + a_tag["href"])

urls = list(set(urls))

news = []

for url in urls:
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    # title
    title_element = soup.find("h1")
    if title_element:
        title = title_element.text.strip()
    else:
        title = ""

    # author and date
    author_date_elements = soup.find(
        "div",
        id="author-byline",
    )

    # date
    date_element = author_date_elements.find(
        "div",
        class_="justify-between md:justify-center inline-block flex w-full items-center md:w-auto",
    )
    if date_element:
        date = date_element.find("div").find("span").text.strip().split("\n")[-1]

    # author
    author_element = author_date_elements.find(
        "div", class_="relative inline-block flex w-full items-center md:w-auto"
    ).find("span")

    if author_element:
        author_details = author_element.find("span", recursive=True)
        if author_details:
            author_name = author_details.text
            author_details = author_element.find("a", recursive=True)
            author_link = "https://www.pcmag.com" + author_details["href"]
        else:
            author_details = author_element.find("a", recursive=True)
            author_name = author_details.text
            author_link = "https://www.pcmag.com" + author_details["href"]

    # content
    content_elements = soup.find("article").find_all("p", recursive=False)
    content = " ".join([element.text.strip() for element in content_elements])

    new_buff = {
        "title": title,
        "author": author_name,
        "author_link": author_link,
        "date": date,
        "content": content,
    }
    news.append(new_buff)

with open("json/pcmag.json", "w", encoding="utf-8") as fout:
    json.dump(news, fout)
