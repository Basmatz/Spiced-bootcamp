#copied from course material 12.5
#https://krspiced.pythonanywhere.com/chapters/project_software_engineering/continuous_integration/continuous_integration.html
from sklearn.datasets import load_wine
import pandas as pd

d = load_wine()
print(d['DESCR'])
df = pd.DataFrame(d['data'], columns=d['feature_names'])
y = d['target']  # cultivator