%%writefile app.py
# Import the libraries.
import streamlit as st
import pandas as pd
import numpy as np
from st_card_component import card_component
from streamlit_tags import st_tags
import random
import altair as alt
import requests

#set config for website
st.set_page_config(page_title="GovSkills", page_icon='🛠️')

#hide menu
#hide_menu_style = """
#        <style>
#        #MainMenu {visibility: hidden;}
#        </style>
#        """
#st.markdown(hide_menu_style, unsafe_allow_html=True)


#import data
stats = pd.read_csv("https://raw.githubusercontent.com/Max-Tee/GovSkills/main/stats_df.csv")
timeseries = pd.read_csv("https://raw.githubusercontent.com/Max-Tee/GovSkills/main/timeseries_skill.csv")

skills_list = list(stats['Item'])


#title, add animation 
st.markdown("<h1 style='text-align: center;'>Now hiring <span style='font-weight: bold; color: #4287f5;'>Tableau</span> skills!</h1>", unsafe_allow_html=True)
st.write("The federal government currently has **_21,453_** open jobs. See what tech skills are trending and join the federal workforce!")

#st.subheader("Search by skill:")
keywords = st_tags(
    label='',
    text='Search for skill and press enter',
    #value=['Zero', 'One', 'Two'],
    suggestions=skills_list,
    maxtags = 1,
    key='1')

while len(keywords) == 0:


    trending = ["Power BI","Tableau","Python","SPSS","Machine Learning","Data Engineering"]

    charts = []
    for i in trending:
        timeseries_filt = timeseries[timeseries['Item']==i]

        chart = alt.Chart(timeseries_filt).mark_area(
                line={'color':'#4287f5'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color='white', offset=0),
                        alt.GradientStop(color='#4287f5', offset=1)],
                    x1=1,
                    x2=1,
                    y1=1,
                    y2=0
                )
            ).encode(
                alt.X('PostedData_Formatted:T'),
                alt.Y('count_jobs_2022:Q',scale=alt.Scale(domain=(0,150)))
            ).properties(
                width=200,
                height=200
            )
        charts.append(chart)

    st.subheader("Trending Tech Skills")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(trending[0])
        st.altair_chart(charts[0], use_container_width=True)
        st.write(trending[1])
        st.altair_chart(charts[1], use_container_width=True)

    with col2:
        st.write(trending[2])
        st.altair_chart(charts[2], use_container_width=True)
        st.write(trending[3])
        st.altair_chart(charts[3], use_container_width=True)

    with col3:
        st.write(trending[4])
        st.altair_chart(charts[4], use_container_width=True)
        st.write(trending[5])
        st.altair_chart(charts[5], use_container_width=True)


    st.subheader("Open Tech Roles")
    col6, col7, col8 = st.columns(3)

    with col6:
        hasClicked = card_component(
        title="Management Analyst",
        context="Posted on 9/12/2022",
        highlight_start = 0,
        highlight_end = 0,
        score = "Department of Defense",
        url="https://usajobs.gov"
        )
    with col7:
        card_component(
        title="Management Analyst",
        context="Posted on 9/12/2022",
        highlight_start = 0,
        highlight_end = 0,
        score = "Department of Agriculture",
        url="https://usajobs.gov"
        )
    with col8:
        card_component(
        title="Management Analyst",
        context="Posted on 9/12/2022",
        highlight_start = 0,
        highlight_end = 0,
        score = "Department of Commerce",
        url="https://usajobs.gov"
    )

    st.stop()


else:
    while keywords[0] in skills_list:

        skill = keywords[0]

        stats_filt = stats[stats['Item'] == skill] 
        job_count = stats_filt.loc[stats_filt['Item']==skill, 'count_jobs_2022'].iloc[0]
        agency_count = stats_filt.loc[stats_filt['Item']==skill, 'agency_count_2022'].iloc[0]
        median_salary = stats_filt.loc[stats_filt['Item']==skill, 'median_salary_2022'].iloc[0]

        timeseries_filt = timeseries[timeseries['Item']==skill]

    
        col9, col10 = st.columns(2)

        with col9:
            st.title(keywords[0])
            st.write("Tableau is a business intelligence software emphasizing a drag-and-drop approach to developing visualizations built on data stored in analytics databases, transactional systems, and static datasets.")
            st.write("[Wikipedia](https://en.wikipedia.org/wiki/Tableau_Software)")

        with col10:
            #big chart
            big_chart = alt.Chart(timeseries_filt).mark_area(
                line={'color':'#4287f5'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color='white', offset=0),
                        alt.GradientStop(color='#4287f5', offset=1)],
                    x1=1,
                    x2=1,
                    y1=1,
                    y2=0
                )
            ).encode(
                alt.X('PostedData_Formatted:T'),
                alt.Y('count_jobs_2022:Q')
            )
            st.altair_chart(big_chart, use_container_width=True)


        st.subheader("**Summary Stats (Calendar Year 2022)**")
        st.write("###")

        col11, col12, col13 = st.columns(3)

        with col11:
            st.metric("Number of Jobs", job_count)

        with col12: 
            st.metric("Number of Agencies Hiring", agency_count)

        with col13:
            st.metric("Median Posted Salary", "$" + str(median_salary))


        st.write("###")
        st.subheader("Open Tableau Roles")


        host = 'data.usajobs.gov'
        userAgent = 'mtitsworth@icloud.com'
        authKey = 'i7187cutNY9D8fV4scNjYHo4rNVeIXsSCDENGVmJKQY='

        base_url = 'https://data.usajobs.gov/api/search?Keyword=PowerBI&ResultsPerPage=500'

        page_response = requests.get(
            base_url,
            headers={
                "Host": host,
                "User-Agent": userAgent,
                "Authorization-Key": authKey
            })


        json_page_data = page_response.json()

        raw_page_df = pd.json_normalize(json_page_data['SearchResult']['SearchResultItems'],max_level=1)
        random = raw_page_df.sample(n=3)

        

        col14, col15, col16 = st.columns(3)

        with col14:
            i = 0
            card_component(
            title=random['MatchedObjectDescriptor.PositionTitle'].iloc[i],
            context="Posted on 9/12/2022",
            highlight_start = 0,
            highlight_end = 0,
            score = random['MatchedObjectDescriptor.DepartmentName'].iloc[i],
            url="https://usajobs.gov"
            )
        with col15:
            i = 1
            card_component(
            title=random['MatchedObjectDescriptor.PositionTitle'].iloc[1],
            context="Posted on 9/12/2022",
            highlight_start = 0,
            highlight_end = 0,
            score = random['MatchedObjectDescriptor.DepartmentName'].iloc[i],
            url="https://usajobs.gov"
            )
        with col16:
            i = 2
            card_component(
            title=random['MatchedObjectDescriptor.PositionTitle'].iloc[i],
            context="Posted on 9/12/2022",
            highlight_start = 0,
            highlight_end = 0,
            score = random['MatchedObjectDescriptor.DepartmentName'].iloc[i],
            url="https://usajobs.gov"
            )
        st.stop()


    else: 
        findcol1, findcol2 = st.columns(2)

        with findcol1:
            st.image("https://i.giphy.com/media/26n6WywJyh39n1pBu/giphy.webp")
        with findcol2: 
            st.markdown("<h1 style='text-align: left;'><span style='font-weight: bold; color: #4287f5;'>Oops!</span></h1>", unsafe_allow_html=True)
            st.header("We couldn't find your skill!")
            st.write("We couldn't find your skill! Use the button below to submit a request for a new skill!")
            url = 'https://docs.google.com/forms/d/e/1FAIpQLSfjWkwsOZr5B1a1YSTW9Z-XW676Sd6uiKpXDSxYYAoJM9EpHg/viewform'

            st.markdown(f'''
            <a href={url}><button style="background-color:c5dafa;">Submit Skill!</button></a>
            ''',
            unsafe_allow_html=True)

