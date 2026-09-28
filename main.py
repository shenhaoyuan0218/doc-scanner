from scanner_utils import scan_paper
import os

def main():
    print("===== 简易文档扫描仪（CV项目） =====")
    image_path = input("请输入图片路径：")
    if not os.path.exists(image_path):
        print("错误：文件不存在！")
        return
    output_file = "scanned_result.jpg"
    scan_paper(image_path, output_file)

if __name__ == "__main__":
    main()
