# logistic regression :: 논리회귀 , 이진분류에만 사용!!!! regression + sigmoid

from calendar import EPOCH
from sklearn.datasets import load_breast_cancer, load_iris, load_wine, load_diabetes, load_boston
import torch
import torch.nn as nn
import torch.optim as optim

import pandas as pd
import numpy as np


USE_CUDA = torch.cuda.is_available()
DEVICE = torch.device('cuda:0' if USE_CUDA else 'cpu')
print('torch : ', torch.__version__, '사용 DEVICE : ', DEVICE)
# torch :  1.12.1 사용 DEVICE :  cuda:0



# 1. 데이터
path = './_data/ddarung/'
train_set = pd.read_csv(path+'train.csv',index_col=0) # index_col = n : n번째 칼럼을 인덱스로 인식
# print(train_set)
# print(train_set.shape) # (1459, 10)

test_set = pd.read_csv(path+'test.csv', index_col=0)
# print(test_set)
# print(test_set.shape) # (715, 9)

### 결측치 처리(일단 제거로 처리) ###
print(train_set.info())
print(train_set.isnull().sum()) # 결측치 전부 더함
# train_set = train_set.dropna() # nan 값(결측치) 열 없앰
train_set = train_set.fillna(0) # 결측치 0으로 채움
print(train_set.isnull().sum()) # 없어졌는지 재확인

x = train_set.drop(['count'], axis=1) # axis = 0은 열방향으로 쭉 한줄(가로로 쭉), 1은 행방향으로 쭉 한줄(세로로 쭉)
y = train_set['count']

print(x.shape, y.shape) # (1328, 9) (1328,)

x = torch.Tensor(x.values)
y = torch.Tensor(y.values)

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size=0.7, shuffle=True, random_state=123)

x_train = torch.FloatTensor(x_train)
y_train = torch.FloatTensor(y_train).to(DEVICE)
x_test = torch.FloatTensor(x_test)
y_test = torch.FloatTensor(y_test).to(DEVICE)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

x_train = torch.FloatTensor(x_train).to(DEVICE)
x_test = torch.FloatTensor(x_test).to(DEVICE)

print(x_train.size())
print(x_train.shape)

# DateLoader 시작
from torch.utils.data import TensorDataset, DataLoader
train_set = TensorDataset(x_train, y_train) # x, y 를 합쳐준다.
test_set = TensorDataset(x_test, y_test) 

# print(train_set) # <torch.utils.data.dataset.TensorDataset object at 0x000002A121CDBF70>
# print("="*30, "train_set[0]") 
# print(train_set[0])
# print("="*30, "train_set[0][0]")
# print(train_set[0][0])
# print("="*30, "train_set[0][1]")
# print(len(train_set[0][1]))
# print("="*30, "train_set 총 갯수")
# print(len(train_set)) # 398

# x, y  배치 결합
train_loader = DataLoader(train_set, batch_size=20, shuffle=True)
test_loader = DataLoader(test_set, batch_size=20, shuffle=True)

# print(train_loader) # <torch.utils.data.dataloader.DataLoader object at 0x000002B437F0E910>
# print("="*30, "train_loader[0]") 
# print(train_loader[0]) # ERROR
# print("="*30, "train_loader[0][0]")
# print(train_loader[0][0])
# print("="*30, "train_loader[0][1]")
# print(len(train_loader[0][1]))
# print("="*30, "train_loader 총 갯수")
# print(len(train_loader)) # 398


# model class 화 
# class ()안에는 상위클래스만 넣을수있음
class Model(nn.Module) :
    def __init__(self, input_dim, output_dim) :
        # super().__init__() # super 사용시 불러온 모듈의 함수와 변수 모두 사용하겠다
        super(Model, self).__init__() # 위와같음
        
        self.linear1 = nn.Linear(input_dim, 64)
        self.linear2 = nn.Linear(64, 32)
        self.linear3 = nn.Linear(32, 16)
        self.linear4 = nn.Linear(16, output_dim)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, input_size): 
        x = self.linear1(input_size)                
        x = self.relu(x)                
        x = self.linear2(x)
        x = self.relu(x)                                
        x = self.linear3(x)
        x = self.relu(x)                                
        x = self.linear4(x)
        x = self.sigmoid(x)
        return x 
    
    
model = Model(9, 1).to(DEVICE)

#3. 컴파일, 훈련

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)



def train(model, criterion, optimizer, loader):
    # model.train()

    total_loss = 0
    
    for x_batch, y_batch in loader :
        optimizer.zero_grad()
        hypothesis = model(x_batch) # batch 단위대로 들어감
        loss = criterion(hypothesis, y_batch)
        
        loss.backward()
        optimizer.step()
        total_loss += loss.item() # 회당 나오는 loss를 더해줌(누적)
        
    return total_loss / len(loader)

EPOCHS = 200

for epoch in range(1, EPOCHS+1):
    loss = train(model, criterion, optimizer, train_loader)
    if epoch %  10 == 0 : 
        print('epoch : {}, loss :{}'.format(epoch, loss)) 
    
       
def evaluate(model, criterion, loader):
    model.eval()
    total_loss = 0

    for x_batch, y_batch in loader:
        with torch.no_grad():
            hypothesis = model(x_batch)
            loss = criterion(hypothesis, y_batch)
            total_loss += loss.item()
        
    return total_loss
    
loss = evaluate(model, criterion, test_loader)
print('최종 LOSS : ', loss)

y_pred = model(x_test)

from sklearn.metrics import r2_score
score = r2_score(y_test.cpu().detach().numpy(), y_pred.cpu().detach().numpy())
print('R2 : ', score)


'''
최종 LOSS :  353756.5283203125
R2 :  -1.666844053689624

'''



