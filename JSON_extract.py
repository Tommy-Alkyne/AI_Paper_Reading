import re
import json
import glob
import os
import pandas as pd

def extract_json_safely(text):
    # 1. 找到最后一个 "# JSON" 的位置
    marker = "# JSON"
    idx = text.rfind(marker)
    
    # 如果找到了标记，就只看标记之后的内容；没找到就看全文
    if idx != -1:
        text_after_json_label = text[idx + len(marker):].strip()
    else:
        text_after_json_label = text.strip()

    # 2. 在这段内容里，找第一个 '{' 和 最后一个 '}'
    # 这样不管有没有 ```json 标签，都能精准提取中间的 {} 整体
    start = text_after_json_label.find('{')
    end = text_after_json_label.rfind('}')

    if start == -1 or end == -1:
        return None

    json_str = text_after_json_label[start:end+1].strip()

    # 3. 解析 JSON
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        # 如果解析失败，可能是因为 AI 在里面写了不规范的单引号
        try:
            # 最后的倔强：尝试处理单引号问题（可选）
            # return json.loads(json_str.replace("'", '"'))
            print(f"JSON 解析失败: {e}")
            return None
        except:
            return None
    
    
param_files = sorted(glob.glob("./notes/*.md"))
results = []

for i, param in enumerate(param_files):
    with open(param, "r", encoding="utf-8") as f:
        content = f.read()
    data = extract_json_safely(content)
    if not data: continue

    print(f"Extracted {i+1}/{len(param_files)} files")
    # 获取子字典的防御性函数
    def g(category, key, default="N/A"):
        return data.get(category, {}).get(key, default)

    row = {
        "citation": data.get("citation", "N/A"),
        "title": data.get("title", "N/A"),
        "dim": g("geometry_parameters", "dimension"),
        
        # 颗粒核心参数：尝试兼容多种写法
        "is_identical": g("particle_properties", "is_identical"),
        "rho_pf": g("density_properties", "density_ratio_p_f"),
        "d_ratio": g("particle_properties", "diameter_ratio_d1_d2") or "1.0",
        "density_p1": g("particle_properties", "density_p1"),
        "density_p2": g("particle_properties", "density_p2"),
        "diameter_p1": g("particle_properties", "diameter_p1"),
        "diameter_p2": g("particle_properties", "diameter_p2"),
        
        # 初始条件
        "arrangement": g("initial_conditions", "arrangement"),
        "dist_v": g("initial_conditions", "initial_distance_vertical"),
        "dist_h": g("initial_conditions", "initial_distance_horizontal"),
        "dist_c": g("initial_conditions", "initial_distance_center"),
        
        # 流体参数
        "Re": g("fluid_properties", "reynolds_number"),
        "viscosity": g("fluid_properties", "viscosity"),

        #计算参数
        "domain_size": g("gemetry_parameters", "domain_size"),
        "boudary": g("geometry_parameters", "boundary_conditions"),
        
        # 复杂物理量（合并到一起）
        "Ga": g("other_dimensionless_numbers", "galileo_number") or g("other_dimensionless_numbers", "ga_number"),
        "Gr": g("other_dimensionless_numbers", "grashof_number"),
        "Pr": g("other_dimensionless_numbers", "prandtl_number"),
        "e_n": g("other_dimensionless_numbers", "restitution_coefficient") or g("other_dimensionless_numbers", "restitution_coefficient"),
    }

    # 列表转字符串处理
    for k, v in row.items():
        if isinstance(v, list):
            row[k] = "; ".join(map(str, v))
            
    results.append(row)

# 导出
df = pd.DataFrame(results)
df.to_csv("param_data/summary_data.csv", index=False, encoding="utf-8-sig")