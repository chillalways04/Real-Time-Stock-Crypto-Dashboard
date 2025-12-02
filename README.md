# 📈 Real-Time Stock & Crypto Dashboard

Dashboard แบบโต้ตอบสำหรับดูราคาหุ้นและคริปโตแบบ **Real-Time Simulation**  
สร้างด้วย **Python + Streamlit + yfinance + Plotly** พร้อม UI สวยงามใช้งานง่าย

---

## 🖼️ Demo / Screenshots

> *(เพิ่มรูปในโฟลเดอร์ `screenshots/` แล้วแก้ชื่อไฟล์ตามต้องการ)*

![Dashboard Overview](screenshots/dashboard_overview.png)
![Volume & Summary](screenshots/dashboard_volume_summary.png)

---

## 🚀 Features

### 🔍 รองรับทั้ง Stocks และ Crypto
- เลือก Symbol หลายตัวพร้อมกัน เช่น `AAPL`, `NVDA`, `META`, `BTC-USD`
- ปรับช่วงเวลาได้: **1M, 3M, 6M, 1Y, Custom**

### 📊 Visualization แบบจัดเต็ม
- 📉 **Price Line Chart** (Zoom / Hover / Multi-Symbol)
- 📊 **Volume Bar Chart**
- 🔢 **KPI Metrics** (Last Close & % Change)
- 📋 **Summary Table** (แสดงผลราคาและ Volume ช่วงเวลาที่เลือก)

### ⚙️ ฟีเจอร์ด้าน Performance
- ทำงานเร็วด้วย `@st.cache_data(ttl=300)`
- โหลดข้อมูลจาก Yahoo Finance ทุกครั้งที่ผู้ใช้เปลี่ยนตั้งค่า
- รองรับ **Log scale** สำหรับราคาที่ต่างกันมาก

---

## 🧰 Tech Stack

| Layer        | Technology                     |
|-------------|---------------------------------|
| Frontend UI | Streamlit                       |
| Backend     | Python                          |
| Charting    | Plotly Express                  |
| Data Engine | Pandas, NumPy                   |
| Data Source | yfinance (Yahoo Finance API)    |

---

## 📂 Project Structure

```txt
StockPy/
│
├── stock.py               # Streamlit main app
├── README.md              # Documentation
├── requirements.txt       # Dependencies
│
└── screenshots/
    ├── dashboard_overview.png
    ├── dashboard_volume_summary.png
