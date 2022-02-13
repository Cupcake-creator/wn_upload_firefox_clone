# Login ก่อนจึงจะอัพโหลดได้

superuser id: admin
superuser password: admin1234

การทำงาน Background
- process ในการลบไฟล์ เมื่อมีไฟล์ expire ใน database จะถูกเรียกใช้ทุกๆ 90 นาที
- ลบไฟล์ทันทีเมื่อ max_downloads < 0 หรือ expire_date < datetime.now()
- ผู้ใช้ที่ไม่ใช่ผู้อัพโหลดไม่สามารถลบไฟล์ได้
- ถ้ารหัสถูกสามารถ download ได้ทันที

Docker command
1. docker build -t send .
2. docker compose up