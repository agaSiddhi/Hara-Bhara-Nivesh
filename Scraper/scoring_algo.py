import pandas as pd
from datetime import datetime

def normalize_score(score_series):
    max_value = score_series.max()
    min_value = score_series.min()
    normalized_score = ((score_series - min_value) / (max_value - min_value)) * 10
    return normalized_score

def process_and_save_data(article_data_filename='Article_data.csv', esg_ratings_filename='sustainalytics_data.csv', output_filename='final_data.csv'):

    columns = ["Company Name", "Environment", "Social", "Governance", "ESG", "Year"]

    df = pd.DataFrame(columns=columns)

    article_data = pd.read_csv(article_data_filename)
    esg_ratings = pd.read_csv(esg_ratings_filename)

    article_data['Normalized_Score'] = (article_data['Score'] + article_data['Score_blob']) / 2

    article_data['Normalized_Score'] = normalize_score(article_data['Normalized_Score'])

    for i in range(len(article_data)):
        company_name = article_data.loc[i, 'Company']
        category = article_data.loc[i, 'Category']
        score = article_data.loc[i, 'Normalized_Score']
        year = datetime.strptime(article_data.loc[i, 'Datetime'], '%Y-%m-%d %H:%M:%S%z').year
        
        if category == 'Environment':
            if company_name in df['Company Name'].values:
                df.loc[df['Company Name'] == company_name, 'Environment'] = score
            else:
                new_row = {"Company Name": company_name, "Environment": score, "Social": 0, "Governance": 0, "ESG": 0, "Year": year}
                df = df.append(new_row, ignore_index=True)
        elif category == 'Social':
            if company_name in df['Company Name'].values:
                df.loc[df['Company Name'] == company_name, 'Social'] = score
            else:
                new_row = {"Company Name": company_name, "Environment": 0, "Social": score, "Governance": 0, "ESG": 0, "Year": year}
                df = df.append(new_row, ignore_index=True)
        elif category == 'Governance':
            if company_name in df['Company Name'].values:
                df.loc[df['Company Name'] == company_name, 'Governance'] = score
            else:
                new_row = {"Company Name": company_name, "Environment": 0, "Social": 0, "Governance": score, "ESG": 0, "Year": year}
                df = df.append(new_row, ignore_index=True)

    esg_ratings['Normalized_Score'] = normalize_score(esg_ratings['Score'])

    for i in range(len(esg_ratings)):
        company_name = esg_ratings.loc[i, 'Company']
        if company_name in df['Company Name'].values:
            df.loc[df['Company Name'] == company_name, 'ESG'] = esg_ratings.loc[i, 'Normalized_Score']
        else:
            year = datetime.now().year
            new_row = {"Company Name": company_name, "Environment": 0, "Social": 0, "Governance": 0, "ESG": esg_ratings.loc[i, 'Normalized_Score'], "Year": year}
            df = df.append(new_row, ignore_index=True)

    filtered_df = df[(df['ESG'] != 0) & (df['Environment'] != 0) & (df['Social'] != 0) & (df['Governance'] != 0)]

    filtered_df['Final_ESG'] = (filtered_df['Environment'] + filtered_df['Social'] + filtered_df['Governance']) * 0.5 + filtered_df['ESG'] * 0.5

    filtered_df['Final_ESG'] = normalize_score(filtered_df['Final_ESG'])

    filtered_df.to_csv(output_filename, index=False)

    return filtered_df

