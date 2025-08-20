<<<<<<< HEAD
# **RucRut - Intelligent Recruitment Optimization System**

## **Overview**
RucRut is an advanced AI-powered recruitment system designed to enhance and streamline the hiring process for both **job providers** and **candidates**. The platform leverages cutting-edge **Natural Language Processing (NLP)** and **AI models** to generate tailored interview questions based on the candidate’s CV and job requirements, automatically evaluate their responses, and provide comprehensive feedback.

This system is built using **Flask**, **SQLAlchemy**, **MongoDB**, and **Hugging Face's NLP models**, with a focus on offering efficient, bias-reducing, and personalized recruitment experiences.

---

## **Video Walkthrough**

[Click here to watch the video walkthrough](https://drive.google.com/file/d/103M12Ok-hC81KZHVV7FvGC586wEa_KKX/view?usp=sharing)

> *(This video explains how the application works)*

---

## **Features**

### **For Job Providers**
- **Dashboard**: Manage job postings and track candidate applications in real-time.
- **Job Posting Creation**: Create and modify job postings with detailed specifications.
- **AI-Generated Interview Questions**: Automatically generate interview questions based on candidate CV and job description.
- **Automatic Feedback and Scoring**: Receive AI-driven feedback and score candidates based on their interview responses.
- **Analytics and Reports**: View candidate performance metrics through various graphs, such as age distribution, score comparisons, and top performers.

### **For Candidates**
- **Job Search and Application**: Browse and apply for job postings in just a few clicks.
- **AI-Powered Interviews**: Experience tailored interview questions based on your CV and the specific job requirements.
- **Immediate Feedback**: Get real-time feedback on interview responses to improve performance.

---

## **Setup and Installation**

To set up the RucRut application locally, follow these steps:

### **Requirements**
- **Python 3.11+**
- **Flask 2.2.3**
- **MongoDB 4.7.0**
- **SQLAlchemy 2.0.8**

### **Steps**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/OmarNouih/SmartRecruit_LLM.git
   cd RucRut
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Ensure to configure your `.env` file with the necessary environment variables for the Flask application, MongoDB connection, and Hugging Face API credentials.

4. **Initialize the database**:
   - Set up your SQLite database:
     ```bash
     flask db upgrade
     ```

5. **Run the Flask application**:
   ```bash
   flask run
   ```
   The application will be available on `http://localhost:5000`.

6. **Access MongoDB**:
   - Ensure MongoDB is running, and it's properly configured in the `.env` file.

---

## **How to Use the Application**

### **Job Providers**
1. **Sign up and Log in**.
2. **Create Job Postings**: Add jobs with specific titles, locations, descriptions, and other necessary information.
3. **Manage Applications**: Review candidates’ CVs, interview responses, and scores.
4. **Track Data**: Use the dashboard to view visual insights such as the top 3 candidates, score comparisons, and other analytics.

### **Candidates**
1. **Browse Jobs**: Search and apply for jobs that match your skills.
2. **AI Interview**: Participate in personalized interviews generated based on your CV.
3. **Get Feedback**: Receive instant feedback and improve based on AI evaluations.

---

## **Technologies Used**

- **Backend**: Flask, SQLAlchemy, MongoDB
- **Frontend**: HTML5, CSS3, JavaScript
- **AI Models**: Hugging Face Transformers, Sentence Transformers
- **PDF Parsing**: PDFPlumber

---

## **Contributing**

We welcome contributions to improve the functionality of RucRut. If you'd like to contribute, please:

1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Submit a pull request.

---

## **License**

This project is licensed under the **3DSF License**.

---

## **Contact**

For any inquiries, you can reach out to the developers:

- **Omar NOUIH** - [Email](omarnouih@gmail.com)
- **Salma SAHL** - [Email](sahlsalma56@gmail.com)
=======
# 林理人才 - 基于AI的智能招聘与人才发展系统

![林理人才 Logo](./logo.png)
*您需要將團隊 Logo 圖片（例如命名為 `logo.png`）放在專案根目錄下，上面的程式碼才能正確顯示圖片。*

[cite_start]**林理人才** (LLRC) 是一個基於AI的智能招聘與人才发展系统 [cite: 2][cite_start]。在人才競爭日益激烈的環境下，我們致力於解決企業在招聘中面臨的簡歷篩選低效、人崗匹配度低、離職預測困難等痛點，同時也幫助求職者應對崗位資訊過載、自身競爭力評估模糊等問題 [cite: 23][cite_start]。本系統旨在構建一個智慧化的招聘生態，重塑數位化招聘的新範式 [cite: 23, 28]。

## ✨ 主要功能 (Features)

本系統的核心是透過先進的 AI 演算法，實現以下智能化功能：

* [cite_start]**多模態簡歷智能解析**：支援對文字、圖片、甚至影片等多種類型簡歷的自動化解析與資訊提取 [cite: 24]。
* [cite_start]**動態人崗匹配度計算**：即時並動態地計算候選人與職位的匹配程度，提供科學的決策依據 [cite: 25]。
* [cite_start]**面試表現多維度分析**：對面試過程進行多維度的智慧分析，客觀評估候選人能力 [cite: 26]。
* [cite_start]**人才發展路徑預測**：基於數據分析，為員工與企業提供可預測的人才發展路徑規劃 [cite: 27]。

## 🛠️ 技術棧 (Tech Stack)

* [cite_start]**專案類型**: Web 應用 [cite: 21]
* [cite_start]**前端**: HTML, CSS, JavaScript [cite: 19]
* [cite_start]**後端**: Python, Java [cite: 20]

## 👨‍💻 我們的團隊 (Our Team)

### 團隊介紹 - 林理人才

* [cite_start]**團隊名稱**：林理人才 [cite: 1, 6]
* [cite_start]**名稱寓意**：“林理”，諧音“林里”，象徵團隊成員均來自**北京林業大學理學院**。以“林理”修飾“人才”，既體現了團隊的出身，也契合我們產品的核心——一個針對人才的智能招聘與發展系統 [cite: 7]。
* [cite_start]**Logo寓意**：Logo中的樹木代表了北京林業大學的特色；大腦的形象既是AI智慧的體現，也是優秀人才的象徵 [cite: 10]。
* [cite_start]**團隊模式**：我們採用 **Scrum** 模式進行敏捷開發 [cite: 12]。

### 團隊成員

| 姓名 | 定位 | 特點說明 |
| :--- | :--- | :--- |
| 侯东杨 | 項目經理 | [cite_start]較冷靜，具備規劃能力，領導力強，擅長协同團隊發展，有較強抗壓能力。 [cite: 14] |
| 謝佳悅 | 產品經理 | [cite_start]創造力強，有全域觀，做事細緻，善於溝通，抗壓能力強。 [cite: 14] |
| 張宇成 | 開發經理 | [cite_start]性格沉穩，遇事冷靜，分析能力較強；學習主動性好，能夠快速掌握新知識，善於總結規律。 [cite: 14] |
| 潘顯雨 | Team成員 | [cite_start]動手能力強，崇尚實踐，以結果為導向。學習鑽研能力突出，邏輯清晰，善於攻克並解決技術難題。 [cite: 14] |
| 蘇杰 | Team成員 | [cite_start]遇事從容，幽默難繃，善於鑽研新知識和新技能，不懼怕挑戰。 [cite: 14] |
| 李雨夢 | Team成員 | [cite_start]溝通協作能力較强，效率高，但技術能力較弱，知識面狹窄。 [cite: 14] |

## 🚀 開始使用 (Getting Started)

*(這部分您可以後續補充，說明其他開發者如何安裝、設定並執行您的專案)*

### 安裝

```bash
# 複製儲存庫
git clone [https://github.com/Rayscout/LLRC.git](https://github.com/Rayscout/LLRC.git)

# 進入專案目錄
cd LLRC

# (新增後續安裝步驟...)
>>>>>>> upstream/main
