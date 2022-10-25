from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
# import json
from deta import Deta
from bs4 import BeautifulSoup
from urllib.request import urlopen

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

def my_cron_job():
    # url = "http://olympus.realpython.org/profiles/dionysus"
    url = "https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    # print(soup.get_text())

    # 'Technology',
    _myInterest = [ 'Science', 'Health' ]
    topic_links = []

    for i in soup.find_all("a"):
        try:
            topic = i['aria-label']
            if topic in _myInterest:
                topic_link = i['href']
                topic_link = "https://news.google.com" + topic_link[1:]
                topic_links.append(topic_link)

        except:
            1

    print(topic_links)

    #* first heading content path
    # .xrnccd.F6Welf.R7GTQ.keNKEd.j7vNaf > article > h3 > a

    #* second heading content path
    # .xrnccd.F6Welf.R7GTQ.keNKEd.j7vNaf > .SbNwzf.eeoZZ > article > h4 > a

    #* common image path
    # .xrnccd.F6Welf.R7GTQ.keNKEd.j7vNaf > a > figure > img

    # _articalClass = ['NiLAwe', 'mi8Lec', 'gAl5If', 'jVwmLb', 'Oc0wGc', 'R7GTQ', 'keNKEd', 'j7vNaf', 'nID9nc']
    _articalClass = ['xrnccd', 'F6Welf', 'R7GTQ', 'keNKEd', 'j7vNaf']

    my_scrapped_data_science = []
    my_scrapped_data_technology = []

    def data_extor(div_body, topic_link):
        first_heading = div_body.select('article > h3 > a')[0]
        second_heading = div_body.select('.SbNwzf.eeoZZ > article > h4 > a')[0]
        image_heading = div_body.select('a > figure > img')[0]

        print("c0")

        first_heading_content = first_heading.string
        first_heading_link = first_heading['href']
        first_heading_link = "https://news.google.com" + first_heading_link[1:]

        print("c1")

        second_heading_content = second_heading.string
        second_heading_link = second_heading['href']
        second_heading_link = "https://news.google.com" + second_heading_link[1:]

        print("c2")

        image_heading_link = image_heading['src']

        print("c4")

        article_object = {
            "first_heading_content": first_heading_content,
            "first_heading_link": first_heading_link,
            "second_heading_content": second_heading_content,
            "second_heading_link": second_heading_link,
            "image_heading_link": image_heading_link
        }

        topic_link_index = topic_links.index(topic_link)

        if topic_link_index == 0:
            my_scrapped_data_science.append(article_object)
            print("c5 s", topic_link_index)
        else:
            my_scrapped_data_technology.append(article_object)
            print("c5 t", topic_link_index)



    for topic_link in topic_links:
        topic_page = urlopen(topic_link)
        topic_html = topic_page.read().decode("utf-8")
        topic_soup = BeautifulSoup(topic_html, "html.parser")
        # print(topic_soup.get_text())
        for div_body in topic_soup.findAll(True, {'class': _articalClass}):
            # first_heading_links.append(div_body)
            # my_scrapped_data
            try:
                data_extor(div_body, topic_link)            
            except:
                1


    science_articles = []
    technology_articles = []

    def delete_science_duplicates():
        seen = set()
        for d in my_scrapped_data_science:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                science_articles.append(d)

    def delete_tech_duplicates():
        seen = set()
        for d in my_scrapped_data_technology:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                technology_articles.append(d)

    delete_science_duplicates()
    delete_tech_duplicates()

    print(len(technology_articles), len(science_articles))
    
    # the json file where the output must be stored
    # technology_articles_out_file = open("technology_articles.json", "w")
    # science_articles_out_file = open("science_articles.json", "w")
    
    # json.dump(technology_articles, technology_articles_out_file, indent = 6)
    # json.dump(technology_articles, science_articles_out_file, indent = 6)
    # 
    # technology_articles_out_file.close()
    # science_articles_out_file.close()

    def save_articles_to_database():
        try:
            deta = Deta('d0qprvt5_hbyBNnNXABFzmPQq3e8vhBhmXde8w42k') # configure your Deta project

            db_science = deta.Base('science_articles')
            db_health = deta.Base('health_articles')

            db_science.put(science_articles)
            db_health.put(technology_articles)

            print("data saved")
        except:
            print("faild to save")

    save_articles_to_database()



with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    manial_trigger = st.slider("Number away to trigger", 1, 5000, 2000)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns



    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))

