from bs4 import BeautifulSoup
import requests


url = "https://www.theverge.com/tech/archives/2"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html")

div_elements = soup.find_all(
    "div",
    class_="duet--content-cards--content-card relative flex flex-row border-b border-solid border-gray-cc px-0 last-of-type:border-b-0 dark:border-gray-31 py-16 hover:bg-[#FBF9FF] dark:hover:bg-gray-18 max-w-container-md last-of-type:border-b-0 md:pl-20",
)
link_tags = soup.findAll("a", class_="hover:shadow-underline-inherit")
urls = []
for tag in link_tags:
    url = tag["href"]
    if url[:5] == "/2024":
        urls.append("https://www.theverge.com/" + tag["href"])

urls = list(set(urls))


news = []

for url in urls:
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html")
    div_elements = soup.find_all(
        "div",
        class_="mx-0 mb-40 basis-full rounded-2xl bg-[#EEE6FF] p-10 sm:mx-0 md:mx-10 md:p-20",
    )

    for div_element in div_elements:
        title_element = div_element.find(
            "div", class_="inline pr-4 text-17 font-bold md:text-17"
        )
        title = title_element.text.strip()

        content_elements = div_element.find_all("p")
        content = "\n".join([element.text.strip() for element in content_elements])

    # title_element = soup.find('div', class_='inline pr-4 text-17 font-bold md:text-17')
    # title = title_element.text.strip()
    # content_elements = soup.find_all('p')
    # content = '\n'.join([element.text.strip() for element in content_elements])

    ref_elements = soup.find_all(
        "div", class_="relative z-10 font-polysans leading-120"
    )

    if ref_elements:
        for ref_element in ref_elements:
            a_tags = ref_element.find_all("a")
            for a_tag in a_tags:
                href = a_tag.get("href")

    print("Title:", title)
    print("Content:", content)
    print("Href:", href)
