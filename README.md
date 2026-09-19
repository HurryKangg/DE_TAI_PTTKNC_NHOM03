# Phân Tích Thống Kê Nhiều Chiều

## Đề tài: Đánh gíá đa chiều về đa chiều về mức độ hài lòng của sinh viên đại học theo khối ngành đào tạo

### 1 Mục tiêu yêu cầu

| Thành phần   | Yêu Cầu                                                                                                                         |
|--------------|---------------------------------------------------------------------------------------------------------------------------------|
| Mục Tiêu     | Kiểm tra xem có sự khác biệt mang ý nghĩa thống kê về mức độ hài lòng đa chiều giữa sinh viên hai khối ngành đào tạo hay không. |
| Kểm định     | Giả thuyết không ($H_0$): $\boldsymbol{\mu}_1 = \boldsymbol{\mu}_2$ (Vector kỳ vọng trung bình mức độ hài lòng giữa 2 khối ngành là như nhau).<br/>Giả thuyết đối ($H_1$): $\boldsymbol{\mu}_1 \neq \boldsymbol{\mu}_2$ (Tồn tại ít nhất một tiêu chí có sự khác biệt).                                                                                                                      |
| Mức ý nghĩa  | Mức ý nghĩa kiểm định: $\alpha = 0.05$.                                                                                             |

### 2. Thiết kế Vector biến ($p = 5$)
Dữ liệu khảo sát được tổng hợp thành 5 biến số định lượng phản ánh các khía cạnh dịch vụ giáo dục:

Phân loại Khối Ngành Đào Tạo ($g = 2$)

| Nhóm | Tên Khối Ngành | Mã Môn Học Quy Ước (`Ma so mon hoc`) | Quy mô mẫu ($n$) |
|:---:|---|---|:---:|
| **Nhóm 1** | **Kỹ thuật – CNTT** | Từ 1 đến 4 ($1 \le \text{code} \le 4$) | $n_1 = 50$ |
| **Nhóm 2** | **Kinh tế – Quản trị** | Từ 5 đến 9 ($5 \le \text{code} \le 9$) | $n_2 = 50$ |
| **Tổng** | **Mẫu chuẩn hóa làm sạch** | **Bộ dữ liệu sau tiền xử lý** | **$N = 100$** |

Vector $p = 5$ Biến Đánh Giá Mức Độ Hài Lòng

| Ký hiệu | Tên tiêu chí | Biến thành phần từ bảng khảo sát gốc | Thang đo |
|:---:|---|---|:---:|
| **$Y_1$** | **Chất Lượng Giảng Dạy** | Lắng nghe trong lớp, Thảo luận cải thiện hứng thú, Lớp học đảo ngược | $[1.0 - 5.0]$ |
| **$Y_2$** | **CSVC** | Loại hình chỗ ở tại Síp, Phương tiện đi lại đến trường | $[1.0 - 5.0]$ |
| **$Y_3$** | **Học Liệu Số** | Đọc sách phi KH, Đọc sách KH, Ghi chép, Ôn giữa kỳ 1, Ôn giữa kỳ 2 | $[1.0 - 5.0]$ |
| **$Y_4$** | **Việc Làm** | Công việc làm thêm, Tác động của dự án/hoạt động | $[1.0 - 5.0]$ |
| **$Y_5$** | **Ngoại Khóa** | Tham dự hội thảo chuyên ngành, Tham dự các lớp học | $[1.0 - 5.0]$ |
### 3. Khung phương pháp luận

| Công đoạn phân tích | Công thức toán học | Diễn giải ý nghĩa |
|---|:---:|---|
| **1. Ước lượng MLE** | ȳᵢ = (1/nᵢ) Σ yᵢⱼ | Vector trung bình mẫu đóng vai trò là ước lượng hợp lý cực đại cho vector kỳ vọng $\mu_i$ |
| **2. Hiệp phương sai gộp** | $S_p = \frac{(n_1 - 1)S_1 + (n_2 - 1)S_2}{n_1 + n_2 - 2}$ | Ước lượng ma trận hiệp phương sai chung từ hiệp phương sai mẫu $S_1$ và $S_2$ |
| **3. Thống kê Hotelling's $T^2$** | $T^2 = \frac{n_1 n_2}{n_1 + n_2} (\bar{y}_1 - \bar{y}_2)^T S_p^{-1} (\bar{y}_1 - \bar{y}_2)$ | Khoảng cách Mahalanobis bình phương giữa 2 vector trung bình |
| **4. Chuyển đổi phân phối $F$** | $F_{\text{stat}} = \frac{n_1 + n_2 - p - 1}{p(n_1 + n_2 - 2)} T^2$ | Quy đổi thống kê $T^2$ về phân phối $F(df_1, df_2)$ với $df_1 = p$, $df_2 = n_1 + n_2 - p - 1$ |
| **5. Tính $p$-value** | $p\text{-value} = P(F \ge F_{\text{stat}}) = \text{sf}(F_{\text{stat}}, df_1, df_2)$ | Xác suất xảy ra dữ liệu cực đoan hơn dưới giả định $H_0$ đúng |

### 4. Cấu trúc thư mục dự án
```text
Nhom03_PTTKNC
├── code
│   └── data_cleanning.py
├── data
│   ├── DATA.xlsx
│   ├── data_clean.csv
│   └── data_raw.csv
├── output
│   ├── chart
│   │   └── chart_data_cleanning.png
│   ├── statistical_data
│   │   ├── demo_CSVC.png
│   │   ├── demo_Chất Lượng Giảng Dạy.png
│   │   ├── demo_Học Liệu Số.png
│   │   ├── demo_Ngoại Khóa.png
│   │   └── demo_Việc Làm.png
├── report
└── README.md
```
### 5. Cài đặt và Hướng dẫn thực thi
Yêu cầu môi trường
Python 3.14.7 hoặc Python 3.9+ 64 bit

Kiểm tra phiên bản
```BASH
py --version
```
Cài đặt thư viện

Thư viện yêu cầu:
```BASH
pip install numpy, pandas, scipy, matplotlib, seaborn, statsmodels,openpyxl.
```

Kích hoạt chạy chương trình

1. Mở tệp giải pháp hoặc dự án demo.pyproj trong Visual Studio 2022.

2. Chọn môi trường Python (Python 3.9+ 64-bit).

3. Nhấn F5 hoặc nút Start để thực thi tệp code/data_cleanning.py.
```bash
python code/data_cleanning.py
```

Xem toàn bộ biểu đồ và tóm tắt thống kê tại thư mục output/.

### 6. Bảng Danh Mục Kết Quả Đầu Ra

| Loại kết quả | Đường dẫn tệp tin | Nội dung chi tiết |
|---|---|---|
| **Báo cáo dữ liệu** | `data/data_clean.csv` | Bảng dữ liệu sạch chuẩn hóa $N=100$ gồm mã sinh viên, khối ngành và 5 biến $Y_1 \dots Y_5$ |
| **Biểu đồ đường** | `../output/chart/chart_data_cleanning.png` | Đồ thị so sánh profile vector trung bình giữa Kỹ thuật – CNTT và Kinh tế – Quản trị |
| **Biểu đồ phân bố** | `../output/statistical_data/demo_*.png` | Bộ 5 biểu đồ Boxplot kết hợp phân tán điểm dữ liệu (Jitter) trực quan hóa từng tiêu chí |
| **Bảng điều khiển** | Màn hình Console | Hiển thị chi tiết: $n_1, n_2, p$, ma trận $S_p$, thống kê $T^2$, giá trị $F$, $p$-value và kết luận |

### Danh Sách Thành Viên Nhóm Thực Hiện

| STT | Mã Sinh Viên | Họ và Tên | Vai Trò | Nhiệm Vụ Phụ Trách | Đánh Giá (%) |
|:---:|:------------:|:----------|:-------:|:-------------------|:------------:|
| 01 | 2045250095 | Huỳnh Võ Anh Khang | Trưởng nhóm | Quản lý dự án, Code fix mã nguồn data,soạn văn bản README.md,kết luận và đưa ra nhận xét | 17% |
| 02 | 2045250199 | Tăng Thành Trí | Thành viên | Xử lý tổng hợp nội dung để báo cáo word | 17% |
| 03 | 2045250066 | Nguyễn Minh Hiền | Thành viên | Tóm tắt và giới thiệu đề tài báo cáo dữ liệu và thiết kế phân tích | 16% |
| 04 | 2045250061 | Liêu Hồ Gia Hân | Thành viên | Kết quả nghiên cứu thông qua phân tích dữ liệu | 17% |
| 05 | 2045250156 | Lý Hữu Phước | Thành viên | Code mô phỏng data xử lý hệ thống nguồn data_clean, vẽ biểu đồ và số liệu thống kê  | 17% |
| 06 | 2045250187 | Trần Minh Thông | Thành viên | Phương pháp nghiên cứu thống kê trực quan hệ thống phân tích dữ liệu | 16% | 