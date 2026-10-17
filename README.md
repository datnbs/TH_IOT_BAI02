# TH_IOT_BAI02

# Bai 1 - Gửi và nhận message bằng AMQP

## 1. Mục tiêu
Xây dựng ứng dụng Python sử dụng thư viện Pika
để gửi và nhận message qua RabbitMQ Cloud.

## 2. Môi trường
- Python 3.x
- pika
- RabbitMQ Cloud
- VS Code

Cài đặt thư viện:

```bash
pip install pika
```

## 3. Cấu hình kết nối
Thiết lập biến môi trường CLOUDAMQP_URL chứa
URL kết nối RabbitMQ Cloud.

PowerShell:

```powershell
$env:CLOUDAMQP_URL = "URL_KET_NOI_CUA_BAN"
```

Không chia sẻ URL chứa thông tin đăng nhập.

## 4. Cách chạy

Mở terminal thứ nhất:

```bash
python consumer_bai1.py
```

Mở terminal thứ hai:

```bash
python producer_bai1.py
```

Nhập họ tên và mã sinh viên theo yêu cầu.

## 5. Kết quả
- Producer kết nối tới RabbitMQ Cloud.
- Producer gửi message vào queue iot_lab_queue.
- Consumer nhận message và in nội dung.
- Consumer hiển thị thời điểm nhận message.

## 6. Các file nộp
- producer_bai1.py
- consumer_bai1.py
