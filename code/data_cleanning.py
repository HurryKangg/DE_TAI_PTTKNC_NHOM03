from genericpath import exists
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
from scipy.stats import f
import turtle as t
import os ,sys

from pandas.core.reshape import encoding
from statsmodels.multivariate.manova import MANOVA
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# ==============================================================================
# HỆ THỐNG BẢNG MÀU DARK NEON (CYBERPUNK MODERN DASHBOARD)
# ==============================================================================
BG_COLOR       = "#0b0e14"
PANEL_BG       = "#151922"
CARD_BG        = "#1e2430"
BORDER_DEFAULT = "#2d3545"

COLOR1       = "#25A2DC"  # Cyan
COLOR2       = "#4ade80"  # Lime Green
COLOR3       = "#c084fc"  # Tím Neon
COLOR4       = "#f43f5e"  # Hồng Đỏ
COLOR5       = "#fb923c"  # Cam Neon
COLOR6       = "#facc15"  # Vàng Neon
COLOR7       = "#64748b"  # Màu dây bus ngầm

TEXT_MAIN      = "#f8fafc"
TEXT_MUTED     = "#94a3b8"

#==========================================================================================
#BƯỚC 1: ĐỌC FILE
#==========================================================================================

# 1. Cấu hình đường dẫn đọc file và xuất kết quả
ROOT = Path("../data/DATA.xlsx")
try:
    if not os.path.exists(ROOT.resolve()):
        print(f"FILE: Không tồn tại {ROOT.resolve()}")
        sys.exit(1)
    thoat_file = os.path.splitext(ROOT.resolve())[0].lower()
    try:
        if thoat_file == ".csv":
            df = pd.read_csv(ROOT.resolve(), encoding="utf-8", sep=";")
        else:
            df = pd.read_excel(ROOT, sheet_name="DATA GỐC")
            df.column = df.column.str.strip() # Loại bỏ khoảng trắng
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")

except FileNotFoundError:
    print("Không tìm thấy file: ", ROOT.resolve())
    sys.exit(1)

# Kiểm tra sự tồn tại của file trước khi đọc
if not ROOT.exists():
    raise FileNotFoundError(f"Không tìm thấy file tại: {ROOT.resolve()}")

# Thiết lập thư mục outputs
OUT_DIR = Path("../output") if len(ROOT.parts) > 1 and ROOT.parts[0] == ".." else Path("output")
CHART_DIR = OUT_DIR / "chart"
STAT_DIR = OUT_DIR / "statistical_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG = OUT_DIR  # Gán thư mục lưu hình ảnh để tránh lỗi NameError

# 2. Đọc và tiền xử lý dữ liệu
if not ROOT.exists(): #Kểm tra không đọc file trong dữ liệu được
    np.random.seed(42)
    n_sample = 120
    df = pd.DataFrame({
        "STUDENT_ID": [f"SV{i:03d}" for i in range(1, n_sample + 1)],
        "Ma so mon hoc": np.random.choice(range(1, 10), n_sample),
        "Lang nghe trong lop hoc": np.random.uniform(2.5, 5.0, n_sample),
        "Thao luan giup cai thien hung thu": np.random.uniform(2.5, 5.0, n_sample),
        "Lop hoc dao nguoc": np.random.uniform(2.0, 5.0, n_sample),
        "Loai hinh cho o tai Sip": np.random.uniform(2.0, 4.5, n_sample),
        "Phuong tien di lai den truong dai hoc": np.random.uniform(2.0, 4.5, n_sample),
        "Tan suat doc sach phi khoa hoc": np.random.uniform(1.5, 4.0, n_sample),
        "Tan suat doc sach khoa hoc": np.random.uniform(2.0, 4.5, n_sample),
        "Ghi chep trong lop hoc": np.random.uniform(2.5, 5.0, n_sample),
        "Chuan bi ky thi giua ky 1": np.random.uniform(2.0, 5.0, n_sample),
        "Chuan bi ky thi giua ky 2": np.random.uniform(2.0, 5.0, n_sample),
        "Cong viec lam them": np.random.uniform(1.5, 4.0, n_sample),
        "Tac dong cua du an/hoat dong": np.random.uniform(2.0, 4.5, n_sample),
        "Tham du hoi thao chuyen nganh": np.random.uniform(1.5, 4.5, n_sample),
        "Tham du cac lop hoc": np.random.uniform(2.5, 5.0, n_sample),
    })
else:
    df = pd.read_excel(ROOT, sheet_name="DATA GỐC")
df.columns = df.columns.str.strip()

#==========================================================================================
#BƯỚC 2: CÀI ĐẶT CÁC THUỘC TÍNH
#==========================================================================================
varr_x1 =[
    'Lang nghe trong lop hoc',
    'Thao luan giup cai thien hung thu',
    'Lop hoc dao nguoc'
]
df['Chất Lượng Giảng Dạy'] = df[varr_x1].mean(axis=1) #chia theo hàng ngang

varr_x2 =[
    'Loai hinh cho o tai Sip',
    'Phuong tien di lai den truong dai hoc'
]
df['CSVC'] = df[varr_x2].mean(axis=1)

varr_x3 =[
    'Tan suat doc sach phi khoa hoc',
    'Tan suat doc sach khoa hoc',
    'Ghi chep trong lop hoc',
    'Chuan bi ky thi giua ky 1',
    'Chuan bi ky thi giua ky 2'
]
df['Học Liệu Số'] = df[varr_x3].mean(axis=1)

varr_x4 =[
    'Cong viec lam them',
    'Tac dong cua du an/hoat dong'
]
df['Việc Làm'] = df[varr_x4].mean(axis=1)

varr_x5 =[
    'Tham du hoi thao chuyen nganh',
    'Tham du cac lop hoc'
]
df['Ngoại Khóa'] = df[varr_x5].mean(axis=1)

#==========================================================================================
#BƯỚC 3: KIỂM TRA VÀ TÍNH TOÁN ƯỚC LƯỢNG MLE VÀ KIỂM ĐỊNH HOTELLING T2
#==========================================================================================

#Phân lối khối ngành   #def dùng để định nghĩa hàm
def Khoi_Nganh(ma_so_mon_hoc):
    if 1 <= ma_so_mon_hoc <= 4:
        return "CNTT - Kỹ Thuật"
    elif 5 <= ma_so_mon_hoc <= 9:
         return "Quản Trị - Kinh Tế"
    else:
        return "Khác"
df["Khối Ngành"] = df['Ma so mon hoc'].apply(Khoi_Nganh)

#Tính ước lượng MLE vector trung bình của sinh viên
varr_x6 = [
   'Chất Lượng Giảng Dạy',
   'CSVC',
   'Học Liệu Số',
   'Việc Làm',
   'Ngoại Khóa'
]
#gourpby nhóm dữ liệu (Khối Ngành) theo cột phân loại
mle_vtr =(df.groupby("Khối Ngành")[varr_x6].mean().round(2))
print("\n--- Ước Lượng MLE vector Trung Bình Của Từng Khối Ngành ---")
print(mle_vtr)

#Kiểm định Hotelling’s T2
#1. khối CNTT - Kỹ Thuật
#2. khối Quản Trị - Kinh Tế
#Tách dữ liệu từng khối ngành thành ma trận
#values chuyển dataframe thành ma trận
nhom_cntt = df[df["Khối Ngành"] == "CNTT - Kỹ Thuật"][varr_x6].values
nhom_quantri = df[df["Khối Ngành"] == "Quản Trị - Kinh Tế"][varr_x6].values

#.shape trả về dạng cặp (số dòng , số cột)
# n1, p là số dòng + số biến của cntt
# n2, _ là số dòng của khoa quantri và _ có nghĩa là p của quantri = p cntt (=5)
n1, p = nhom_cntt.shape
n2, _ = nhom_quantri.shape

#Tính vector trung bình mẫu của hai khối ngành (x1,x2)
#y ngang giá trị trung bình
#axis = 0 chia theo hàng dọc
y1 = np.mean(nhom_cntt, axis=0)
y2 = np.mean(nhom_quantri, axis = 0)

#Tính ma trận hiệp phương sai S_p
#rowvar = False: mỗi cột là p biến, mỗi dòng là n quan sát
#rowvar = True : mỗi cột là n quan sát , mỗi dòng là p biến
#N - g = n1 + n2 - 2
s1 = np.cov(nhom_cntt, rowvar = False)
s2 = np.cov(nhom_quantri, rowvar = False)
#Công thức tính Sp
E = ((n1 - 1) * s1 + (n2 - 1) * s2)
S_p = E / (n1 + n2 - 2)

#Tính khoảng cách Hotelling T2
#diff là sự chênh lệch giữa cntt (y1) và quantri(y2)
#np.linalg.inv(S_p) tìm ma trận khả nghịch của S_P
#diff.T là chuyển vị
# @ là phép nhân hai ma trận

diff = y1 - y2
T2 = float((n1 * n2) / (n1 + n2)) * float(diff.T @ np.linalg.inv(S_p) @ diff)

# Chuyển đổi T2 sang F và giá trị p-value
#f.cdf tinh xac suat tu diem 0 di len
df1 = p
df2 = n1 + n2 - p - 1
F_stat = ((n1 + n2 - p - 1) / (p*(n1 + n2 - 2))) *T2
p_value = 1 - float(f.cdf(F_stat, df1, df2))

#In Kết Quả
print("\n ---Kiểm Định Hotelling T2 Cho 2 Khối Ngành---")
print(f"Thống kê T2:  {T2:.4f}")
print(f"Giá trị F  :  {F_stat:.4f}")
print(f"p-value    :  {p_value:.5} (p < 0.001)")
if p_value < 1e-4:
    print(f"p-value    :  {p_value:.4e} (p < 0.001)")
else:
    print(f"p-value    :  {p_value:.4f}")

if p_value < 0.05:
    print("\nCó sự khác biệt thống kê giữa vector trung bình của 2khối ngành\n")
else:
    print("\nKhông đủ bằng chứng để bác bỏ giải thuyết vector trung bình của 2 khối ngành giống nhau\n")



# Chỉ hiển thị các cột cần xem
cot_hien_thi = (
    ['STUDENT_ID']
    + ['Khối Ngành']
    + ['Chất Lượng Giảng Dạy']
    + ['CSVC']
    + ['Học Liệu Số']
    + ['Việc Làm']
    + ['Ngoại Khóa']
)

print(df[cot_hien_thi].round(2).head(3)) #round(2) làm tròn 2 số sau dấu phẩy
print(df[cot_hien_thi].round(2).tail(3))

# ==============================================================================
# BƯỚC 4: XUẤT ĐỒ THỊ MATPLOTLIB VÀ FILE CSV SẠCH
# ==============================================================================
khoi_nganh = ["CNTT - Kỹ Thuật", "Quản Trị - Kinh Tế"]
set_color = {"CNTT - Kỹ Thuật": COLOR1, "Quản Trị - Kinh Tế": COLOR5}
mle_T = mle_vtr.T

# Biểu đồ đường
fig, ax = plt.subplots(figsize=(7.2, 4.5))
for kn in khoi_nganh:
    if kn in mle_T.columns:
        ax.plot(varr_x6, mle_T[kn].to_numpy(), marker="o", label=kn, color = set_color[kn], linewidth = 2.2, markersize = 6)
ax.set_ylabel("Điểm đánh giá")
ax.set_xlabel("Tiêu chí")
ax.set_title("So Sánh Vector Trung Bình Giữa 2 Khối Ngành")
ax.legend()
plt.xticks(rotation=15)
fig.tight_layout()
fig.savefig(CHART_DIR / "chart_data_cleanning.png", dpi=180)  # Sửa đường dẫn lưu trực tiếp vào CHART_DIR
plt.close(fig)

# Biểu đồ Boxplot + Jitter
for x in varr_x6:
    fig, ax = plt.subplots(figsize=(6.4, 4.4))

    val_cntt = df.loc[df['Khối Ngành'].eq("CNTT - Kỹ Thuật"), x].dropna().to_numpy()
    val_qtkt = df.loc[df['Khối Ngành'].eq("Quản Trị - Kinh Tế"), x].dropna().to_numpy()
    data_plot = [val_cntt, val_qtkt]

    #Vẽ 2 khung bên CNTT = Xanh, QT = Cam
    bp = ax.boxplot(data_plot, tick_labels=khoi_nganh, patch_artist=True)

    palette = [COLOR1, COLOR5]

    for patch, color in zip(bp['boxes'], palette):
        patch.set_facecolor(color)
        patch.set_alpha(0.35)
        patch.set_edgecolor(color)
        patch.set_linewidth(1.5)

    for median in bp['medians']:
        median.set_color("black")
        median.set_linewidth(1.5)

    jitter1 = np.linspace(-0.08,0.08, len(val_cntt))
    ax.scatter(np.full(len(val_cntt), 1) + jitter1, val_cntt, alpha=0.6, color=COLOR1, edgecolors="none")


    jitter2 = np.linspace(-0.08,0.08, len(val_qtkt))
    ax.scatter(np.full(len(val_qtkt), 2) + jitter2, val_qtkt, alpha=0.6, color=COLOR5, edgecolors="none")
    ax.set_title(f"Phân Bố Tiêu Chí: {x}")
    ax.set_ylabel("Thông số")
    fig.tight_layout()
    safe_name = x.replace(" ", "_")
    fig.savefig(STAT_DIR / f"demo_{safe_name}.png", dpi=180)  # Sửa đường dẫn lưu trực tiếp vào STAT_DIR
    plt.close(fig)

# Xuất tệp CSV sạch
cot_co_san = [c for c in cot_hien_thi if c in df.columns]
DATA_DIR = Path("../data") if len(ROOT.parts) > 1 and ROOT.parts[0] == ".." else Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
clean_file = DATA_DIR / "data_clean.csv"
df[cot_co_san].round(2).to_csv(clean_file, index=False, encoding="utf-8-sig")
print(f"[XUẤT TỆP] Đã lưu thành công: {clean_file.resolve()}")

# ==============================================================================
# BƯỚC 5: XÂY DỰNG GIAO DIỆN TURTLE DASHBOARD HIỆN ĐẠI
# ==============================================================================
man_hinh = t.Screen()
man_hinh.setup(width=1120, height=750)
man_hinh.title("BẢNG ĐIỀU KHIỂN PHÂN TÍCH ĐA BIẾN - HOTELLING'S T²")
man_hinh.bgcolor(BG_COLOR)
t.tracer(0)

pen = t.Turtle()
pen.hideturtle()
pen.speed(3)
pen.penup()

def draw_card(x, y, w, h, bgcolor, border_color=None, border_width=1):
    """Vẽ Card hình chữ nhật chuẩn xác theo chiều rộng w và chiều cao h."""
    pen.goto(x, y)
    pen.color(border_color if border_color else bgcolor, bgcolor)
    pen.width(border_width)
    pen.pendown()
    pen.begin_fill()
    for _ in range(2):
        pen.forward(w)
        pen.right(90)
        pen.forward(h)
        pen.right(90)
    pen.end_fill()
    pen.penup()
# 1. Header Banner
draw_card(-520, 340, 1040, 80, PANEL_BG, BORDER_DEFAULT, 2)
pen.goto(-500, 305)
pen.color(COLOR1)
pen.write("HỆ THỐNG ĐÁNH GIÁ ĐA CHIỀU MỨC ĐỘ HÀI LÒNG SINH VIÊN", font=("Segoe UI", 16, "bold"))
pen.goto(-500, 278)
pen.color(TEXT_MUTED)
pen.write("Mô hình kiểm định Hotelling's T² • Ước lượng hợp lý cực đại (MLE) • Vector p = 5 chiều", font=("Segoe UI", 11, "normal"))

# 2. Card Trái: Kết Quả Thống Kê & Kiểm Định
draw_card(-520, 235, 490, 520, CARD_BG, BORDER_DEFAULT, 1)
pen.goto(-500, 205)
pen.color(COLOR6)
pen.write("THỐNG KÊ MA TRẬN & KIỂM ĐỊNH T²", font=("Segoe UI", 13, "bold"))

stats_info = [
    (f"Cỡ mẫu nhóm CNTT - Kỹ Thuật (n1): {n1}", TEXT_MAIN),
    (f"Cỡ mẫu nhóm Quản Trị - Kinh Tế (n2): {n2}", TEXT_MAIN),
    (f"Số biến phản hồi quan sát (p): {p}", TEXT_MAIN),
    (f"Bậc tự do (df1, df2): ({df1}, {df2})", TEXT_MUTED),
    (f"Thống kê Hotelling's T²: {T2:.4f}", COLOR1),
    (f"Giá trị F quan sát: {F_stat:.4f}", COLOR1),
    (f"p-value: {p_value:.4e}" if p_value < 1e-4 else f"p-value: {p_value:.4f}", COLOR2 if p_value < 0.05 else COLOR4),
]

curr_y = 165
for line, color in stats_info:
    pen.goto(-500, curr_y)
    pen.color(color)
    pen.write(line, font=("Consolas", 11, "normal"))
    curr_y -= 28

# Hộp kết luận thống kê
is_diff = p_value < 0.05
status_color = COLOR2 if is_diff else COLOR4
draw_card(-500, -50, 450, 110, PANEL_BG, status_color, 2)
pen.goto(-480, -95)
pen.color(status_color)
pen.write("KẾT LUẬN: " + ("BÁC BỎ H0 (CÓ Ý NGHĨA THỐNG KÊ)\n" if is_diff else "CHẤP NHẬN H0"), font=("Segoe UI", 11, "bold"))

pen.goto(-480, -140)
pen.color(TEXT_MAIN)
conclusion_desc = (
    "Có sự khác biệt ý nghĩa thống kê về mức độ hài lòng\ngiữa hai khối ngành đào tạo (p < 0.05)."
    if is_diff
    else "Không đủ bằng chứng để kết luận có sự khác biệt\nvề mức độ hài lòng giữa hai khối ngành (p >= 0.05)."
)
pen.write(conclusion_desc, font=("Segoe UI", 10, "normal"))

pen.goto(-500, -220)
pen.color(COLOR7)
pen.write(f"• Dữ liệu sạch: {clean_file.resolve()}", font=("Segoe UI",7, "italic"))
pen.goto(-500, -245)
pen.write("• Biểu đồ: output/chart/ & output/statistical_data/", font=("Segoe UI", 7, "italic"))

# 3. Card Phải: Trực Quan Hóa Profile MLE (Bar Chart Kép)
draw_card(-10, 235, 530, 520, CARD_BG, BORDER_DEFAULT, 1)
pen.goto(15, 205)
pen.color(COLOR3)
pen.write("SO SÁNH PROFILE ĐIỂM TRUNG BÌNH (MLE)", font=("Segoe UI", 13, "bold"))

labels = ["Giảng Dạy", "CSVC", "Học Liệu", "Việc Làm", "Ngoại Khóa"]
bar_y = 145

for idx, label in enumerate(labels):
    pen.goto(15, bar_y)
    pen.color(TEXT_MAIN)
    pen.write(label, font=("Segoe UI", 10, "bold"))

    val_cntt = y1[idx]
    val_kt = y2[idx]

    # Thanh màu CNTT (Cyan)
    draw_card(115, bar_y + 12, int(val_cntt * 60), 12, COLOR1)
    pen.goto(125 + int(val_cntt * 60), bar_y + 1)
    pen.color(COLOR1)
    pen.write(f"{val_cntt:.2f}", font=("Consolas", 9, "bold"))

    # Thanh màu Quản Trị - Kinh Tế (Hồng Neon)
    draw_card(115, bar_y - 6, int(val_kt * 60), 12, COLOR4)
    pen.goto(125 + int(val_kt * 60), bar_y - 17)
    pen.color(COLOR4)
    pen.write(f"{val_kt:.2f}", font=("Consolas", 9, "bold"))

    bar_y -= 65

# Chú thích màu biểu đồ
draw_card(115, -235, 18, 12, COLOR1)
pen.goto(140, -235)
pen.color(TEXT_MAIN)
pen.write("CNTT - Kỹ Thuật", font=("Segoe UI", 10, "normal"))

draw_card(300, -235, 18, 12, COLOR4)
pen.goto(325, -235)
pen.color(TEXT_MAIN)
pen.write("Quản Trị - Kinh Tế", font=("Segoe UI", 10, "normal"))

# Cập nhật hiển thị lên cửa sổ
t.update()
print("[HOÀN THÀNH] Toàn bộ tác vụ và giao diện Turtle đã hiển thị thành công!")

# Hàm xuất Data ra file CSV
# Khai bán hàm để xuất data ra file csv
def export_file_csv(data_frame, file_path="demo.csv", columns=None):
    try: #Kiểm tra lỗi nếu có thì chuyển xuống except
        if columns is not None: #Nếu có, lấy các cột nằm trong columns
            export_df = data_frame[columns]

        else: #Nếu không lấy toàn bộ cột
            export_df = data_frame

        export_df = export_df.round(2) #Làm tròn các cột 2 số sau dấu phẩy

        # index=False: không xuất số thứ tự
        # encoding ="utf-8-sig": hiển thị tiếng Việt
        # sep=",": ngăn cách các cột bằng dấu ,
        export_df.to_csv(file_path, index = False, encoding ="utf-8-sig", sep = ",")
        print(f"Đã xuất thành công file CSV {file_path}")

    # Hiển thị lỗi nếu file xuất không được
    except Exception as e:
        print(f"Xuất file không thành công: {e}")

# Gọi hàm để lấy các cột cần xem
export_file_csv(df,file_path="../data/data_clean.csv", columns = cot_hien_thi)

#Xuất ra màn hình
t.done()
