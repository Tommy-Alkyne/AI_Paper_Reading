# Please install OpenAI SDK first: `pip3 install openai`
# Add API key: export DEEPSEEK_API_KEY="your_api_key"
import glob
import os

from openai import OpenAI
from pypdf import PdfReader

USE_API = True

client = None
if USE_API:
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    model_name = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
    if not api_key:
        raise RuntimeError("未找到API Key，请设置环境变量: DEEPSEEK_API_KEY")

    client = OpenAI(api_key=api_key, base_url=base_url)
    print(f"API_PROVIDER=deepseek, base_url={base_url}, model={model_name}")


def extract_pdf_text(pdf_path: str) -> str:
    """提取PDF文本"""
    try:
        reader = PdfReader(pdf_path)
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
        return "\n\n".join(pages).strip()
    except Exception as e:
        return ""


pdf_files = sorted(glob.glob("./files/*.pdf"))
output_dir = "./files_extracted"
os.makedirs(output_dir, exist_ok=True)

print(f"找到 {len(pdf_files)} 个PDF文件")
print("=" * 60)

for index, pdf_file in enumerate(pdf_files, start=1):
    pdf_name = os.path.basename(pdf_file)
    pdf_stem = os.path.splitext(pdf_name)[0]
    txt_path = os.path.join(output_dir, f"{pdf_stem}.txt")

    print(f"\n[{index}/{len(pdf_files)}] 提取并分析: {pdf_name}")

    # 本地提取PDF文本
    full_text = extract_pdf_text(pdf_file)
    if not full_text:
        print("提取文本失败或为空，跳过")
        continue
    print(f"提取成功，文本长度: {len(full_text)} 字符")

    # 保存到txt文件
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"文本已保存: {txt_path}")

    if not USE_API:
        print("USE_API=False，跳过API分析")
        continue

    prompt_text = full_text

    # 从txt文件读取并发送给API分析
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            file_full_text = f.read()
        prompt_text = file_full_text

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant that analyzes academic papers. Please output the note as a markdown file. The first line should be the year and title of the paper. the third line should be \\cite{{{pdf_stem}}}. if the paper focuses on calculation, add #cal in the second line. if the paper focuses on the physical mechanism, add #phy in the second line. then add another research obj, choosing from #obj/heat #obj/shape #obj/Re #obj/channel #obj/density #obj/init in the second line.",
                },
                {
                    "role": "user",
                    "content": (
                        f"请分析以下论文（{pdf_name}）。\n"
                        f"这篇文章是否研究了DKT现象, 改变了哪些参数, 根据改变的参数归纳了哪些regime, 背后有哪些机理? 详细归纳机理.\n"
                        f"改变参数的范围是什么? 颗粒是否是全同的? 这两个问题请直接放到表格里\n"
                        f"不要有任何好的, 我这就回答问题这样的话. 直接输出参数范围表格与笔记. 例如\n"
                        f"2021 Interaction between two unequal particles at intermediate Reynolds numbers- A pattern of horizontal oscillatory motion\n"
                        f"\cite{{nieInteractionTwoUnequal2021}}\n"
                        f"***\n"
                        f"该文章通过 2D-LBM（格点玻尔兹曼法）深入研究了**DKT现象**（作为基础及验证），并重点揭示了非全同颗粒（密度和直径均不同）特有的**水平振荡运动（HOM）**模式。\n"
                        f"\n"
                        f"# Params range\n"
                        f"| 参数类型 | 研究参数 (Params) | 范围/取值 (Range/Values) |\n"
                        f"| :--- | :--- | :--- |\n"
                        f"| **几何参数** | 直径比 ($r = d_2/d_1$) | 0.2 - 0.75 |\n"
                        f"| | 限制比/通道宽度 ($\beta = L/d_1$) | 3.5 - 12 (基准值为 5) |\n"
                        f"| **密度参数** | 颗粒密度比 ($\lambda = \rho_2/\rho_1$) | 1.0 - 3.5 |\n"
                        f"| | 颗粒-流体密度比 ($\gamma = \rho_1/\rho_f$) | 1.05 - 2.5 (基准值为 1.5) |\n"
                        f"| **动力学参数** | 雷诺数 ($Re = U_0d_1/\nu$) | 10 - 50 |\n"
                        f"| **初始条件** | 释放位置 | 垂直排列 (大球在左下，小球在右上或反之) |\n"
                        f"\n"
                        f"# Regime and mechanism\n"
                        f"**1. 归纳的演化区间 (Regimes)**\n"
                        f"该研究在 $(r, \lambda)$ 参数空间中识别出以下五种主要模式：\n"
                        f"*   **DKT-I (经典模式):** 典型的下落-接触-翻滚。翻滚后大颗粒领先，小颗粒落后。\n"
                        f"*   **DKT-II (逆向追赶模式):** 翻滚后由于小颗粒足够重（$\lambda$ 较大），会迅速移动到大颗粒下方再次形成尾流吸引，产生\"逆向追赶（Inverse drafting）\"过程。\n"
                        f"*   **HOM (水平振荡模式):** 发现于 $r \approx 0.3$ 且 $\lambda$ 较大时。特征是大颗粒（轻）位于小颗粒（重）正上方，两者在水平方向产生强烈的周期性对称振荡。\n"
                        f"*   **VSS (垂直稳态模式):** 当 $\lambda$ 接近 $\lambda_{{max}}$ 或雷诺数较低时，HOM 分岔为一种稳定的直线排列下落状态，不再振荡。\n"
                        f"*   **Separated (分离模式):** 当 $\lambda$ 极小或极大时，由于两球终端速度差异过大，无法维持水动力相互作用，两球最终彼此分离。\n"
                        f"\n"
                        f"**2. 核心机理 (Mechanism)**\n"
                        f"*   **尾流捕获与位置交换:** 领先颗粒的尾流降低了后随颗粒的阻力。对于非全同颗粒，大颗粒领先时产生的尾流显著强于小颗粒，这种非对称性决定了 DKT 过程是否仅发生一次。\n"
                        f"*   **Hopf 分岔机制:** 文章指出 HOM 模式的出现本质上是系统的 **Hopf 分岔**。随着密度比 $\lambda$ 增加，颗粒从稳态沉降转变为周期性振荡。\n"
                        f"*   **非对称性与回复力:** 在 HOM 模式中，重力、浮力与不对称的尾流升力共同作用。当颗粒偏离中心线时，水动力产生一个回复力使其摆回，形成类似摆锤的水平往复运动。\n"
                        f"*   **壁面受限机理:** 窄通道（$\beta$ 较小）会抑制 DKT 触发。存在一个临界限制比（约 $\beta \approx 7.5$），跨越此值后，颗粒的沉降速度和振荡频率会因壁面阻力的突变而发生非线性跳变。\n"
                        f"*   **惯性主导:** 当颗粒-流体密度比 $\gamma$ 较大时（颗粒惯性极强），尾流无法有效驱动颗粒产生水平振荡，HOM 模式消失。\n"
                        f"论文文本：\n{prompt_text}"
                    ),
                },
            ],
            stream=False,
        )
        
        output_content = response.choices[0].message.content
        
        # 提取第一行作为文件名
        lines = output_content.split('\n', 1)
        first_line = lines[0].strip()
        remaining_content = lines[1] if len(lines) > 1 else ""
        
        # 清理文件名（移除特殊字符）
        filename = "".join(c if c.isalnum() or c in ' -_.' else '' for c in first_line)
        filename = filename.strip()
        
        # 创建notes目录
        notes_dir = "./notes"
        os.makedirs(notes_dir, exist_ok=True)
        
        # 保存到markdown文件
        md_path = os.path.join(notes_dir, f"{filename}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(remaining_content)
        
        print("API分析完成：")
        print(output_content)
        print(f"\n✅ 分析结果已保存: {md_path}")
    except Exception as exc:
        print(f"分析失败: {exc}")

    break

print("\n" + "=" * 60)
print(f"处理完成！共处理 {len(pdf_files)} 个PDF文件")
print(f"文本文件保存在: {output_dir}")