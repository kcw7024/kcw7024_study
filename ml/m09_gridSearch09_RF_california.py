#### 과제 2 
# activation : sigmoid, relu, linear 넣고 돌리기
# metrics 추가
# EarlyStopping 넣고
# 성능 비교
# 감상문, 느낀점 2줄이상!!!

from sklearn.model_selection import StratifiedKFold, train_test_split, KFold, cross_val_predict, cross_val_score, GridSearchCV
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/gulim.TTc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
from sklearn.datasets import fetch_california_housing
import time
from sklearn.svm import LinearSVC, LinearSVR
from sklearn.metrics import r2_score
import numpy as np

#1. 데이터
datasets = fetch_california_housing()
x = datasets.data
y = datasets.target

x_train, x_test, y_train, y_test = train_test_split(x,y,
                                                    train_size=0.8,
                                                    random_state=66
                                                    )
n_splits = 5
kfold = KFold(n_splits = n_splits, shuffle=True, random_state=66)

parameters = [
    {'n_estimators' : [100, 200], 'max_depth': [40,30,20,50], 'min_samples_leaf':[15, 30, 50, 100]}, #epochs
    {'max_depth' : [6, 8, 10, 12], 'min_samples_split':[2, 4, 5, 20], 'n_jobs' : [-1, 3]},
    {'min_samples_leaf' : [3, 5, 7, 10], 'n_estimators':[150, 300, 200], 'max_depth':[7, 8, 9, 10]},
    {'min_samples_split' : [2, 3, 5, 10]},
    {'n_jobs' : [-1, 2, 4]}    
]



'''
print(x)
print(y)
print(x.shape, y.shape) # (506, 13) (506,)
print(datasets.feature_names) #싸이킷런에만 있는 명령어
print(datasets.DESCR)
'''

#2. 모델구성
from sklearn.svm import LinearSVC, SVC
from sklearn.linear_model import Perceptron 
from sklearn.linear_model import LogisticRegression, LinearRegression 
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor 
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor 

model = GridSearchCV(RandomForestRegressor(), parameters, cv=kfold, verbose=1,
                     refit=True, n_jobs=-1)


#3. 컴파일 훈련
import time
start = time.time()
model.fit(x_train, y_train)
#Fitting 5 folds for each of 119 candidates, totalling 595 fits
end = time.time()
print("최적의 매개변수 : ", model.best_estimator_)
print("최적의 파라미터 : ", model.best_params_)
print("best_score_ : ", model.best_score_) # train에 대한 점수
print("model.score : ", model.score(x_test, y_test)) #test score라서 위와 값이 다름

#4. 평가, 예측
from sklearn.metrics import accuracy_score, r2_score

y_predict = model.predict(x_test)
print("r2 스코어 :" , r2_score(y_test, y_predict))

y_pred_best = model.best_estimator_.predict(x_test)
print("최적 튠 R2 : ", r2_score(y_test, y_pred_best))
print("걸린시간 : ", round(end-start, 2))


# 최적의 매개변수 :  RandomForestRegressor(min_samples_split=5)
# 최적의 파라미터 :  {'min_samples_split': 5}
# best_score_ :  0.797642107454815
# model.score :  0.8242507575298538
# r2 스코어 : 0.8242507575298538
# 최적 튠 R2 :  0.8242507575298538
# 걸린시간 :  542.93