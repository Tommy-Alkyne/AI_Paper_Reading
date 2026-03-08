# Please install OpenAI SDK first: `pip3 install openai`
# Add API key: export DEEPSEEK_API_KEY="your_api_key"
import glob
import os

from openai import OpenAI
from pypdf import PdfReader

from extract_pdf import extract_save

prompt_path = "./prompt.*"
out_dir = "./notes"
system_prompt_path = "./system_prompt.*"

client = None

api_key = os.environ.get("DEEPSEEK_API_KEY")
base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
model_name = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
if not api_key:
    raise RuntimeError("未找到API Key，请设置环境变量: DEEPSEEK_API_KEY")

client = OpenAI(api_key=api_key, base_url=base_url)
print(f"API_PROVIDER=deepseek, base_url={base_url}, model={model_name}")



pdf_files = sorted(glob.glob("./files/*.pdf"))
txt_dir = "./files/files_extracted"
os.makedirs(txt_dir, exist_ok=True)

print(f"找到 {len(pdf_files)} 个PDF文件")
print("=" * 60)

for index, pdf_file in enumerate(pdf_files, start=1):
    pdf_name = os.path.basename(pdf_file)
    pdf_stem = os.path.splitext(pdf_name)[0]
    txt_path = os.path.join(txt_dir, f"{pdf_stem}.txt")

    prompt_text = extract_save(pdf_file, pdf_name, pdf_stem, txt_path, save = True)

    # 从txt文件读取并发送给API分析
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            file_full_text = f.read()
        literature_text = file_full_text

        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_text = f.read()

        with open(system_prompt_path, "r", encoding="utf-8") as f:
            system_prompt_text = f.read()

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt_text,
                },
                {
                    "role": "user",
                    "content": (
                        f"请分析以下论文（{pdf_name}）。\n"
                        f"{prompt_text}"
                        f"论文文本：\n{literature_text}"
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
        os.makedirs(out_dir, exist_ok=True)
        
        # 保存到markdown文件
        md_path = os.path.join(out_dir, f"{filename}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(remaining_content)
        
        print("API分析完成：")
        print(output_content)
        print(f"\n✅ 分析结果已保存: {md_path}")
    except Exception as exc:
        print(f"分析失败: {exc}")



print("\n" + "=" * 60)
print(f"处理完成！共处理 {len(pdf_files)} 个PDF文件")
print(f"txt文本文件保存在: {txt_dir}")