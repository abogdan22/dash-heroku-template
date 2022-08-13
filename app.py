import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



# For this lab, we will be working with the 2019 General Social Survey one last time.

# In[2]:


gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                             encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE','DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])


# Here is code that cleans the data and gets it ready to be used for data visualizations:

# In[3]:


mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')


# The `gss_clean` dataframe now contains the following features:
# 
# * `id` - a numeric unique ID for each person who responded to the survey
# * `weight` - survey sample weights
# * `sex` - male or female
# * `education` - years of formal education
# * `region` - region of the country where the respondent lives
# * `age` - age
# * `income` - the respondent's personal annual income
# * `job_prestige` - the respondent's occupational prestige score, as measured by the GSS using the methodology described above
# * `mother_job_prestige` - the respondent's mother's occupational prestige score, as measured by the GSS using the methodology described above
# * `father_job_prestige` -the respondent's father's occupational prestige score, as measured by the GSS using the methodology described above
# * `socioeconomic_index` - an index measuring the respondent's socioeconomic status
# * `satjob` - responses to "On the whole, how satisfied are you with the work you do?"
# * `relationship` - agree or disagree with: "A working mother can establish just as warm and secure a relationship with her children as a mother who does not work."
# * `male_breadwinner` - agree or disagree with: "It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family."
# * `men_bettersuited` - agree or disagree with: "Most men are better suited emotionally for politics than are most women."
# * `child_suffer` - agree or disagree with: "A preschool child is likely to suffer if his or her mother works."
# * `men_overwork` - agree or disagree with: "Family life often suffers because men concentrate too much on their work."


markdown_text = '''
According to the [Pew Research Center](https://www.pewresearch.org/fact-tank/2021/05/25/gender-pay-gap-facts/), the United States has a gender pay gap where male counterparts tend to earn more then females for the same positions. This pay gap has remained steady for the past 15 years where, in 2020, women earned 84% of what men earned for both full- and part-time positions. Measurable factors that have explained these pay gaps include education, occupational segregation, and work experience. Other variables that are difficult to measure include gender discrimination, career disruptions such as motherhood, and greater caregiving responsiblities at home. Many Americans believe equal pay is necessary for gender equality and as such is a prominent issue in the United States.

Since 1972, the [General Social Survey] (GSS) (https://gss.norc.org/About-The-GSS) has collected and studied data on American society to monitor and explain trends in behaviors, attidues, and opinions. Topics studied include but are not limited to civil liberties, crime/violence, national spending, mental health, morality, and social mobility. GSS considers itself the the single best source for sociological and attitudinal trend data for the United States studying society in general, the roles played by subgroups, and compares trends in the US to other countries. This dashboard utilizes data from the 2019 General Social Survey. 
'''

# Generate a table that shows the mean income, occupational prestige, socioeconomic index, and years of education for men and for women. Use a function from a `plotly` module to display a web-enabled version of this table. This table is for presentation purposes, so round every column to two decimal places and use more presentable column names. [3 points]

gender_display = gss_clean.groupby('sex').agg({'income':'mean',
                             'job_prestige':'mean',
                             'socioeconomic_index':'mean',
                             'education':'mean'},axis = 1).reset_index()
gender_display = round(gender_display, 2)
gender_display = gender_display.rename({'sex':'Sex',
                                 'income':'Average Income',
                                 'job_prestige':'Average Occupational Prestige',
                                 'socioeconomic_index':'Average Socioeconomic Status',
                                 'education':'Average Years of Education'}, axis = 1)
#gender_display

gender_table = ff.create_table(gender_display)
#gender_table.show()

# Create an interactive barplot that shows the number of men and women who respond with each level of agreement to `male_breadwinner`. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]
breadwinner = gss_clean.groupby(['sex','male_breadwinner']).size().reset_index()
breadwinner = breadwinner.rename({0:'Count'}, axis = 1)
#breadwinner

#male breadwinner opinion question results by answer and sex
fig = px.bar(breadwinner, x = 'male_breadwinner', y = 'Count', color = 'sex',
             labels = {'male_breadwinner':'Breadwinner Opinion','sex':'Sex'},
            barmode = 'group')
#fig.show()

# Create an interactive scatterplot with `job_prestige` on the x-axis and `income` on the y-axis. Color code the points by `sex` and make sure that the figure includes a legend for these colors. Also include two best-fit lines, one for men and one for women. Finally, include hover data that shows us the values of `education` and `socioeconomic_index` for any point the mouse hovers over. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]
#income against job prestige by sex
fig2 = px.scatter(gss_clean, x = 'job_prestige', y = 'income', color = 'sex',
                  trendline = 'ols',
                 labels = {'job_prestige':'Occupational Prestige', 'income':'Income', 
                           'sex':'Sex', 'socioeconomic_index':'Socioeconomic Index',
                          'education':'Education'},
                 hover_data = ['education','socioeconomic_index'],
                 height = 700, width = 1000)
#fig2.show()



# Create two interactive box plots: one that shows the distribution of `income` for men and for women, and one that shows the distribution of `job_prestige` for men and for women. Write presentable labels for the axis that contains `income` or `job_prestige` and remove the label for `sex`. Also, turn off the legend. Don't bother with titles because we will be using subtitles on the dashboard for these graphics. [3 points]
#income distribution by sex
fig3 = px.box(gss_clean, x = 'income', y = 'sex', color = 'sex',
              labels = {'income':'Income','sex':''})
fig3.update_layout(showlegend = False)
#fig3.show()


#job prestige distribution by sex
fig4 = px.box(gss_clean, x = 'job_prestige', y = 'sex', color = 'sex',
              labels = {'job_prestige':'Occupational Prestige','sex':''})
fig4.update_layout(showlegend = False)
#fig4.show()

#cerate facetgrid

#Create a new dataframe that contains only income, sex, and job_prestige
gss_sub = gss_clean[['income','sex','job_prestige']]

#Then create a new feature in this dataframe that breaks job_prestige into six categories with equally sized ranges.
gss_sub['job_prestige_equal'] = pd.cut(gss_sub['job_prestige'], 6)


#Finally, drop all rows with any missing values in this dataframe.
gss_sub = gss_sub.dropna()



# Then create a facet grid with three rows and two columns in which each cell contains an interactive box plot comparing the income distributions of men and women for each of these new categories.


fig5 = px.box(gss_sub, x = 'income', y = 'sex', color = 'sex',
              facet_col = 'job_prestige_equal', facet_col_wrap = 2,
              labels = {'sex':'', 'income':'Income'},
              color_discrete_map = {'male':'blue', 'female':'red'},
              height = 700, width = 1000
             )
#fig5.show()

# Create a dashboard

#app = JupyterDash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Exploring the 2019 General Social Survey: United States Gender Wage Gap"),
        
        dcc.Markdown(children = markdown_text),
        
        html.H2("Average Gender Differences"),
        
        dcc.Graph(figure=gender_table),
        
        html.H2('Opinion of "Males as Breadwinners" by Sex'),
        
        dcc.Graph(figure=fig),
        
        html.H2("Income vs. Job Prestige by Sex"),
        
        dcc.Graph(figure=fig2),
        
        html.Div([
            
            html.H2("Income Distribution by Sex"),
            
            dcc.Graph(figure=fig3)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H2("Occupational Prestige Disribution by Sex"),
            
            dcc.Graph(figure=fig4)
            
        ], style = {'width':'48%', 'float':'right'}),
        
        html.H2("Income Distribution by Sex and Job Prestige"),
        
        dcc.Graph(figure=fig5)
        
        
        
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8058)
