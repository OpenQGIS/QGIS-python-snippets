# =========== 自己修改的参数在这里 ===========
names = ["全国铁路数据 — 铁路站点", "全国铁路数据 — 铁路线"]
out = r"C:\Users\tesla\Downloads\全国铁路数据.geojson"
# ============================================

from qgis.core import QgsProject
import json

NEW_FIELD_NAME = "layer"    # 写入源图层名的字段名

project = QgsProject.instance()
layers = []
for n in names:
    lyr = project.mapLayersByName(n)
    if not lyr:
        print(f"未找到图层：{n}")
        continue
    layers.append(lyr[0])

if not layers:
    raise Exception("没有找到任何可合并图层，请检查 names 列表。")

features_out = []
total = 0

for lyr in layers:
    field_names = [f.name() for f in lyr.fields()]

    for f in lyr.getFeatures():
        geom = f.geometry()
        geom_json = None if geom is None or geom.isEmpty() else json.loads(geom.asJson())

        props = {}
        attrs = f.attributes()
        for i, name in enumerate(field_names):
            val = attrs[i]
            props[name] = val if isinstance(val, (str, int, float, bool, list, dict)) else str(val) if val is not None else None

        props[NEW_FIELD_NAME] = lyr.name()

        features_out.append({
            "type": "Feature",
            "properties": props,
            "geometry": geom_json
        })
        total += 1

feature_collection = {
    "type": "FeatureCollection",
    "features": features_out
}

with open(out, "w", encoding="utf-8") as w:
    json.dump(feature_collection, w, ensure_ascii=False, indent=2)

print(f"完成：{total} 条。输出：{out}")
