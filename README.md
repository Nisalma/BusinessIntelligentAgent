# BusinessIntelligentAgent
Nexus Retail Engine with AI Consultant and Secure Config

From Raw Data to Predictive Intelligence: The Nexus Journey
Data is just noise until you give it a voice. Over the past few weeks, I’ve been building Nexus, a project designed to take raw, messy retail records and transform them into a live, conversational AI consultant.

Here is the breakdown of how I built the pipeline from scratch:

 Stage 1: The Foundation (Engineering)
I started with a massive raw dataset from Kaggle. Using Google Colab, I performed the initial handling missing values and refining features to prepare the data for a professional environment. Once the data was pristine, I migrated it to MySQL, where I built structured views and performed the queries necessary to extract core business KPIs.

 Stage 2: The Visual Layer (Power BI)
With a solid SQL backbone, I first moved into Power BI. I developed a dashboard to handle the heavy historical lifting—mapping out global sales and market share. While this gave me a great "Big Picture," I realized that static charts can't answer "What's next?" I wanted something interactive and alive.

Stage 3: The Intelligence Layer (Streamlit & ML)
To turn a static report into a strategic tool, I used Python and Streamlit to build a custom web engine. This is where the project moved from reporting to consulting:

Machine Learning: I integrated a Linear Regression model using scikit-learn. By analyzing hourly sales momentum, the engine now forecasts revenue for the upcoming business window.

The Nexus Consultant: I developed a chatbot that uses multi-keyword logic to understand user intent. It doesn't just guess; it knows the difference between a request for the "Best Item" and the "Best Hour" of the day.

The Big Picture
The result is a Hybrid Intelligence System. It uses Power BI for deep-dive historical auditing and Python/ML for real-time, conversational forecasting.

Nexus proves that the most powerful business tools aren't just about looking at where you've been—they’re about predicting where you’re going. By bridging the gap between SQL databases and Machine Learning, I’ve turned a "static log" into a "strategic advisor."

 Technical Deep Dive (For the Devs)
Data Cleaning: Google Colab / Pandas

Database: MySQL (Relational Schema)

BI & Visualization: Power BI (DAX)
Frontend: Streamlit (Python)
Predictive Model: Scikit-Learn (Linear Regression)
Security: Environment Variables (.env) for credential protection.

#DataScience #Python #MachineLearning #SQL #PowerBI #Streamlit #DataEngineering #AI #WomenInTech
