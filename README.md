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

## Key Features

- **AI-Powered KPI Analysis**: Utilize Google's **Flan T5 LLM** to gather benchmark data and evaluate your business’s KPIs against industry standards.
  
- **Recommendation Engine**: Powered by Meta's **Llama LLM**, our system generates actionable, data-driven strategies tailored specifically to your startup's performance.
  
- **Sentiment Analysis**: Using **Hugging Face's BERT** model, we analyze the sentiment around your KPIs to understand the emotional and financial impact on your business.
  
- **Time Series Analysis & Visualization**: Our platform offers dynamic visualizations that help interpret trends and statistical foundations, making it easier to comprehend the impact of your decisions over time.

- **User-Friendly Interface**: Developed using **Streamlit** and **Flask**, the app ensures a seamless and easy-to-use experience.
  
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
