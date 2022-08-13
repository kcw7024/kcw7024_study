from cgitb import reset
import numpy as np
from sklearn.datasets import load_diabetes, load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from xgboost import XGBClassifier, XGBRegressor
import time
from sklearn.feature_selection import SelectFromModel


#1. 데이터
datasets = load_iris()
x = datasets.data
y = datasets.target
print(x.shape, y.shape) #(442, 10) (442,)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, shuffle=True, random_state=123, train_size=0.8
    )

scaler = MinMaxScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

#2. 모델 

model = XGBClassifier(random_state=123, 
                      n_estimators=100,
                      learning_rate=0.1,
                      max_depth=3, #max_depth : 얕게잡을수록 좋다 너무 깊게잡을수록 과적합 우려 #None = 무한대
                      gamma=1, )

#model = GridSearchCV(xgb, parameters, cv=kfold, n_jobs=8)

model.fit(
          x_train, y_train, early_stopping_rounds=200, 
          eval_set=[(x_train, y_train), (x_test, y_test)], # < [(훈련하고),(검증한다)]
          eval_metric = 'mlogloss',
          )

results = model.score(x_test, y_test)
print("최종 스코어 : ", results)

from sklearn.metrics import accuracy_score, r2_score
y_predict = model.predict(x_test)
acc= accuracy_score(y_test, y_predict)
print("진짜 최종 test 점수 : ", acc)

print(model.feature_importances_)

# [0.03986917 0.04455113 0.25548902 0.07593288 0.04910125 0.04870857
#  0.06075545 0.05339111 0.30488744 0.06731401]

thresholds = model.feature_importances_
print("="*80)
for thresh in thresholds : 
    selection = SelectFromModel(model, threshold=thresh, prefit=True)
    # SelectFromModel :: 크거나 같은 컬럼을 다 뽑아준다
    select_x_train = selection.transform(x_train) 
    select_x_test = selection.transform(x_test) 
    print(select_x_train.shape, select_x_test.shape)

    selection_model = XGBClassifier(n_jobs=-1,
                                  random_state=123, 
                                  n_estimators=100,
                                  learning_rate=0.1,
                                  max_depth=3, #max_depth : 얕게잡을수록 좋다 너무 깊게잡을수록 과적합 우려 #None = 무한대
                                  gamma=1,  
                                  )
    
    selection_model.fit(select_x_train, y_train)
    y_predict = selection_model.predict(select_x_test)
    score = r2_score(y_test, y_predict)
    print("Thresh=%.3f, n=%d, R2: %.2f%%"
          %(thresh, select_x_train.shape[1],score*100))


'''

최종 스코어 :  0.9666666666666667
진짜 최종 test 점수 :  0.9666666666666667
[0.07726122 0.06581087 0.5901149  0.26681304]
================================================================================
(120, 3) (30, 3)
Thresh=0.077, n=3, R2: 95.81%
(120, 4) (30, 4)
Thresh=0.066, n=4, R2: 95.81%
(120, 1) (30, 1)
Thresh=0.590, n=1, R2: 91.62%
(120, 2) (30, 2)
Thresh=0.267, n=2, R2: 95.81%

'''   
    
    