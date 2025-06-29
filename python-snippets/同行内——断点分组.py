from qgis.PyQt.QtCore import QVariant

# 替换为你的图层名称
layer = QgsProject.instance().mapLayersByName('point')[0]

# 添加字段，如果已经存在可以跳过这一行
if 'group' not in [field.name() for field in layer.fields()]:
    layer.dataProvider().addAttributes([QgsField('group', QVariant.Int)])
    layer.updateFields()

# 获取字段索引
group_idx = layer.fields().indexOf('group')

# 收集要素，并按 row_index 分组
from collections import defaultdict

features_by_row = defaultdict(list)

for feat in layer.getFeatures():
    row = feat['row_index']
    features_by_row[row].append(feat)

layer.startEditing()

group_id = 1  # 初始组号

for row, feats in features_by_row.items():
    # 按 col_index 排序
    feats_sorted = sorted(feats, key=lambda f: f['col_index'])
    
    prev_col = None
    for feat in feats_sorted:
        col = feat['col_index']
        if prev_col is None or (col - prev_col > 1):
            current_group = group_id
            group_id += 1
        # 否则仍属于当前组
        # 设置字段值
        layer.changeAttributeValue(feat.id(), group_idx, current_group)
        prev_col = col

layer.commitChanges()
print("分组完成！")
