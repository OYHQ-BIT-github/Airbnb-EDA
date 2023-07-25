import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'Times New Roman'

pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option('display.max_columns', 20)

# 加载数据
data_path = 'DATA/Summary listings.csv'
airbnb = pd.read_csv(data_path)
airbnb = airbnb.drop(['id', 'name', 'host_name', 'last_review', 'neighbourhood_group'], axis=1)
airbnb['reviews_per_month'].fillna(0, inplace=True)
airbnb['license'].fillna('no license', inplace=True)

# 各社区评论数统计
reviews = pd.DataFrame(airbnb['number_of_reviews'].groupby(airbnb['neighbourhood']).sum())
reviews = reviews.sort_values(by='number_of_reviews')
colors = plt.cm.viridis(np.linspace(0, 0.95, len(reviews.index)))
fig = plt.figure(figsize=(10, 6))
plt.barh(reviews.index, reviews['number_of_reviews'], color=colors)
plt.title('Number of reviews in each neighbourhood')
plt.xlabel('number of reviews')
plt.ylabel('neighbourhood')
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.legend().set_visible(False)
plt.tight_layout()
plt.show()

# 以评论数作为指标，筛选出前6个热门社区
top_6_neighbourhood = reviews.index[::-1][:6]

# 前6个热门社区的房源类型分布
room_type = pd.DataFrame(airbnb['room_type'].groupby(airbnb['neighbourhood']).value_counts())
for i in range(6):
    plt.subplot(2, 3, i + 1)
    neighbourhood_room_type = room_type.loc[top_6_neighbourhood[i]]
    if 'Shared room' not in neighbourhood_room_type.index:
        neighbourhood_room_type.loc['Shared room'] = 0
    if 'Hotel room' not in neighbourhood_room_type.index:
        neighbourhood_room_type.loc['Hotel room'] = 0
    new_row_name = 'Shared room/Hotel room'
    new_row_data = neighbourhood_room_type.loc['Shared room'] + neighbourhood_room_type.loc['Hotel room']
    neighbourhood_room_type.loc[new_row_name] = new_row_data
    neighbourhood_room_type.drop(['Shared room', 'Hotel room'], inplace=True)
    plt.pie(neighbourhood_room_type.iloc[:, 0], autopct='%1.1f%%', pctdistance=1.2)
    circle = plt.Circle((0, 0), 0.7, color='white')
    plt.gca().add_artist(circle)
    plt.legend(neighbourhood_room_type.index, loc='center', fontsize=7)
    plt.title(top_6_neighbourhood[i], fontsize=10)
plt.suptitle('Proportion of room type in each neighbourhood')
plt.tight_layout()
plt.show()

# 前6个热门社区的房源价格分布
price = airbnb[airbnb['neighbourhood'].isin(top_6_neighbourhood)][airbnb['price'] < 800]
price['neighbourhood'] = pd.Categorical(price['neighbourhood'], categories=top_6_neighbourhood, ordered=True)
price = price.groupby('neighbourhood')['price']
neighbourhood_price = [group.values for name, group in price]
plt.violinplot(neighbourhood_price, showmedians=True)
plt.xticks([1, 2, 3, 4, 5, 6], price.groups.keys(), fontsize=8)
plt.xlabel('neighbourhood')
plt.ylabel('price')
plt.title('Price distribution in each neighbourhood')
plt.grid(True)
plt.tight_layout()
plt.show()

# 前6个热门社区的最小入住天数分布
minimum_nights = airbnb[airbnb['neighbourhood'].isin(top_6_neighbourhood)][airbnb['minimum_nights'] < 50]
minimum_nights['neighbourhood'] = pd.Categorical(minimum_nights['neighbourhood'], categories=top_6_neighbourhood,
                                                 ordered=True)
minimum_nights = minimum_nights.groupby('neighbourhood')['minimum_nights']
neighbourhood_minimum_nights = [group.values for name, group in minimum_nights]
plt.violinplot(neighbourhood_minimum_nights)
plt.xticks([1, 2, 3, 4, 5, 6], minimum_nights.groups.keys(), fontsize=8)
plt.xlabel('neighbourhood')
plt.ylabel('minimum nights')
plt.title('minimum nights distribution in each neighbourhood')
plt.grid(True)
plt.tight_layout()
plt.show()

# # 筛选出后6个热门社区
# bottom_6_neighbourhood = reviews.index[::-1][-6:]
#
# room_type = pd.DataFrame(airbnb['room_type'].groupby(airbnb['neighbourhood']).value_counts())
# for i in range(6):
#     plt.subplot(2, 3, i + 1)
#     neighbourhood_room_type = room_type.loc[bottom_6_neighbourhood[i]]
#     if 'Shared room' not in neighbourhood_room_type.index:
#         neighbourhood_room_type.loc['Shared room'] = 0
#     if 'Hotel room' not in neighbourhood_room_type.index:
#         neighbourhood_room_type.loc['Hotel room'] = 0
#     new_row_name = 'Shared room/Hotel room'
#     new_row_data = neighbourhood_room_type.loc['Shared room'] + neighbourhood_room_type.loc['Hotel room']
#     neighbourhood_room_type.loc[new_row_name] = new_row_data
#     neighbourhood_room_type.drop(['Shared room', 'Hotel room'], inplace=True)
#     plt.pie(neighbourhood_room_type.iloc[:, 0], autopct='%1.1f%%', pctdistance=1.2)
#     circle = plt.Circle((0, 0), 0.7, color='white')
#     plt.gca().add_artist(circle)
#     plt.legend(neighbourhood_room_type.index, loc='center', fontsize=7)
#     plt.title(bottom_6_neighbourhood[i], fontsize=10)
# plt.suptitle('Proportion of room type in each neighbourhood')
# plt.tight_layout()
# plt.show()
#
# price = airbnb[airbnb['neighbourhood'].isin(bottom_6_neighbourhood)][airbnb['price'] < 800]
# price['neighbourhood'] = pd.Categorical(price['neighbourhood'], categories=bottom_6_neighbourhood, ordered=True)
# price = price.groupby('neighbourhood')['price']
# neighbourhood_price = [group.values for name, group in price]
# plt.violinplot(neighbourhood_price)
# plt.xticks([1, 2, 3, 4, 5, 6], price.groups.keys(), fontsize=8)
# plt.xlabel('neighbourhood')
# plt.ylabel('price')
# plt.title('Price distribution in each neighbourhood')
# plt.grid(True)
# plt.tight_layout()
# plt.show()
#
# minimum_nights = airbnb[airbnb['neighbourhood'].isin(bottom_6_neighbourhood)][airbnb['minimum_nights'] < 50]
# minimum_nights['neighbourhood'] = pd.Categorical(minimum_nights['neighbourhood'], categories=bottom_6_neighbourhood,
#                                                  ordered=True)
# minimum_nights = minimum_nights.groupby('neighbourhood')['minimum_nights']
# neighbourhood_minimum_nights = [group.values for name, group in minimum_nights]
# plt.violinplot(neighbourhood_minimum_nights)
# plt.xticks([1, 2, 3, 4, 5, 6], minimum_nights.groups.keys(), fontsize=8)
# plt.xlabel('neighbourhood')
# plt.ylabel('minimum_nights')
# plt.title('minimum_nights distribution in each neighbourhood')
# plt.grid(True)
# plt.tight_layout()
# plt.show()
