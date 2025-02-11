from pickletools import optimize
import numpy as np

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from sklearn.model_selection import train_test_split


# 1. 데이터

x = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
y = np.array([1,2,4,3,5,7,9,3,8,12,13,8,14,15,9,6,17,23,21,20])

x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size=0.7, shuffle=True, random_state=66
)

print(x_train.shape, y_train.shape) #(14,) (14,)
print(x_test.shape, y_test.shape) #(6,) (6,)

# 2. 모델구성
 
model = Sequential()
model.add(Dense(5, input_dim=1)) 
model.add(Dense(2))
model.add(Dense(3))
model.add(Dense(4))
model.add(Dense(1))

# 3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam') #회귀모델 형식
model.fit(x_train, y_train, epochs=1, batch_size=1)

# 4. 평가, 예측 
loss = model.evaluate(x_test, y_test)
print('loss : ', loss)

y_predict = model.predict(x)

from sklearn.metrics import r2_score
r2 = r2_score(y, y_predict)
print('r2스코어 : ', r2)

#R2 




#import matplotlib.pyplot as plt #데이터를 가시적으로 보여줌
#plt.scatter(x, y)
#plt.plot(x, y_predict, color='red')
#plt.show()













