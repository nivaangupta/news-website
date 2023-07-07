import streamlit
from bs4 import BeautifulSoup
from urllib.request import urlopen
from newspaper import Article
import nltk

nltk.download("punkt")
streamlit.set_page_config(page_title='Shorts📰 - Get Summarised News', page_icon='./data/icon.png')


def fetch_news(endpoint):
    webpage = urlopen(endpoint)
    content = webpage.read()
    webpage.close()
    scrapped_data = BeautifulSoup(content, 'xml')
    news_list = scrapped_data.find_all('item')
    return news_list


def fetch_news_topic(topic):
    endpoint = 'https://news.google.com/rss/search?q={}'.format(topic)
    return fetch_news(endpoint)


def fetch_news_general():
    endpoint = 'https://news.google.com/rss'
    return fetch_news(endpoint)


def display_news(ls, an):
    c = 0
    for news in ls:
        c += 1
        streamlit.write('**({}) {}**'.format(c, news.title.text))
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            print(e)
        with streamlit.expander(news.title.text):
            streamlit.markdown(
                '''<h6 style="text-align: justify;">{}</h6>'''.format(news_data.summary),
                unsafe_allow_html=True
            )
            streamlit.markdown("[Read more at {}...]({})".format(news.source.text, news.link.text))
        streamlit.success("Published Date: " + news.pubDate.text)
        if c >= an:
            break


def run():
    streamlit.title("Shorts📰 - Get Summarised News")
    category = ['--Select--', 'Top Trending News', 'News by Topic', 'News by Topic Search']
    category_options = streamlit.selectbox('Select your Category', category)
    if category_options == category[0]:
        streamlit.warning('Please select a category to get NEWS')
    elif category_options == category[1]:
        streamlit.subheader(" Here are some Top Trending News ")
        articles_per_page = streamlit.slider("Articles per Page", min_value=5, max_value=25, step=5)
        news_list = fetch_news_general()
        display_news(news_list, articles_per_page)
    elif category_options == category[2]:
        topics = ['--Choose Topics--', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE', 'HEALTH']
        chosen_topic = streamlit.selectbox("Choose the Topic", topics)
        if chosen_topic == topics[0]:
            streamlit.warning("Please choose a topic to view NEWS")
        else:
            articles_per_page = streamlit.slider("Articles per Page", min_value=5, max_value=25, step=5)
            news_list = fetch_news_topic(chosen_topic)
            if news_list:
                streamlit.subheader(f"{chosen_topic} NEWS")
                display_news(news_list, articles_per_page)
            else:
                streamlit.error(f"No latest NEWS on {chosen_topic}")
    elif category_options == category[3]:
        user_topic = streamlit.text_input("Enter the topic you want to search NEWS for")
        articles_per_page = streamlit.slider("Articles per Page", min_value=5, max_value=25, step=5)
        if streamlit.button("Search") and user_topic != '':
            user_topic_pr = user_topic.replace(' ', '')
            news_list = fetch_news_topic(topic=user_topic_pr)
            if news_list:
                streamlit.subheader(f"{user_topic.capitalize()} NEWS")
                display_news(news_list, articles_per_page)
            else:
                streamlit.error(f"No NEWS for for the topic: {user_topic}")
        else:
            streamlit.warning("Please type the topic name to search NEWS")


if __name__ == "__main__":
    run()




