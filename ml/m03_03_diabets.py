#### 과제 2 
# activation : sigmoid, relu, linear 넣고 돌리기
# metrics 추가
# EarlyStopping 넣고
# 성능 비교
# 감상문, 느낀점 2줄이상!!!

from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC, LinearSVR
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/gulim.TTc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
from sklearn.datasets import load_diabetes
import time

#1. 데이터
datasets = load_diabetes()
x = datasets.data
y = datasets.target

x_train, x_test, y_train, y_test = train_test_split(x,y,
                                                    train_size=0.8,
                                                    random_state=72
                                                    )
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

model = RandomForestRegressor()

#3. 컴파일, 훈련
use_models = [LinearRegression, KNeighborsRegressor, DecisionTreeRegressor, RandomForestRegressor]

# model.fit(x_train, y_train)

# #4. 평가, 예측
# result = model.score(x_test, y_test)
# print('결과 acc : ', result)
# y_predict = model.predict(x_test)
# # y_predict = np.argmax(y_predict, axis= 1)
# # y_test = tf.argmax(y_test, axis= 1)
# acc= accuracy_score(y_test, y_predict)
# print('acc스코어 : ', acc) 


for model in use_models :
    model = model()
    name = str(model).strip('()')
    model.fit(x_train, y_train)
    result = model.score(x_test, y_test)
    print(name,'의 ACC : ', result)


'''
LinearRegression 의 ACC :  0.6579209558684551
KNeighborsRegressor 의 ACC :  0.5403351561734346
DecisionTreeRegressor 의 ACC :  0.07477703370600408
RandomForestRegressor 의 ACC :  0.54973565912068

'''