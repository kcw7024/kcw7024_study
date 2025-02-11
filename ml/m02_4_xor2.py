import numpy as np
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score

# 1. 데이터
x_data = [[0,0],[0,1][1,0],[1,1]]
y_data = [0,1,1,0] # xor: 같으면 0 다르면 1

# 2. 모델
# model = LinearSVC()
# model = Perceptron()
model = SVC() # MLP 멀티 레이어 퍼셉트론 - xor 문제를 차원을 접는 것으로 해결함, 다층 퍼셉트론으로

# 3. 훈련
model.fit(x_data, y_data)

# 4. 평가, 예측
y_pred = model.predict(x_data)
print(x_data, '의 예측결과: ', y_pred)

result = model.score(x_data, y_data)
print('model.score: ', result)

acc = accuracy_score(y_data, y_pred)
print('accuracy_score: ', acc)