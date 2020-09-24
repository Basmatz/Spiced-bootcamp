from sklearn.ensemble import RandomForestClassifier

def train_model(X, y):
    m = RandomForestClassifier()

    m.fit(X,y)
    return m