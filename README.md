Here’s a well-structured **`README.md`** file for your project. Just copy and paste it into your GitHub repository. 🚀  

---

# **Customer Chatbot with AI & Data Insights** 🤖  

An intelligent chatbot that answers **customer-related queries** using **AI & FAISS-powered search**. It understands user questions, retrieves customer insights from a dataset, and responds accordingly. If no relevant data is found, it uses an **AI model (Groq API)** for general queries.  


---

## **✨ Features**  
✅ **AI-Powered Responses**: Uses Groq API for general queries  
✅ **Smart Dataset Search**: Retrieves customer details based on **ID, age, gender, income, and spending score**  
✅ **Fast Search with FAISS**: Efficient similarity-based lookup for customer queries  
✅ **Dark Mode Toggle**: User-friendly interface with light/dark mode  
✅ **Voice Input Support**: Speak instead of typing for hands-free interaction  
✅ **Beautiful UI**: Responsive and clean chatbot interface  

---

## **📂 Project Structure**  

```
│── /static              # Frontend Assets (CSS, JS)
│    │── styles.css       # Stylesheet
│    │── chat.js          # Chatbot functionality (JS)
│── /templates           # HTML Templates
│    │── index.html       # Home Page
│    │── chatbot.html     # Chatbot Page
│    │── about.html       # About Page
│    │── contact.html     # Contact Page
│    │── footer.html      # Footer Component
│    │── navbar.html      # Navigation Bar
│── chatbot.py           # Main Flask backend
│── Mall_Customers.csv   # Customer dataset
│── README.md            # Project Documentation (You're reading this!)
```

---

## **🔧 Installation & Setup**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/pallav110/customer-chatbot.git
```

### **2️⃣ Install Dependencies**  
Make sure you have Python installed, then run:  
```bash
pip install -r requirements.txt
```

### **3️⃣ Run the Chatbot Locally**  
```bash
python chatbot.py
```
The chatbot will be available at **`http://127.0.0.1:5000/`**.

---

## **📊 Dataset Used**  
We use the **Mall Customers Dataset** which contains customer details such as:  
- **Customer ID**  
- **Gender**  
- **Age**  
- **Annual Income (in $1000s)**  
- **Spending Score (1-100)**  

📝 *The chatbot retrieves relevant information when users ask about customer details or trends in the dataset.*

---

## **🛠️ Technologies Used**  
- **Python (Flask)** - Backend Framework  
- **FAISS** - Fast Similarity Search for Dataset Queries  
- **Sentence Transformers** - Text Embeddings for Efficient Searching  
- **Groq API** - AI-based Conversational Responses  
- **HTML, CSS, JS** - Frontend for the Chatbot UI  
- **Tailwind CSS** - Modern and Responsive UI  

---

## **🤝 Contributing**  
Feel free to **fork this repository**, create a branch, and submit a pull request. Contributions are welcome! 😊  

---

## **📜 License**  
This project is **open-source** under the **MIT License**.  

---

### ⭐ **If you like this project, don’t forget to give it a star on GitHub!** ⭐  

---

Let me know if you want any modifications! 🚀
