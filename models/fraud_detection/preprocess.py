import pandas as pd

def preprocess_data(csv_path: str):
    df = pd.read_csv(csv_path)

    # Extract hour from timestamp
    df['Hour'] = pd.to_datetime(df['Timestamp'], format="%d-%m-%Y %H:%M").dt.hour

    # Encode categorical features
    df['SenderUPI'] = df['Sender UPI ID'].astype('category').cat.codes
    df['ReceiverUPI'] = df['Receiver UPI ID'].astype('category').cat.codes
    df['StateCode'] = df['State'].astype('category').cat.codes
    df['CityCode'] = df['City'].astype('category').cat.codes

    # Features & Labels
    X = df[['Amount','Hour','SenderUPI','ReceiverUPI','StateCode','CityCode']]
    
    # Rule-based suspicion (for labeling training set)
    df['Label'] = df.apply(lambda x: suspicious_rule(x), axis=1)
    y = df['Label']

    return X, y, df

def suspicious_rule(row):
    """Basic rules for suspicious detection"""
    # Unusual high amount
    if row['Amount'] > 50000:
        return 1
    # Odd hour (midnight transactions)
    if row['Hour'] >= 23 or row['Hour'] <= 5:
        return 1
    # Same sender -> many receivers (mule accounts detection)
    # Simplified rule: if SenderUPI or ReceiverUPI are very rare
    return 0
