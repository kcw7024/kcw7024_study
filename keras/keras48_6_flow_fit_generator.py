from grpc import AuthMetadataContext
from tensorflow.keras.datasets import fashion_mnist
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
import numpy as np

(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

train_datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    vertical_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1,
    rotation_range=5,
    zoom_range=0.1,
    shear_range=0.7,
    fill_mode='nearest'
)

augument_size = 40 #증폭
randidx = np.random.randint(x_train.shape[0], size=augument_size) #(60000)
# x_train.shape[0] 범위내에서 augment_size 만큼 정수값을 뽑아준다
#randint 균일 분포의 정수 난수(랜덤) 생성 (최소값, 최대값, 조건) 사이에서 생성해준다.
#x_train.shape #(60000, 28, 28)
print(x_train.shape[0]) # 60000
print(randidx)          # [20014 40476  4736 ... 53470 50713 47713] 랜덤으로 
print(np.min(randidx), np.max(randidx)) # 5 59997 랜덤으로 뽑은 40000개

print(type(randidx)) # <class 'numpy.ndarray'>

x_augmented = x_train[randidx].copy()
y_augmented = y_train[randidx].copy()


#print(x_augmented.shape) #(40000, 28, 28)
#print(y_augmented.shape) #(40000,)



x_train = x_train.reshape(60000, 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)
x_augmented = x_augmented.reshape(x_augmented.shape[0], x_augmented.shape[1], x_augmented.shape[2], 1)

x_train = np.concatenate((x_train, x_augmented))
y_train = np.concatenate((y_train, y_augmented))

#이미지 변경
xy_train  = train_datagen.flow(x_augmented, y_augmented, batch_size=augument_size, shuffle=False)
xy_train1  = train_datagen.flow(x_train, y_train, batch_size=augument_size, shuffle=False)
#print(x_augmented)
#print(x_augmented.shape) #(40000, 28, 28, 1)

# x_train = np.concatenate((x_train, x_augmented))
# y_train = np.concatenate((y_train, y_augmented))

xy_train2 = np.concatenate((xy_train, xy_train1))

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

#print(xy_train2.shape ) # (100000, 28, 28, 1) (100000,) 

#x_train = x_train.reshape(60000, 28, 28, 1)



### 모델구성 ###
# 성능비교, 증폭 전 후 비교
#2. 모델

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Conv2D, Flatten


model = Sequential()
model.add(Conv2D(32, (2,2), input_shape=(28, 28, 1), activation='relu'))
model.add(Conv2D(32, (3,3), activation='relu'))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(10, activation='softmax'))

#3. 컴파일, 훈련

model.compile(loss ='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#배치를 최대로 잡으면 이방법도 가능
hist = model.fit(x_train, y_train, epochs=30, batch_size=15, validation_split=0.2) 

accuracy = hist.history['accuracy']
val_accuracy = hist.history['val_accuracy']
loss = hist.history['loss']
val_loss = hist.history['val_loss']


print('loss : ', loss[-1])
print('val_accuracy : ', val_accuracy[-1])
print('accuracy : ', accuracy[-1])
print('val_loss : ', val_loss[-1])



# 증폭 전

# loss :  0.06670371443033218
# val_accuracy :  0.8924166560173035
# accuracy :  0.9821041822433472
# val_loss :  0.6203776597976685

# 증폭 후

# loss :  0.06313396245241165
# val_accuracy :  0.7648500204086304
# accuracy :  0.986762523651123
# val_loss :  1.8850736618041992