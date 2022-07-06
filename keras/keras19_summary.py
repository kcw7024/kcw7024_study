from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
import numpy as np

#1. 데이터

x = np.array([1,2,3])
y = np.array([1,2,3])


#2. 모델구성

model = Sequential()
model.add(Dense(5, input_dim=1))
model.add(Dense(3, activation='relu'))
model.add(Dense(4, activation='sigmoid'))
model.add(Dense(2, activation='relu'))
model.add(Dense(1))

model.summary() #연산량을 보여준다
#y=wx+b 에서 바이어스(b)가 1개의 추가 노드를 차지





