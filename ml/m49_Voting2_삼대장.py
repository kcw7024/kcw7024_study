from tabnanny import verbose
import numpy as np
import pandas as pd

from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

#1. 데이터
datasets = load_breast_cancer()

# df = pd.DataFrame(datasets.data, columns=datasets.feature_names)
# print(df.head(7))

x_train, x_test, y_train, y_test = train_test_split(
    datasets.data, datasets.target, train_size=0.9, random_state=123,
    stratify=datasets.target
)

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

#2. 모델

xg = XGBClassifier()
lg = LGBMClassifier()
cat = CatBoostClassifier(verbose=False)

model = VotingClassifier(  
        estimators = [('XG', xg), ('LG', lg), ('CAT', cat)],
        voting = 'soft'  # hard 도 있다.
)

#3. 훈련
model.fit(x_train, y_train)

#4. 평가, 예측
y_predict = model.predict(x_test)
score = accuracy_score(y_test, y_predict)
# print("보팅 결과 : ", round(score, 4))

# 보팅 결과 :  0.9912

classifiers = [cat, xg, lg]

for model2 in classifiers :
    model2.fit(x_train, y_train)
    y_predict = model2.predict(x_test)
    score2 = accuracy_score(y_test, y_predict)
    class_name = model2.__class__.__name__
    print('{0} 정확도 : {1:.4f}'.format(class_name, score2))

print("보팅 결과 : ", round(score, 4))

'''
CatBoostClassifier 정확도 : 1.0000
XGBClassifier 정확도 : 0.9825
LGBMClassifier 정확도 : 0.9825
보팅 결과 :  1.0

'''


