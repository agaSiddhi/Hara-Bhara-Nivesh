import pandas as pd
from datetime import datetime
import yaml

def assign_weights(column):
    if column == -1:
        return 0
    else:
        return 1

def update_final_esg_score(df):
    for i in range(len(df)):
        environment = df.loc[i,'Environment']
        social = df.loc[i,'Social']
        governance = df.loc[i,'Governance']
        esg_ratings = df.loc[i,'ESG_ratings']
        count = 0
        w1 = assign_weights(environment)
        if w1 == 1: count+=1
        w2 = assign_weights(social)
        if w2 == 1: count+=1
        w3 = assign_weights(governance)
        if w3 == 1: count+=1
        w4 = assign_weights(esg_ratings)
        if w4 == 1: count+=1
        final_esg_score = w1 * environment + w2 * social + w3 * governance + w4 * esg_ratings
        df.loc[i, 'Final_ESG_Score'] = final_esg_score/count
    return df

def update_historical_esg_score(df, last_occurrence):
    for index, row in df.iterrows():
        company = row['Company Name']
        esg_score = row['Final_ESG_Score']
        if company not in last_occurrence:
            last_occurrence[company] = [esg_score, 1]
            final_esg_score = esg_score
        else:
            prev_esg_score, count = last_occurrence[company]
            last_occurrence[company] = [prev_esg_score + esg_score, count + 1]
            final_esg_score = (prev_esg_score + esg_score) / (count + 1)
        df.at[index, 'Historical_esg_score'] = final_esg_score
    return df, last_occurrence

def push_data_to_csv(df, csv_file):
    df.to_csv(csv_file, index=False)

def update_yaml_file(last_occurrence, yaml_file):
    with open(yaml_file, 'w') as file:
        yaml.dump(last_occurrence, file)

def scoring_algorithm(articles_file = 'Scraper/Article_data.csv' , esg_ratings_file = 'Scraper/sustainalytics_data.csv' , yaml_file = 'Scraper/dictionary.yaml', output_csv_file = 'Scraper/final_data.csv'):
    articles = pd.read_csv(articles_file)
    esg_ratings = pd.read_csv(esg_ratings_file)

    articles['Final_Score'] = (articles['Score'] + 1) / 2 * 100
    articles['Score_blob'] = (articles['Score_blob'] + 1) / 2 * 100
    articles['Final_Score'] = (articles['Score'] * 0.5) + (articles['Score_blob'] * 0.5)

    df = pd.DataFrame(columns=["Company Name","Date", "Environment", "Social", "Governance", "ESG_ratings","Final_ESG_Score","Historical_esg_score"])

    for i in range(len(articles)):
        company_name = articles.loc[i, 'Company']
        category = articles.loc[i, 'Category']
        score = articles.loc[i, 'Final_Score']
        date = articles.loc[i, 'Datetime'][:10]

        if category in ['Environment', 'Social', 'Governance']:
            if (company_name in df['Company Name'].values) and (df.loc[(df['Company Name'] == company_name) & (df['Date'] == date)].shape[0] > 0):
                df.loc[(df['Company Name'] == company_name) & (df['Date'] == date), category] = score
            else:
                new_row = {"Company Name": company_name, "Date": date, category: score}
                df = df.append(new_row, ignore_index=True)

    for i in range(len(esg_ratings)):
        company_name = esg_ratings.loc[i, 'Company']
        if company_name in df['Company Name'].values:
            df.loc[df['Company Name'] == company_name, 'ESG_ratings'] = esg_ratings.loc[i, 'Score']
        else:
            date = datetime.now().date().strftime('%Y-%m-%d')
            new_row = {"Company Name": company_name, "ESG_ratings": esg_ratings.loc[i, 'Score'], "Date": str(date)}
            df = df.append(new_row, ignore_index=True)

    df.fillna(-1, inplace=True)

    df = update_final_esg_score(df)

    df = df.sort_values(by='Date', ascending=True)

    yaml_data = {}
    try:
        with open(yaml_file, 'r') as file:
            yaml_data = yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        pass

    df, updated_yaml_data = update_historical_esg_score(df, yaml_data)

    update_yaml_file(updated_yaml_data, yaml_file)

    push_data_to_csv(df, output_csv_file)

