import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# 加载数据
data_path = 'DATA/Summary listings.csv'
airbnb = pd.read_csv(data_path)

# 划分字段
cag_col = ['neighbourhood', 'room_type']
x_col = ['neighbourhood', 'latitude', 'longitude',
         'room_type', 'price', 'minimum_nights', 'number_of_reviews',
         'calculated_host_listings_count', 'availability_365']
y_col = ['price']

# 非数值型数据转换成数值型
label = LabelEncoder()
for i in cag_col:
    airbnb[i] = label.fit_transform(airbnb[i])

# 设置特征和标签
X = airbnb[x_col]
Y = airbnb[y_col]
X = np.array(X)
Y = np.array(Y)

# 将数据集划分为训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 创建多层感知机回归器
mlp = MLPRegressor(hidden_layer_sizes=(100, 50), activation='relu', solver='adam', max_iter=200, random_state=42)

# 在训练集上拟合模型
mlp.fit(x_train, y_train)

# 在测试集上进行预测
y_pred = mlp.predict(x_test)

# 计算均方误差
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
# Mean Squared Error: 1.0029741201915732

# 画图展示
plt.plot(y_test, linewidth=1)
plt.plot(y_pred, linestyle='--', linewidth=1)
plt.legend(['test', 'pred'])
plt.yscale('log')
plt.show()
