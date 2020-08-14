def feature_engineer_Kelvin3(data):
    """
    prepares features for linear regression including 
    - weather variables: humidity, windspeed, atemp, weather,
    - one-hot-encoded hours, day of the week, months, years
    
    arguments
    ---------
    data: raw training data
    
    
    return
    ------
    dataframe of engineered features
    
    """
    
    data['t-1 K'] = data['Kelvin'].shift(1)
    data['t-2 K'] = data['Kelvin'].shift(2)
    data['t-3 K'] = data['Kelvin'].shift(3)

    
    X = data[['t-1 K', 't-2 K', 't-3 K']]
    
    return X.dropna()





def feature_engineer_Kelvin10(data):
    """
    prepares features for linear regression including 
    - weather variables: humidity, windspeed, atemp, weather,
    - one-hot-encoded hours, day of the week, months, years
    
    arguments
    ---------
    data: raw training data
    
    
    return
    ------
    dataframe of engineered features
    
    """
    
    data['t-1 K'] = data['Kelvin'].shift(1)
    data['t-2 K'] = data['Kelvin'].shift(2)
    data['t-3 K'] = data['Kelvin'].shift(3)
    data['t-4 K'] = data['Kelvin'].shift(4)
    data['t-5 K'] = data['Kelvin'].shift(5)
    data['t-6 K'] = data['Kelvin'].shift(6)
    data['t-7 K'] = data['Kelvin'].shift(7)
    data['t-8 K'] = data['Kelvin'].shift(8)
    data['t-9 K'] = data['Kelvin'].shift(9)
    data['t-10 K'] = data['Kelvin'].shift(10)

    
    X = data[['t-1 K', 't-2 K', 't-3 K', 't-4 K', 't-5 K', 't-6 K', 't-7 K', 't-8 K', 't-9 K', 't-10 K']]
    
    return X.dropna()





def feature_engineer_pct3(data):
    """
    prepares features for linear regression including 
    - weather variables: humidity, windspeed, atemp, weather,
    - one-hot-encoded hours, day of the week, months, years
    
    arguments
    ---------
    data: raw training data
    
    
    return
    ------
    dataframe of engineered features
    
    """
    
    df_train['t-1 pct'] = df_train['pct_stationary'].shift(1)
    df_train['t-2 pct'] = df_train['pct_stationary'].shift(2)
    df_train['t-3 pct'] = df_train['pct_stationary'].shift(3)

    
    X = data[['t-1 pct', 't-2 pct', 't-3 pct']]
    
    return X