# 📈 Real-Time Stock & Crypto Dashboard

Dashboard แบบโต้ตอบสำหรับดูราคาหุ้นและคริปโตแบบ **Real-Time Simulation**  
สร้างด้วย **Python + Streamlit + yfinance + Plotly** พร้อม UI สวยงามใช้งานง่าย

---

## Data visualization


![Dashboard Overview](screenshots/dashboard_overview.png)
![Volume & Summary](screenshots/dashboard_volume_summary.png)

---

## 🚀 Features

### 🔍 รองรับทั้ง Stocks และ Crypto
- เลือก Symbol หลายตัวพร้อมกัน เช่น `AAPL`, `NVDA`, `META`, `BTC-USD`
- ปรับช่วงเวลาได้: **1M, 3M, 6M, 1Y, Custom**

### 📊 Visualization 
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



# ⚙️ Installation & Setup & How it Works
* Clone repository
 git clone https://github.com/your-username/StockPY.git cd StockPY

--- 


## (แนะนำ) สร้าง virtual environment
    python -m venv venv

## Windows:
    venv\Scripts\activate

## Run application
    streamlit run stock.py
* เปิดเบราว์เซอร์:
#### http://localhost:8501


## 🧠 How It Works
  #### 1. ดึงข้อมูลตลาดผ่าน yfinance (OHLCV)
* Close Price
* Volume
* Auto Adjust (ปรับตาม dividend/split)
ข้อมูลถูก cache ไว้ 5 นาทีเพื่อความเร็ว 

#### 2. แปลงข้อมูลสำหรับ Plotly

* ข้อมูลถูกแปลงจาก wide → long format:

        | Date | Symbol | Close | Volume |

        เหมาะสำหรับ line chart และ bar chart

####  3. แสดง KPI (Period Change)

คำนวณ:

    %Change = (Last Close - First Close) / First Close * 100
แล้วแสดงผ่าน st.metric

#### 4. สร้างกราฟแบบ Interactive

📉 Price Chart
        
* ulti-symbol

 * Hover shows price & volume

* รองรับ Log scale

📊 Volume Chart

* Grouped bars per date

* เปรียบเทียบระหว่าง Symbol ได้ดีมาก

## 📋 Summary Table
แสดงข้อมูลสุดท้ายของช่วงเวลาที่เลือก:

* Last Close

* Change %

* Last Volume

* Last Date

## 📡 API & Data Source

ใช้ข้อมูลจาก Yahoo Finance ผ่านไลบรารี:

    yfinance

ดึงข้อมูล OHLCV ทุกครั้งที่ผู้ใช้เปลี่ยน Symbol หรือช่วงเวลา


## 📝 Requirements
    streamlit
    yfinance
    pandas
    numpy
    plotly

## 📜 License

##### This project is released under the MIT License.
You are free to use, modify, and distribute this project.


## 📂 Project Structure

```txt
StockPy/
│
├── stock.py               # Streamlit main app
├── README.md              # Documentation
│
└── screenshots/
    ├── dashboard_overview.png
    ├── dashboard_volume_summary.png











