import requests
from bs4 import BeautifulSoup
from time import sleep
from csv import DictWriter

url = "http://quotes.toscrape.com"

def get_quotes(link):
    page = "/page/1/"
    quotes = []
    while page:
        response = requests.get(link+page)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        all_quotes = soup.find_all(class_ = "quote")
        for item in all_quotes:
            text = item.find(class_ = "text").get_text()
            author = item.find(class_ = "author").get_text()
            bio_link = item.find("a")["href"]
            author_page = requests.get(link+bio_link)
            author_page.encoding = "utf-8"
            author_soup = BeautifulSoup(author_page.text, "html.parser")
            birthdate = author_soup.find(class_ = "author-born-date").get_text()
            birthplace = author_soup.find(class_ = "author-born-location").get_text()
            quotes.append({"text": text, "author": author, "bio": bio_link, "birthdate": birthdate, "birthplace": birthplace})
        next = soup.find(class_ = "next")
        if next:
            page = next.find("a")["href"]
            sleep(3)
        else:
            break
    return quotes

if __name__ == '__main__':
    quotes = get_quotes(url)

def write_quotes_to_csv(quotes):
    with open("Quotes.csv", "w", encoding = "utf-8", newline = "") as file:
        headers = ["text", "author", "bio", "birthdate", "birthplace"]
        csv_writer = DictWriter(file, fieldnames= headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)

if __name__ == '__main__':
    write_quotes_to_csv(quotes)
