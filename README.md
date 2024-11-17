# **Startup Decision Support System**

## **Problem Statement**

Develop a platform that provides the top ten actions an entrepreneur can take to strengthen a startup in a given industry and with a specific key performance indicator (KPI) provided, such as can be found here: [Gilion's Startup Metrics](https://www.gilion.com/basics/startup-metrics). This application would be useful for founding teams working to adjust their business strategy to better accommodate the current needs of their target market.

## Video Demo [Video Title](video_url)

## **Tech Required**

### **1. Analytical Skills**
- **Data Analysis**:
  - Use tools like **Pandas** or **Excel** for data manipulation and exploratory data analysis.
- **Statistical Analysis**:
  - Perform trend identification using statistical methods.

### **2. Artificial Intelligence (AI)**
- **Natural Language Processing (NLP)**:
  - Conduct **news sentiment analysis** to understand market sentiment and trends.
- **AI-Driven Recommendations**:
  - Develop recommendation systems to generate customized suggestions for startups.

### **3. Machine Learning Algorithms**
- **Classification Models**:
  - Apply machine learning techniques for trend analysis across industries and KPIs.
- **Recommendation Systems**:
  - Leverage collaborative and content-based filtering for personalized insights.

## **Tech Stack**

### **Frontend**
- **Streamlit**
- **Pandas**
- **Matplotlib**

### **Backend**
- **Flask**
- **Transformers** (Hugging Face models) (Meta llama, Google flan-t5)
- **Pandas**


## **Project Team Members**
- **Anmol Munnolli**  
- **Venkata Madhumitha Gannavaram**  
- **Virija Nandamudi**  
- **Venkatesh Talasila**

## Summary  
**Startup Buddy** is a smart data tool designed to help businesses analyze their performance and plan for growth. Comparing your company’s KPIs (Key Performance Indicators) with industry standards provides clear insights into how your business is doing and what you can improve. The platform uses advanced AI models, intuitive visualizations, and forecasting to make decision-making easy and effective.  

## Key Features  

### 1. Compare with Industry Benchmarks  
- Get industry-specific KPI benchmarks using Google’s **Flan-T5** model to see how your business stacks up.  

### 2. Personalized Recommendations  
- Receive improvement suggestions based on your KPI data, powered by Facebook’s **Llama** model.  

### 3. Forecast Future Trends  
- Predict your KPI performance for the next 12 months using a reliable **Holt-Winters statistical technique**.  

### 4. Sentiment Analysis  
- Understand market trends with sentiment analysis of news articles using **FinancialBERT**, giving you a clear picture of the current business climate.  

### 5. Visualize Your Data  
- View easy-to-understand charts and graphs created with **Matplotlib** and displayed in a user-friendly interface built with **Streamlit**.  

### 6. Flexible and Versatile  
- Works for businesses in any industry, providing tailored insights without restrictions.  

**Startup Buddy** simplifies complex data analysis, giving you the tools to make informed decisions and achieve your business goals.

  
## **How to Run the Project**

### **1. Set up a Virtual Environment**
- First, create a virtual environment for the project by running the following command in your terminal:
  ```bash
  python -m venv venv
### **2. Activate the Virtual Environment**
- On **Windows**:
  ```bash
  .\venv\Scripts\activate
### **3. Install Dependencies**
- Install the required packages listed in requirements.txt:
  ```bash
   pip install -r requirements.txt
### **4. Run the Backend**
- After setting up the virtual environment and installing the dependencies, run the backend-logic.py file:
  ```bash
   python ./backend/backend_logic.py
### **5. Run the Frontend**
- To start the frontend using Streamlit, run the app.py file:
   ```bash
   streamlit run ./frontend/app.py
