import os
import glob
from pypdf import PdfReader

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

def extract_save(pdf_file, pdf_name, pdf_stem, txt_path, save = True):
    print(f"\n 提取并分析: {pdf_name}")

    # 本地提取PDF文本
    full_text = extract_pdf_text(pdf_file)
    if not full_text:
        print("提取文本失败或为空，跳过")
        return
    print(f"提取成功，文本长度: {len(full_text)} 字符")

    # 保存到txt文件
    if save:
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"文本已保存: {txt_path}")

    return full_text
 