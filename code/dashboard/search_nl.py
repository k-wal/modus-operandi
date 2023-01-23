import pandas as pd
import numpy as np
from datetime import datetime
import re

def search_drug_pattern(search_word):
    '''creates regex search pattern from a search word 
    for example 3mmc search will look for 
    3mmc 3-mmc 3 mmc and 3MMC 3 MMC 3-MMC
    '''
    search_word = search_word.strip() # remove leadning and trailing white spaces
    pattern = r'\s+' # one white space or more
    search_word=re.sub(pattern,"-", search_word)    
    pattern = r'([0-9]+)' # one dash or more
    search_word = re.sub(pattern, r"\1-", search_word)
    pattern = r'-+' # one dash or more
    search_word = re.sub(pattern,"-", search_word)
 
    pattern = search_word.replace("-","\s*\-*")
    pattern = '\\b'+pattern+'\\b'
    pattern = re.compile(pattern, flags=re.IGNORECASE)  
    return pattern

# combine three sources of drugsforum.nl and return df
def get_nl_df():
    df1 = pd.read_csv('nl_corpus/drugs_generaldrugsforumnl_threads.csv',
                     lineterminator='\n')
    df2 = pd.read_csv('nl_corpus/research_chemicalsdrugsforumnl_threads.csv')
    df3 = pd.read_csv('nl_corpus/trip_reportsdrugsforumnl_threads.csv',
                     lineterminator='\n')
    return pd.concat([df1, df2, df3], axis=0)    


def fill_missing_months(drug_df, beg_year, end_year):
#    beg_year, end_year = 2008, 2022
    beg_month, end_month = 1, 12
    for year in range(beg_year, end_year+1):
        for month in range(beg_month, end_month+1):
            if month<10:
                month_str = '0'+str(month)
            else:
                month_str = str(month)
            month_year = str(year) + '-' + month_str
            if month_year in drug_df['month-year'].unique():
                #print(month_year)
                continue
            new_row = pd.DataFrame({
                'month' : [month_str],
                'year' : [str(year)],
                'month-year' : [month_year],
                'comments' : [0],
                'views' : [0],
                'url' : [''],
                'title' : ['something'],
                'username' : ['something]'],
                'user_url' : [''],
                'thread_id' : [0],
                'forum' : [''],
            }, index = [len(drug_df)])
            drug_df = drug_df.append(new_row)
    return drug_df

def search_drug(drug, beg_year=2012, end_year=2022):
    df = get_nl_df()
    drug_df = pd.DataFrame(columns=df.columns)
    df = df[df['date']!='something']
    df['title'] = df['title'].str.lower()
    df['content'] = df['content'].str.lower()

    drug_name = drug.lower()
    drug_pattern = search_drug_pattern(drug_name)
    t_df = df[df['title'].str.contains(pat=drug_pattern)]
    c_df = df[df['title'].str.contains(pat=drug_pattern)]
    tc_df = pd.concat([t_df,c_df]).drop_duplicates().reset_index(drop=True)
    drug_df = pd.concat([drug_df, tc_df]).drop_duplicates().reset_index(drop=True)

    drug_df['month'] = drug_df['date'].apply(lambda x: int(x.split('-')[1]))
    drug_df['year'] = drug_df['date'].apply(lambda x: int(x.split('-')[0]))
    drug_df['month-year'] = drug_df['date'].apply(lambda x: x.split('-')[0] + '-' + x.split('-')[1])
    
    # filter by year given through dashboard
    drug_df = drug_df[(drug_df['year']>=beg_year) & (drug_df['year']<=end_year)]
    
    drug_df = fill_missing_months(drug_df, beg_year, end_year)
    
    data=drug_df.sort_values(by=['month-year'], ascending=True)

    data['views'] = data['views'].astype('int')
    data['comments'] = data['comments'].astype('int')

    data['month-year'] = data['month-year'].apply(lambda x: datetime.strptime(x, "%Y-%m"))
    data['freq'] = data['views'].map(lambda x: 0 if x == 0 else 1)
    
    data = data.drop(['thread_id','forum','title','content','url','username','user_id','user_url','date']
              ,axis=1)
    
    agg_data = pd.DataFrame()
    agg_data['views'] = data.groupby(['month-year'])['views'].sum().reset_index()['views']
    agg_data['month-year'] = data.groupby(['month-year'])['freq'].sum().reset_index()['month-year']
    data = agg_data
    
    data['moving-avg-views'] = data['views'].rolling(5).mean()
    data['moving-avg-views'] = data['moving-avg-views'].fillna(0)

    return data    


data = search_drug(drug, beg_year, end_year)