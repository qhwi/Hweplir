### ❔ **/help** (*command*)

Hiển thị list tên các command

Parameter:
- `command` (Optional): Chọn 1 command bất kì để xem kĩ thông tin

## 1. [CTFTime] Commands

Prefix: `/ct-`

### 🔎 **/ct-info_find** (*search-key*)

Tra cứu thông tin một giải CTF bất kì trên CTFTime

Parameter:
- `search-key` (str): CTFtime ID hoặc tên của một CTF chưa diễn ra cần tìm

### 🔎 **/ct-info_ongo**

Xem tóm tắt thông tin các giải CTF **đang** diễn ra trên CTFTime

### 🔎 **/ct-info_upco** (*page = 1*, *step = 3*)

Xem tóm tắt thông tin các giải CTF **sắp** diễn ra trên CTFTime

Parameters:
- `page` (Optional[int]): Chuyển số trang
- `step` (Optional[int]): Tuỳ chỉnh số kết quả hiện trên mỗi trang

### 🚩 **/ct-reg** (*ctftime-id*)

Tạo category thảo luận cho một giải CTF mới trên CTFTime

*Note: Category thảo luận sẽ bị ẩn sau 2 tuần từ khi kết thúc CTF*

Parameter:
- `ctftime-id` (int): ID giải CTF trên CTFTime

VD: `https://ctftime.org/event/1000` -> `ctftime-id = 1000`

### 🚩 **/ct-regacc** (*username*, *password*, *cate_id*)

Update thông tin tài khoản CTF đã tạo, để chia sẻ account cho mọi người cùng tham gia

Parameters:
- `username` (str): Tên đăng nhập của account đã tạo
- `password` (str): Mật khẩu của account đã tạo
- `cate_id` (Optional[int]): ID của Category thảo luận của giải CTF tương ứng trong Server [Hoặc bỏ qua nếu đang gọi command trong đúng Category đó]  

## 2. [CTF Chung] Commands

Prefix: `/c-`

### 📃 **/c-list** (*order = 'Mới nhất'*, *page = 1*, *step = 5*)

List tất cả các giải CTF đã tạo trong Server

Parameters:
- `order`: Thứ tự xếp list - 'Mới nhất' (default) hoặc 'Cũ nhất'
- `page` (Optional[int]): Chuyển số trang
- `step` (Optional[int]): Tuỳ chỉnh số kết quả hiện trên mỗi trang

### 👁 **/c-view** (*ctf-name*)

Toggle ẩn/hiện Category thảo luận của một giải CTF trong Server

*Note: Để xem danh sách các giải trong Server, hãy dùng `/c-list`*

Parameter:
- `ctf-name` (discord.Role): Chọn role CTF cần thêm (VD: "<BKCTF 2023>") 

## 3. [Admin] Commands

Prefix: `/admin-`

*Note: Các command này nên được thêm Permission Override trong Setting của server, để chỉ cho phép một số người sử dụng.*

### 🚩 **/admin-reg_special** (*name*, *hide_after*)

Tạo Category thảo luận thủ công cho một giải CTF (không trên CTFTime)

*Note: Category thảo luận sẽ bị ẩn `hide_after` ngày từ khi tạo.*

Parameters:
- `name` (str): Tên của giải CTF muốn tạo
- `hide_after` (int): Số ngày trước khi auto ẩn category

### ❌ **/admin-delete** (*search_id*)

Xoá một giải CTF đã tạo trong server

*Note: Có thể xoá tất cả dữ liệu, hoặc chỉ xoá Role và dữ liệu trong `ctf.json` nhưng giữ lại Category thảo luận.*

Parameter:
- `search_id` (str): CTFTime ID hoặc ID của Category thảo luận

### ➕ **/admin-add** (*cate_id*)

Thêm vào List `ctf.json` (và tạo Role xem) cho category thảo luận của một giải CTF bất kì

Parameter:
- `cate_id` (Optional[int]): ID của Category thảo luận của giải CTF tương ứng trong Server [Hoặc bỏ qua nếu đang gọi command trong đúng Category đó]

### 👁 **/admin-hide**

Ẩn Category thảo luận của các CTF cũ ngay lập tức [autorun cùng /reg]