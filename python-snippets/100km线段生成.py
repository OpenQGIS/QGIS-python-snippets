from qgis.core import QgsDistanceArea, QgsPointXY, QgsGeometry, QgsVectorLayer, QgsFeature, QgsProject

# 初始化测地距离计算器
distance_calculator = QgsDistanceArea()
distance_calculator.setEllipsoid('WGS84')

# 创建图层
layer = QgsVectorLayer("LineString?crs=EPSG:4326", "100km_lines_at_105E", "memory")
provider = layer.dataProvider()

# 定义纬度范围
latitudes = range(-80, 81, 10)
base_lon = 105

for lat in latitudes:
    if abs(lat) >= 89:  # 跳过极点
        continue
    
    start_point = QgsPointXY(base_lon, lat)
    # 计算 1 度经度的距离（千米）
    delta_lon = distance_calculator.measureLine([start_point, QgsPointXY(base_lon + 1, lat)]) / 1000
    # 计算 100 千米对应的经度跨度
    end_lon = base_lon + (100 / delta_lon)
    end_point = QgsPointXY(end_lon, lat)
    
    # 创建线段
    line = QgsGeometry.fromPolylineXY([start_point, end_point])
    
    # 添加到图层
    feature = QgsFeature()
    feature.setGeometry(line)
    provider.addFeature(feature)

# 更新图层并添加到项目
layer.updateExtents()
QgsProject.instance().addMapLayer(layer)
