import fitz  # PyMuPDF
import zipfile
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_pdf_to_zip(pdf_path, output_zip_path, dpi=300):
    """
    Chuyển đổi toàn bộ các trang của file PDF thành ảnh JPEG 
    và đóng gói trực tiếp vào một file ZIP mà không lưu ảnh tạm xuống đĩa.
    """
    # Mở file PDF
    doc = fitz.open(pdf_path)
    
    # Thiết lập độ phân giải
    zoom = dpi / 72  
    mat = fitz.Matrix(zoom, zoom)
    
    # Khởi tạo file ZIP để ghi dữ liệu
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Render trang thành pixmap (độ phân giải cao)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            # Chuyển đổi trực tiếp dữ liệu ảnh thành dạng bytes (JPEG) trong RAM
            img_data = pix.tobytes(output="jpg")
            
            # Định dạng tên file ảnh bên trong file ZIP
            # Bạn có thể đổi cấu trúc tên tùy ý (VD: PhieuDuThi_Trang_1.jpg)
            img_name = f"PhieuDuThi_Trang_{page_num + 1}.jpg"
            
            # Ghi trực tiếp mảng bytes ảnh vào file ZIP
            zipf.writestr(img_name, img_data)
            print(f"-> Đã nén thành công: {img_name}")
            
    print(f"=== ĐÃ TẠO FILE ZIP THÀNH CÔNG: {output_zip_path} ===")

def ThucHienChuyenDoiGUI():
    """
    Hàm tạo giao diện nút bấm (Upload/Save) để người dùng dễ thao tác
    """
    # 1. Hộp thoại "Upload" chọn file PDF đầu vào
    pdf_path = filedialog.askopenfilename(
        title="Chọn file PDF cần chuyển đổi",
        filetypes=[("PDF Files", "*.pdf")]
    )
    
    # Nếu người dùng tắt hộp thoại không chọn file
    if not pdf_path:
        return
        
    # Lấy tên file gốc để gợi ý tên file ZIP tương ứng
    file_name_without_ext = os.path.splitext(os.path.basename(pdf_path))[0]
    suggested_zip_name = f"{file_name_without_ext}_Images.zip"
    
    # 2. Hộp thoại "Save" chọn vị trí lưu file ZIP đầu ra
    output_zip_path = filedialog.asksaveasfilename(
        title="Chọn nơi lưu file ZIP",
        initialfile=suggested_zip_name,
        filetypes=[("ZIP Files", "*.zip")]
    )
    
    if not output_zip_path:
        return
        
    try:
        # Gọi hàm xử lý lõi
        convert_pdf_to_zip(pdf_path, output_zip_path, dpi=300)
        messagebox.showinfo("Thành công", "Đã chuyển đổi tất cả các trang và đóng gói thành file ZIP gọn gàng!")
    except Exception as e:
        messagebox.showerror("Lỗi hệ thống", f"Có lỗi xảy ra trong quá trình xử lý: {str(e)}")

# --- Khởi chạy ứng dụng thử nghiệm ---
if __name__ == "__main__":
    # Khởi tạo một cửa sổ giao diện giao tiếp ẩn để gọi hộp thoại chọn file
    root = tk.Tk()
    root.withdraw() 
    
    print("Đang mở giao diện chọn file...")
    # Chạy tính năng
    ThucHienChuyenDoiGUI()