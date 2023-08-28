#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df = pd.read_csv(r'E:/navttc_files/Salary_Survey_2021.csv', encoding='latin-1')


# In[3]:


pd.reset_option('display.max_rows')


# ## renaming columns

# In[4]:


column_name_changes = {
    "If your job title needs additional context, please clarify here:": "additional_job_title",
    "What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)": "annual_salary",
    "What industry do you work in?": "industry",
    "How old are you?": "age",
    "What is your gender?": "gender",
    "How much additional monetary compensation do you get, if any (for example, bonuses or overtime in an average year)? Please only include monetary compensation here, not the value of benefits.": "add_mon_comp",
    "Please indicate the currency": "currency",
    "If your income needs additional context, please provide it here:": "add_income_cont",
    "What country do you work in?": "work_country",
    "If you're in the U.S., what state do you work in?": "US state",
    "What city do you work in?": "work_city",
    "How many years of professional work experience do you have overall?": "total experience",
    "How many years of professional work experience do you have in your field?": "field experience",
    "What is your highest level of education completed?": "highest education",
    "What is your race? (Choose all that apply.)": "race",
    "Job title": "job title",
    "If 'Other,' please indicate the currency here:	": "other_currency",
}

df.rename(columns=column_name_changes, inplace=True)
df


# # Pandas Profiling

# In[5]:


# import pandas as pd
# from pandas_profiling import ProfileReport

# # Assuming you already have your DataFrame 'df'

# # Create a Pandas Profiling report
# profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)

# # Generate the report as an HTML file
# profile.to_file("output_report.html")
# profile


# ### removing un-necessary columns

# In[6]:


df.drop(['Timestamp','add_income_cont','US state','work_city','If "Other," please indicate the currency here: ','additional_job_title','add_mon_comp'], axis=1, inplace=True)


# In[7]:


df.drop(columns=['Unnamed: 18','Unnamed: 19','Unnamed: 20','Unnamed: 21','Unnamed: 22','Unnamed: 23'], axis =1, inplace= True)


# In[8]:


df.dropna(subset = ['industry','job title','highest education','gender','race'], inplace = True)


# In[9]:


df['gender'].replace('Prefer not to answer','Other or prefer not to answer',inplace=True)


# In[10]:


df['gender'].replace(['Woman','Man','Non-binary','Other or prefer not to answer'],value=[0,1,2,3],inplace = True)


# In[11]:


race_counts = df['race'].value_counts() #counting the number of people in each race
valid_races = race_counts[race_counts >= 5].index.tolist()
df = df[df['race'].isin(valid_races)] #filtering out races with less than 5 people


# In[12]:


df['race'].value_counts()


# In[13]:


df['race'].replace(['Black or African American, White','Black or African American',
                   'Black or African American, Hispanic, Latino, or Spanish origin',
                   'Black or African American, Hispanic, Latino, or Spanish origin, White',
                   'Black or African American, Native American or Alaska Native, White',
                   'Black or African American, Middle Eastern or Northern African, White',
                   'Black or African American, Hispanic, Latino, oHispanic, Latino, or Spanish originHispanic, Latino, or Spanish originr Spanish origin, Native American or Alaska Native, White',
                   'Black or African American, Another option not listed here or prefer not to answer'],value='black', inplace = True)


# In[14]:


df['race'].replace(['Hispanic, Latino, or Spanish origin','Hispanic, Latino, or Spanish origin, White ',
                   'Hispanic, Latino, or Spanish origin, White',
                   'Hispanic, Latino, or Spanish origin, Middle Eastern or Northern African, White',
                   'Hispanic, Latino, or Spanish origin, Another option not listed here or prefer not to answer',
                   'Hispanic, Latino, or Spanish origin, Native American or Alaska Native, White',
                   'Hispanic, Latino, or Spanish origin, Native American or Alaska Native'], value = 'hispanic', inplace = True)


# In[15]:


df['race'].replace(['Another option not listed here or prefer not to answer'], value = 'others', inplace = True)


# In[16]:


df['race'].replace(['Asian or Asian American','Asian or Asian American, Another option not listed here or prefer not to answer',
                   'Middle Eastern or Northern African, White','Asian or Asian American, White','Asian or Asian American, White, Another option not listed here or prefer not to answer'
                   'Middle Eastern or Northern African' ,'Native American or Alaska Native, White',
                   'Asian or Asian American, Hispanic, Latino, or Spanish origin',
                   'Asian or Asian American, Hispanic, Latino, or Spanish origin, White',
                   'Asian or Asian American, Black or African American',
                   'Asian or Asian American, Black or African American ',
                   'Asian or Asian American, Middle Eastern or Northern African',
                   'Asian or Asian American, Black or African American, White',
                   'Asian or Asian American, White, Another option not listed here or prefer not to answer',
                   'Asian or Asian American, Native American or Alaska Native, White'], value = 'asian', inplace = True)


# In[17]:


df['race'].replace(['White, Another option not listed here or prefer not to answer'], value = 'White', inplace = True)


# In[18]:


df['race'].replace(['White','asian','hispanic','black','others','Middle Eastern or Northern African','Native American or Alaska Native'],value=[1,2,3,4,5,6,7],inplace = True)


# In[19]:


df['highest education'].replace(['College degree','Master\'s degree','Some college','PhD','Professional degree (MD, JD, etc.)','High School'], value = [1,2,3,4,5,6], inplace = True) #replacing values in 'Highest education' column


# In[20]:


def calculate_experience(experience_range):
    if '-' in experience_range:
        range_parts = experience_range.split('-')
        lower = int(range_parts[0])
        upper = int(range_parts[-1].split()[0])  # Remove any additional text
        return (lower + upper) / 2
    elif 'year' in experience_range:
        if 'less' in experience_range:
            return 0.5  # Assuming 1 year or less is considered as 0.5 years
        elif 'more' in experience_range:
            return 41  # Assuming 41 years or more is considered as 41 years
        else:
            return 1  # For "1 year"
    else:
        return None


# In[21]:


df['field experience'] = df['field experience'].apply(calculate_experience)


# In[22]:


df['field experience'] = df['field experience'].astype(int)


# In[23]:


df['total experience'] = df['total experience'].apply(calculate_experience)


# In[24]:


df['total experience'] = df['total experience'].astype(int)


# In[25]:


df = df.drop_duplicates() #removing duplicates


# In[26]:


country_replacements = {
    'US': 'United States',
    'USA': 'United States',
    'United States ': 'United States',
    'U.S.': 'United States',
    'UK': 'United Kingdom',
    'Usa': 'United States',
    'U.S': 'United States',
    'U.S.A': 'United States',
    'U.S.A.': 'United States',
    'United States of America': 'United States',
    'USA ': 'United States',
    'United states': 'United States',
    'usa': 'United States',
    'United Sates': 'United States',
    'united states': 'United States',
    'United States of America ': 'United States',
    'United Sates ': 'United States',
    'United State': 'United States',
    'U.S. ': 'United States',
    'America': 'United States',
    'Us': 'United States',
    'U.S. ': 'United States',
    'us': 'United States',
    'US ': 'United States',
    'Unites States': 'United States',
    'UnitedStates': 'United States',
    'United Stated': 'United States'
}

df['work_country'].replace(country_replacements, inplace=True)
df['work_country'].value_counts()


# In[27]:


#in work_country column replace all values indicating United Kingdom to United Kingdom
df['work_country'].replace('United Kingdom', 'United Kingdom', inplace = True)
df['work_country'].replace('United Kingdom ', 'United Kingdom', inplace = True)
df['work_country'].replace('UK', 'United Kingdom', inplace = True)
df['work_country'].replace('England', 'United Kingdom', inplace = True)
df['work_country'].replace('Scotland', 'United Kingdom', inplace = True)
df['work_country'].replace('Wales', 'United Kingdom', inplace = True)
df['work_country'].replace('Northern Ireland', 'United Kingdom', inplace = True)
df['work_country'].replace('Ireland', 'United Kingdom', inplace = True)
df['work_country'].replace('Ireland ', 'United Kingdom', inplace = True)
df['work_country'].replace('Uk', 'United Kingdom', inplace = True)
df['work_country'].replace('United kingdom ', 'United Kingdom', inplace = True)
df['work_country'].replace('England ', 'United Kingdom', inplace = True)
df['work_country'].replace('United kingdom', 'United Kingdom', inplace = True)
df['work_country'].replace('united kingdom', 'United Kingdom', inplace = True)
df['work_country'].replace('united kingdom ', 'United Kingdom', inplace = True)
df['work_country'].replace('UK', 'United Kingdom', inplace = True)
df['work_country'].replace('UK ', 'United Kingdom', inplace = True)


# In[28]:


#in work_country column replace all values indicating the country Canada to Canada
df['work_country'].replace('Canada', 'Canada', inplace = True)
df['work_country'].replace('Canada ', 'Canada', inplace = True)
df['work_country'].replace('canada', 'Canada', inplace = True)
df['work_country'].replace('canada ', 'Canada', inplace = True)
df['work_country'].replace('CANADA', 'Canada', inplace = True)



# In[29]:


#in work_country column replace all values indicating the country Australia to Australia
df['work_country'].replace('Australia', 'Australia', inplace = True)
df['work_country'].replace('Australia ', 'Australia', inplace = True)
df['work_country'].replace('australia', 'Australia', inplace = True)
df['work_country'].replace('australia ', 'Australia', inplace = True)
df['work_country'].replace('AUS', 'Australia', inplace = True)
df['work_country'].replace('AUS ', 'Australia', inplace = True)
df['work_country'].replace('au', 'Australia', inplace = True)
df['work_country'].replace('au ', 'Australia', inplace = True)
df['work_country'].replace('australia ', 'Australia', inplace = True)
df['work_country'].replace('AUSTRALIA', 'Australia', inplace = True)
df['work_country'].replace('AUSTRALIA ', 'Australia', inplace = True)
df['work_country'].replace('Australian ', 'Australia', inplace = True)


# In[30]:


#in work_country column replace all values indicating the country Germany to Germany
df['work_country'].replace('Germany', 'Germany', inplace = True)
df['work_country'].replace('Germany ', 'Germany', inplace = True)
df['work_country'].replace('germany', 'Germany', inplace = True)
df['work_country'].replace('germany ', 'Germany', inplace = True)
df['work_country'].replace('GERMANY', 'Germany', inplace = True)
df['work_country'].replace('GERMANY ', 'Germany', inplace = True)



# In[31]:


#in work_country column replace all values indicating the country New Zealand to New Zealand
df['work_country'].replace('New Zealand', 'New Zealand', inplace = True)
df['work_country'].replace('New Zealand ', 'New Zealand', inplace = True)
df['work_country'].replace('new zealand', 'New Zealand', inplace = True)
df['work_country'].replace('New zealand', 'New Zealand', inplace = True)
df['work_country'].replace('new zealand ', 'New Zealand', inplace = True)
df['work_country'].replace('NEW ZEALAND', 'New Zealand', inplace = True)
df['work_country'].replace('NEW ZEALAND ', 'New Zealand', inplace = True)
df['work_country'].replace('NZ', 'New Zealand', inplace = True)
df['work_country'].replace('NZ ', 'New Zealand', inplace = True)
df['work_country'].replace('nz', 'New Zealand', inplace = True)


# In[32]:


#in work_country column replace all values indicating the country France to France
df['work_country'].replace('France', 'France', inplace = True)
df['work_country'].replace('France ', 'France', inplace = True)
df['work_country'].replace('france', 'France', inplace = True)
df['work_country'].replace('france ', 'France', inplace = True)
df['work_country'].replace('FRANCE', 'France', inplace = True)


# In[33]:


#in work_country column replace all values indicating the country Netherlands to Netherland
df['work_country'].replace('Netherlands', 'Netherlands', inplace = True)
df['work_country'].replace('Netherlands ', 'Netherlands', inplace = True)
df['work_country'].replace('netherlands', 'Netherlands', inplace = True)
df['work_country'].replace('The Netherlands', 'Netherlands', inplace = True)


# In[34]:


df['work_country'].value_counts()


# In[35]:


#in work_country column replace all values indicating the country Sweden to Sweden
df['work_country'].replace('Sweden ', 'Sweden', inplace = True)


# In[36]:


value_counts = df['work_country'].value_counts()


# In[37]:


#in the work_country column drop all the values that are less than 20
countries_to_keep = value_counts[value_counts >= 20].index
df = df[df['work_country'].isin(countries_to_keep)]


# In[38]:


df['work_country'].replace(['United States','Canada','United Kingdom','Australia','New Zealand','Germany','France','Spain',
                            'Sweden','Belgium','Switzerland','Netherlands','Japan'], value = [1,2,3,4,5,6,7,8,9,10,11,12,13], inplace = True)


# In[39]:


df.info()


# In[40]:


df['currency'].value_counts()


# In[41]:


df['currency'].replace(['USD','CAD','GBP','AUD/NZD','SEK','CHF','EUR','Other','JPY'],value = [1,2,3,4,5,6,7,8,9], inplace = True)


# In[42]:


#handling age range


# In[43]:


def calculate_age(age_range):
    if '-' in age_range:
        range_parts = age_range.split('-')
        lower = int(range_parts[0])
        upper = int(range_parts[-1].split()[0])  # Remove any additional text
        return (lower + upper) / 2
    elif 'year' in age_range:
        if 'less' in age_range:
            return 0.5  # Assuming 1 year or less is considered as 0.5 years
        elif 'more' in age_range:
            return 41  # Assuming 41 years or more is considered as 41 years
        else:
            return 1  # For "1 year"
    else:
        return None


# In[44]:


df['age_filtered'] = df['age'].apply(calculate_age)


# In[45]:


df.groupby('age')['age_filtered'].value_counts()


# # label encoding on industry

# In[46]:


df['annual_salary'] = df['annual_salary'].str.replace(',', '').astype(int)


# In[47]:


df.dropna(inplace = True)


# In[48]:


#using the annual salary column predict monthly salary data type integar
df['monthly_salary'] = df['annual_salary'] / 12
df['monthly_salary'] = df['monthly_salary'].astype(int)


# In[49]:


df['monthly_salary'].value_counts()


# In[50]:


df.groupby('job title')['industry'].value_counts()


# In[51]:


job_counts = df['job title'].value_counts()

# Sort the DataFrame by the job title counts in descending order
df = df[df['job title'].isin(job_counts.index)].sort_values(by=['job title'], key=lambda x: x.map(job_counts), ascending=False)

df


# In[52]:


industry_counts = df['industry'].value_counts().sort_values(ascending=False)


from sklearn.preprocessing import OrdinalEncoder
encoder = OrdinalEncoder(categories=[industry_counts.index])


df['industry_encoded'] = encoder.fit_transform(df[['industry']]) + 1  # Adding 1 to start indexing from 1
df['industry_encoded'] = df['industry_encoded'].astype(int)
df


# In[53]:


print(df.groupby('industry_encoded')['industry'].value_counts())


# In[54]:


df.groupby('industry_encoded')['industry'].value_counts()


# In[55]:


df.groupby('industry_encoded')['industry'].value_counts(ascending = False)


# In[56]:


job_counts = df['job title'].value_counts().sort_values(ascending=False)


from sklearn.preprocessing import OrdinalEncoder
encoder = OrdinalEncoder(categories=[job_counts.index])


df['job_encoded'] = encoder.fit_transform(df[['job title']]) + 1  # Adding 1 to start indexing from 1
df['job_encoded'] = df['job_encoded'].astype(int)
df


# In[57]:


df.info()


# In[ ]:




