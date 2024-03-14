from bs4 import BeautifulSoup
import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

urls = []

# parent page

url = "https://www.theverge.com/tech/archives/2"
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")

link_tags = soup.findAll("a", class_="hover:shadow-underline-inherit")
for tag in link_tags:
    url = tag["href"]
    if url[:5] == "/2024":
        urls.append("https://www.theverge.com/" + tag["href"])

urls = list(set(urls))

news = []

# individual pages

for url in urls:
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    # news div
    div_element = soup.find(
        "div",
        class_="mx-0 mb-40 basis-full rounded-2xl bg-[#EEE6FF] p-10 sm:mx-0 md:mx-10 md:p-20",
    )

    if div_element:

        # title
        title_element = div_element.find(
            "div", class_="inline pr-4 text-17 font-bold md:text-17"
        )
        if title_element:
            title = title_element.text.strip()
        else:
            title = ""

        # author
        author_element = div_element.find(
            "div",
            class_="flex flex-row flex-wrap items-center pb-10 font-polysans text-11 uppercase leading-130 tracking-15 text-gray-33 dark:text-gray-cc md:pb-6",
        ).find("a")
        if author_element:
            author_name = author_element.text
            author_link = "https://www.theverge.com" + author_element["href"]
        else:
            author_name = ""
            author_link = ""

        # date and time
        time_element = div_element.find("time")
        datetime = time_element.text[7:].split(" At ")

        month = datetime[0][:3]

        if month == "Jan":
            datetime[0] = "January" + datetime[0][3:]
        if month == "Feb":
            datetime[0] = "February" + datetime[0][3:]
        if month == "Mar":
            datetime[0] = "March" + datetime[0][3:]
        if month == "Apr":
            datetime[0] = "April" + datetime[0][3:]
        if month == "Jun":
            datetime[0] = "June" + datetime[0][3:]
        if month == "Jul":
            datetime[0] = "July" + datetime[0][3:]
        if month == "Aug":
            datetime[0] = "August" + datetime[0][3:]
        if month == "Sep":
            datetime[0] = "September" + datetime[0][3:]
        if month == "Oct":
            datetime[0] = "October" + datetime[0][3:]
        if month == "Nov":
            datetime[0] = "November" + datetime[0][3:]
        if month == "Dec":
            datetime[0] = "December" + datetime[0][3:]

        content_element = div_element.find(
            "div", class_="font-polysans text-black dark:text-gray-ef leading-130"
        )
        content_elements = content_element.find_all("p")
        content = " ".join([element.text.strip() for element in content_elements])

        # reference
        ref_element = soup.find("div", class_="relative z-10 font-polysans leading-120")

        if ref_element:
            ref_title = ref_element.find("p").text[1:-1]
            ref_link = ref_element.find("a").get("href")
        else:
            ref_title = ""
            ref_link = ""

        new_buff = {
            "title": title,
            "author": author_name,
            "author_link": author_link,
            "date": datetime[0],
            "time": datetime[1],
            "content": content,
            "ref": ref_title,
            "ref_link": ref_link,
        }
        news.append(new_buff)

with open("json/verge.json", "w", encoding="utf-8") as fout:
    json.dump(news, fout)
