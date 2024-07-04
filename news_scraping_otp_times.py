import requests
import datetime
import pandas as pd
import re
from urllib.parse import urljoin
from goose3 import Goose
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

#Get the Current Year
now = datetime.date.today()
year = now.year
currentyear = year.__str__()
#Get the Curent Month
month = (now.month)
if(month == 1 or month == 2 or month == 3 or month == 4 or month == 5 or month == 6 or month == 7 or month == 8 or month == 9):
    currentmonth = '{:02d}'.format(month)
    currentmonth = currentmonth.__str__()
else:
    currentmonth = month.__str__()

#Enter the URL to check for news
url = 'https://www.opindia.com/'
#Append this url for all the articles
url1 = 'https://www.opindia.com/'
#Match the pattern in all the url's
pattern = 'https://www.opindia.com/'+currentyear+'/'+currentmonth+'/'
#Get Response of url
response = requests.get(url)
http_encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
html_encoding = EncodingDetector.find_declared_encoding(response.content, is_html=True)
encoding = html_encoding or http_encoding
soup = BeautifulSoup(response.content, from_encoding=encoding)

final_urls = []
#Get the list of hyperlink on the page
for link in soup.find_all('a'):
    href = link.attrs.get("href")
    href = urljoin(url1, href)
    if pattern in href:
        final_urls.append(href)

# #Remove duplicate URL's        
unique_urls = set(final_urls)
# #Convert it back to lists
unique_urls_list = list(unique_urls)

#Get the Title, Author and Text of Each URL
#Create the lists of all variables
final_title_list = []
final_text_list = []
final_source_list = []
final_image_list = []
for data in unique_urls_list:
    g = Goose()
    article = g.extract(url=data)
    title = article.title
    text = article.cleaned_text
    domain = article.domain
    image = article.infos
    print(image)
    source=re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))',domain)
    final_title_list.append(title)
    final_text_list.append(text)
    final_source_list.extend(source)
    dict_1 = {'title': final_title_list, 'text': final_text_list, 'author':final_source_list}
    df = pd.DataFrame({key: pd.Series(value) for key, value in dict_1.items()})
    # print(df)
    # df.to_csv('OPTimes_news.csv', encoding='utf-8', index=False)
# #Download the file in your local