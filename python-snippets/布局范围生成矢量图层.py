# 导入核心库
from qgis.core import (
    QgsProject,
    QgsLayoutItemMap,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsField,
    QgsFields
)
from qgis.PyQt.QtCore import QVariant

# 定义布局名称
layout_name = "Layout 1"  # ⭐️ 修改此处为你的布局名

# 获取项目实例和布局管理器
project = QgsProject.instance()
layout_manager = project.layoutManager()

# 按名称查找布局
target_layout = layout_manager.layoutByName(layout_name)
if not target_layout:
    print(f"错误：未找到名为 '{layout_name}' 的布局")
else:
    # 查找布局中的地图项
    map_items = [item for item in target_layout.items() 
                if isinstance(item, QgsLayoutItemMap)]
    
    if not map_items:
        print("错误：布局中未找到地图项")
    else:
        # 获取第一个地图项的范围
        map_item = map_items[0]
        bbox = map_item.extent()
        
        # 创建内存图层（临时矢量层）
        temp_layer = QgsVectorLayer(
            f"Polygon?crs={map_item.crs().authid()}",
            f"{layout_name}_范围",
            "memory"
        )
        
        # 添加属性字段
        provider = temp_layer.dataProvider()
        fields = QgsFields()
        fields.append(QgsField("布局名称", QVariant.String))
        fields.append(QgsField("X最小值", QVariant.Double))
        fields.append(QgsField("Y最小值", QVariant.Double))
        fields.append(QgsField("X最大值", QVariant.Double))
        fields.append(QgsField("Y最大值", QVariant.Double))
        provider.addAttributes(fields)
        temp_layer.updateFields()
        
        # 创建矩形要素
        rect_geom = QgsGeometry.fromRect(bbox)
        feature = QgsFeature()
        feature.setGeometry(rect_geom)
        feature.setAttributes([
            layout_name,
            round(bbox.xMinimum(), 6),
            round(bbox.yMinimum(), 6),
            round(bbox.xMaximum(), 6),
            round(bbox.yMaximum(), 6)
        ])
        
        # 添加要素到图层
        provider.addFeatures([feature])
        
        # 添加到项目
        project.addMapLayer(temp_layer)
        print(f"✅ 已为布局 '{layout_name}' 创建范围图层")
        print(f"📐 X范围: {bbox.xMinimum():.6f} → {bbox.xMaximum():.6f}")
        print(f"📐 Y范围: {bbox.yMinimum():.6f} → {bbox.yMaximum():.6f}")
