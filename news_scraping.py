import requests
import pandas as pd
import re
from urllib.parse import urljoin
from goose3 import Goose
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

url = 'https://www.thehindu.com/'

response = requests.get(url)
http_encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
html_encoding = EncodingDetector.find_declared_encoding(response.content, is_html=True)
encoding = html_encoding or http_encoding
soup = BeautifulSoup(response.content, from_encoding=encoding)

final_urls = []
for link in soup.select("a[href$='.ece']"):
    href = link.attrs.get("href")
    final_urls.append(href)
#   href = urljoin(url, href)
#   if pattern in href:
#     # final_urls = [href]
        
unique_urls = set(final_urls)
unique_urls_list = list(unique_urls)


#Get the Title, Author and Text of Each URL
#Create the lists of all variables
final_title_list = []
final_text_list = []
final_source_list = []
for data in unique_urls_list:
  # request = requests.get(data)
    g = Goose()
    article = g.extract(url=data)
    title = article.title
    text = article.cleaned_text
    domain = article.domain
    source=re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))',domain)
    final_title_list.append(title)
    final_text_list.append(text)
    final_source_list.extend(source)
    dict_1 = {'title': final_title_list, 'text': final_text_list, 'author':final_source_list}
    df = pd.DataFrame({key: pd.Series(value) for key, value in dict_1.items()})
    df.to_csv('TheHindu_DataSet.csv', encoding='utf-8', index=False)
# #Download the file in your local
# files.download("TheHindu_DataSet.csv")