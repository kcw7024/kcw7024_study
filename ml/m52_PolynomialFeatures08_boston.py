from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

#1. 데이터
datasets = load_boston()
x, y = datasets.data, datasets.target
print(x.shape, y.shape) # (506, 13) (506,)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size=0.8, random_state=1234    
)

Kfold = KFold(n_splits=5, shuffle=True, random_state=1234)

#2. 모델

model = make_pipeline(StandardScaler(), 
                      LinearRegression()
                      )

model.fit(x_train, y_train)

print("기본 스코어 : ", model.score(x_test, y_test))

from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, x_train, y_train, cv=Kfold, scoring='r2')
print("기본 CV : ", scores)
print("기본 CV 나눈 값 : ", np.mean(scores))


########################################### PolynomialFeature 후

pf = PolynomialFeatures(degree=2, include_bias=False)
xp = pf.fit_transform(x)
print(xp.shape) # (506, 105)

x_train, x_test, y_train, y_test = train_test_split(
    xp, y, train_size=0.8, random_state=1234    
)

#2. 모델

model = make_pipeline(StandardScaler(), 
                      LinearRegression()
                      )

model.fit(x_train, y_train)

print("폴리 스코어 : ", model.score(x_test, y_test))

from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, x_train, y_train, cv=Kfold, scoring='r2')
print("폴리 CV : ", scores)
print("폴리 CV 나눈 값 : ", np.mean(scores))


'''

(506, 13) (506,)
기본 스코어 :  0.7665382927362877
기본 CV :  [0.71606004 0.67832011 0.65400513 0.56791147 0.7335664 ]
기본 CV 나눈 값 :  0.669972627809433

(506, 104)
폴리 스코어 :  0.8745129304823852
폴리 CV :  [0.7917776  0.8215846  0.79599441 0.81776798 0.81170102]
폴리 CV 나눈 값 :  0.807765121221582

'''