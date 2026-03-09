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
all_results = []

for i, param in enumerate(param_files):
    file_name = os.path.basename(param)

    with open(param,"r", encoding="utf-8") as f:
        content = f.read()

    data = extract_json_safely(content)

    print(f"Extracted {i+1} / {len(param_files)} \n")
    print(data)


    if data:
        # 创建一个扁平的字典来存储这篇论文的所有参数
        row = {
            #"file_name": os.path.basename(param),
            "title": data.get("title", "N/A"),
            "citation": data.get("citation", "N/A")
        }
        
        # --- 分类别提取 ---
        
        # 1. 初始条件 (Initial Conditions)
        init = data.get("initial_conditions", {})
        row["init_arrangement"] = init.get("arrangement")
        row["init_dist_center"] = init.get("initial_distance_center")
        row["init_angle"] = init.get("initial_angle")
        
        # 2. 颗粒特性 (Particle Properties)
        part = data.get("particle_properties", {})
        row["part_identical"] = part.get("is_identical")
        row["part_rho1"] = part.get("density_p1") or part.get("density_ratio_p1_p2")
        row["part_d1"] = part.get("diameter_d1") or part.get("diameter_ratio_d1_d2")
        
        # 3. 流体特性 (Fluid Properties)
        fluid = data.get("fluid_properties", {})
        row["fluid_re"] = fluid.get("reynolds_number")
        row["fluid_mu"] = fluid.get("viscosity")
        
        # 4. 密度特性
        row["rho_ratio_p_f"] = data.get("density_properties", {}).get("density_ratio_p_f")
        
        # 5. 几何参数
        geom = data.get("geometry_parameters", {})
        row["geom_dim"] = geom.get("dimension")
        row["geom_domain"] = geom.get("domain_size")
        
        # 6. 其他无量纲数 (这个比较特殊，可能有很多 key)
        others = data.get("other_dimensionless_numbers", {})
        if isinstance(others, dict):
            row["num_ga"] = others.get("galileo_number") or others.get("ga_number")
            row["num_gr"] = others.get("grashof_number")
        
        all_results.append(row)

# --- 汇总导出 ---
df = pd.DataFrame(all_results)
df.to_csv("param_data/summary_data.csv", index=False, encoding="utf-8-sig")


