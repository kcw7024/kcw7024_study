# y = wx + b
from pickletools import optimize
import tensorflow as tf
tf.set_random_seed(123)  # 항상 같은 랜덤값이 지정 됨

# 1. 데이터
# x = [1, 2, 3, 4, 5]
# y = [1, 2, 3, 4, 5]

x = tf.placeholder(tf.float32, shape=[None])
y = tf.placeholder(tf.float32, shape=[None])
# shape :: input shape
W = tf.Variable(tf.random_normal([1]), dtype=tf.float32)  # random_normal = 갯수
b = tf.Variable(tf.random_normal([1]), dtype=tf.float32)

# 2. 모델 구성
hypothesis = x * W + b  # y = wx + b

# 3-1. 컴파일
loss = tf.reduce_mean(tf.square(hypothesis-y))  # mse
# square = 제곱, reduce_mean = 평균
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
train = optimizer.minimize(loss)  # 로스값이 최적화된 minimize위치를 찾아낸다
# model.compile(loss = 'mse', optimizer = 'sgd')

# 3-2. 훈련
# session은 항상 열고난뒤 닫아줘야 한다/ 마지막에 close
with tf.compat.v1.Session() as sess:
    # sess = tf.compat.v1.Session()
    sess.run(tf.global_variables_initializer())  # 초기화 시킨다.

    epochs = 4001
    for step in range(epochs):
        # sess.run(train)
        _, loss_val, W_val, b_val = sess.run([train, loss, W, b],  # 그래프화
                                             feed_dict=(
                                                 {x: [1, 2, 3, 4, 5], y: [1, 2, 3, 4, 5]})
                                             )
        if step % 20 == 0:  # %20 의 나머지가 0이 아닐때 프린트함. 즉, 20번에 한번씩 실행시킨다.
            print(step, loss_val, W_val, b_val)

# _ 의미 :: 따로 정의는 하지 않고 실행만 시키겠다.

# sess.close()
# with문의 개념 :: with 문 안의 내용들은 with 문이  끝날때 자동으로 끝이난다. (sess.close 사용할 필요가 없음)
