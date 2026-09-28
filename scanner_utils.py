import cv2
import numpy as np

def make_edge_image(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_img = cv2.GaussianBlur(gray_img, (5,5), 0)
    edge_img = cv2.Canny(blur_img, 75, 200)
    return edge_img


def find_paper_contour(edge_img):
    contours, _ = cv2.findContours(edge_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    paper_contour = None

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx_shape = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx_shape) == 4:
            paper_contour = approx_shape
            break
    return paper_contour


def sort_corner_points(points):
    points = points.reshape((4,2))
    corner_list = np.zeros((4,2), dtype="float32")

    sum_xy = points.sum(axis=1)
    corner_list[0] = points[np.argmin(sum_xy)]  #左上
    corner_list[2] = points[np.argmax(sum_xy)]  #右下

    diff_xy = np.diff(points, axis=1)
    corner_list[1] = points[np.argmin(diff_xy)] #右上
    corner_list[3] = points[np.argmax(diff_xy)] #左下
    return corner_list


def fix_perspective(original_img, four_points):
    corners = sort_corner_points(four_points)
    top_left, top_right, bottom_right, bottom_left = corners

    
    width1 = np.sqrt(((bottom_right[0] - bottom_left[0])**2) + ((bottom_right[1] - bottom_left[1])**2))
    width2 = np.sqrt(((top_right[0] - top_left[0])**2) + ((top_right[1] - top_left[1])**2))
    max_width = max(int(width1), int(width2))

    height1 = np.sqrt(((top_right[0] - bottom_right[0])**2) + ((top_right[1] - bottom_right[1])**2))
    height2 = np.sqrt(((top_left[0] - bottom_left[0])**2) + ((top_left[1] - bottom_left[1])**2))
    max_height = max(int(height1), int(height2))

   
    target_corners = np.array([
        [0, 0],
        [max_width-1, 0],
        [max_width-1, max_height-1],
        [0, max_height-1]
    ], dtype="float32")

    
    transform_matrix = cv2.getPerspectiveTransform(corners, target_corners)
    fixed_img = cv2.warpPerspective(original_img, transform_matrix, (max_width, max_height))
    return fixed_img


def scan_paper(img_path, output_path):
    """主扫描函数：读取图片，矫正，生成扫描件"""
    img = cv2.imread(img_path)
    scale_ratio = img.shape[0] / 500.0
    original_copy = img.copy()
   
    small_img = cv2.resize(img, (int(img.shape[1]/scale_ratio), 500))

    edge_img = make_edge_image(small_img)
    paper_outline = find_paper_contour(edge_img)

    if paper_outline is None:
        print("⚠️ 找不到纸张轮廓，直接保存原图")
        cv2.imwrite(output_path, original_copy)
        return original_copy

   
    fixed_img = fix_perspective(original_copy, paper_outline.reshape(4,2)*scale_ratio)
   
    gray_fixed = cv2.cvtColor(fixed_img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray_fixed, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite(output_path, binary_img)
    print(f"✅ 扫描完成！输出文件：{output_path}")
    return binary_img
