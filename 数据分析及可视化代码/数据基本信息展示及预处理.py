import pandas as pd

pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option('display.max_columns', 20)

# 加载数据
data_path = 'DATA/Summary listings.csv'
airbnb = pd.read_csv(data_path)
print('数据集展示：\n', airbnb.head())
print('数据集大小：\n', airbnb.shape)
print('数据集字段：\n', airbnb.columns)

# 去除无关字段
airbnb = airbnb.drop(['id', 'name', 'host_name', 'last_review'], axis=1)

print('预处理前:')
print('数据集信息：\n', airbnb.info())
print('各字段缺失值统计：\n', pd.DataFrame(airbnb.isnull().sum(), columns=['缺失值计数']))
print('数据集重复行统计：\n', airbnb.duplicated().sum())
print('数据集信息统计：\n', airbnb.describe())

# 数据预处理
airbnb = airbnb.drop(['neighbourhood_group'], axis=1)
airbnb['reviews_per_month'].fillna(0, inplace=True)
airbnb['license'].fillna('no license', inplace=True)

print('预处理后:')
print('各字段缺失值统计：\n', pd.DataFrame(airbnb.isnull().sum(), columns=['缺失值计数']))
print('数据集信息统计：\n', airbnb.describe())
