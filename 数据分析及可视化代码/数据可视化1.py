import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
import json


def create_neighbourhood_marker(geojson, Am_map):
    for feature in geojson.data['features']:
        # 提取区域名称
        name = feature['properties']['neighbourhood']

        # 提取区域中心坐标
        coordinates = feature['geometry']['coordinates'][0][0]
        coordinates = np.array(coordinates)
        center_lon = (np.max(coordinates[:, 0]) + np.min(coordinates[:, 0])) / 2
        center_lat = (np.max(coordinates[:, 1]) + np.min(coordinates[:, 1])) / 2

        # 创建标记并添加到地图上
        folium.Marker(location=[center_lat, center_lon],
                      popup=name,
                      icon=folium.Icon(icon='home')).add_to(Am_map)


# 阿姆斯特丹经纬度
Amsterdam_latitude = 52.36
Amsterdam_longitude = 4.9

# 载入房源数据
data_path = 'DATA/Summary listings.csv'
airbnb = pd.read_csv(data_path)
# 载入地理数据
geojson_path = 'DATA/neighbourhoods.geojson'
Am_geo = folium.GeoJson(geojson_path)
# 查看地理数据特征
with open(geojson_path, 'r') as f:
    geojson_data = json.load(f)
features = geojson_data['features'][0]
print(features)

# ##### Map 1 #####
# # 房源数量分布图
# Am_map_1 = folium.Map(location=[Amsterdam_latitude, Amsterdam_longitude], zoom_start=12)
# # 房源数量统计
# neighbourhood = pd.DataFrame(airbnb['neighbourhood'].groupby(airbnb['neighbourhood']).count())
# neighbourhood.rename(columns={'neighbourhood': 'number of rooms'}, inplace=True)
# neighbourhood.reset_index(level=0, inplace=True)
#
# # 设置社区标签
# create_neighbourhood_marker(Am_geo, Am_map_1)
# # 绘制分布图
# choropleth_map = folium.Choropleth(geo_data=geojson_path,
#                                    data=neighbourhood,
#                                    columns=['neighbourhood', 'number of rooms'],
#                                    key_on='feature.properties.neighbourhood',
#                                    fill_color='YlOrRd',
#                                    legend_name='Number of Rooms')
# choropleth_map.add_to(Am_map_1)
#
# # 保存房源数量分布图
# Am_map_1.save('Amsterdam_Room_Number_Choropleth.html')
#
# ##### Map 2 #####
# # 房源分布热力图
# Am_map_2 = folium.Map(location=[Amsterdam_latitude, Amsterdam_longitude], zoom_start=12)
#
# # 绘制热力图
# HeatMap(airbnb[['latitude', 'longitude']],
#         radius=10,
#         gradient={0.2: 'blue',
#                   0.4: 'purple',
#                   0.6: 'orange',
#                   0.8: 'red'}).add_to(Am_map_2)
#
# # 保存房源分布热力图
# Am_map_2.save('Amsterdam_Room_Heatmap.html')
#
# ##### Map 3 #####
# # 房源评论数量分布图
# Am_map_3 = folium.Map(location=[Amsterdam_latitude, Amsterdam_longitude], zoom_start=12)
# # 房源评论数量统计
# reviews = pd.DataFrame(airbnb['number_of_reviews'].groupby(airbnb['neighbourhood']).sum())
# reviews.reset_index(level=0, inplace=True)
#
# # 设置社区标签
# create_neighbourhood_marker(Am_geo, Am_map_3)
# # 绘制分布图
# choropleth_map = folium.Choropleth(geo_data=geojson_path,
#                                    data=reviews,
#                                    columns=['neighbourhood', 'number_of_reviews'],
#                                    key_on='feature.properties.neighbourhood',
#                                    fill_color='YlOrRd',
#                                    legend_name='Number of Reviews')
# choropleth_map.add_to(Am_map_3)
#
# # 保存房源评论数量分布图
# Am_map_3.save('Amsterdam_Review_Number_Choropleth.html')

##### Map 4 #####
# 前100热门房源分布图
Am_map_4 = folium.Map(location=[Amsterdam_latitude, Amsterdam_longitude], zoom_start=12)
# 筛选前100热门房源
top_100_room = airbnb.sort_values('number_of_reviews', ascending=False).head(100)

# 创建标记聚类
room_markercluster = MarkerCluster().add_to(Am_map_4)
for lat, lng, label in zip(top_100_room['latitude'], top_100_room['longitude'], top_100_room['name']):
    folium.Marker(location=[lat, lng],
                  icon=None,
                  popup=label).add_to(room_markercluster)
Am_map_4.add_child(room_markercluster)

folium.GeoJson(data=geojson_path,
               style_function=lambda feature: {
                   'fillColor': 'blue',
                   'color': 'black',
                   'weight': 2}).add_to(Am_map_4)

# 保存前100热门房源分布图
Am_map_4.save('Amsterdam_top_100_room_Choropleth.html')
