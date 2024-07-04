from GoogleNews import GoogleNews
googlenews = GoogleNews()

googlenews = GoogleNews(lang='en')
googlenews.get_news('india road accident')
googlenews.search('india road accident')

result_0 = googlenews.page_at(1)

desc_1 = googlenews.get_texts()
link_1 = googlenews.get_links()

for i in list(range(2, 70)):

    result = googlenews.page_at(i)
    desc = googlenews.get_texts()
    link = googlenews.get_links()

    desc_1 = desc_1 + desc
    link_1 = link_1 + link
    # print("link_1:: ",link_1)

    import pandas as pd

    column_names = ["description_text", 'link']
    df = pd.DataFrame(columns = column_names)

    df['description_text'] = desc_1
    df['link'] = link_1

    df.to_csv('google_news.csv', index = False)