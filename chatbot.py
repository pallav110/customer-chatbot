import os
import groq
import faiss
import pandas as pd
from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer

app = Flask(__name__, static_folder="static", template_folder="templates")

model = SentenceTransformer("all-MiniLM-L6-v2")

dataset_path = "Mall_customers.csv"  
try:
    df = pd.read_csv(dataset_path, dtype={"CustomerID": str})  
    print("✅ CSV Loaded Successfully.")
except Exception as e:
    print(f"❌ Error Loading CSV: {e}")
    df = None

required_columns = ["CustomerID", "Genre", "Age", "Annual Income (k$)", "Spending Score (1-100)"]
if df is not None and all(col in df.columns for col in required_columns):
    documents = df.astype(str).apply(lambda row: " | ".join(row), axis=1).tolist()
    doc_embeddings = model.encode(documents)

    if doc_embeddings.shape[0] > 0:
        index = faiss.IndexFlatL2(doc_embeddings.shape[1])
        index.add(doc_embeddings)
        print("✅ FAISS Index created.")
    else:
        print("❌ Error: No embeddings generated.")
        index = None
else:
    print("❌ Error: CSV file does not contain the required columns.")
    documents = []
    doc_embeddings = None
    index = None

# Groq API Key (Replace with yours)
GROQ_API_KEY = "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"

if not GROQ_API_KEY:
    raise ValueError("❌ Groq API Key is missing! Set it properly.")

# Initialize Groq Client
client = groq.Client(api_key=GROQ_API_KEY)

def is_dataset_query(query):
    """Detect if the query is related to the dataset"""
    dataset_keywords = ["customer", "income", "spending", "score", "age", "gender", "annual", "salary"]
    return any(keyword in query.lower() for keyword in dataset_keywords)

def get_response(query):
    """Dynamically process any dataset query using FAISS + LLM"""
    
    # **1️⃣ Detect Specific CustomerID Queries**
    words = query.split()
    for word in words:
        if word.isdigit() and len(word) == 4:  # Assuming CustomerID is 4 digits
            customer_data = df[df["CustomerID"] == word]
            if not customer_data.empty:
                person = customer_data.iloc[0]
                return (
                    f"Customer {word} is a {person['Age']}-year-old {person['Genre']} "
                    f"with an annual income of ${person['Annual Income (k$)']}k "
                    f"and a spending score of {person['Spending Score (1-100)']}."
                )

    # **2️⃣ Convert Dataset into Searchable Text**
    dataset_text = "\n".join([f"Customer {row.CustomerID}: {row.Genre}, {row.Age} years old, "
                               f"Annual Income ${row['Annual Income (k$)']}k, Spending Score {row['Spending Score (1-100)']}"
                               for _, row in df.iterrows()])

    # **3️⃣ Use FAISS for Information Retrieval**
    if index:
        query_embedding = model.encode([query])
        _, I = index.search(query_embedding, 3)  # Retrieve top 3 similar results
        retrieved_docs = [documents[i] for i in I[0] if i < len(documents)]
        
        if retrieved_docs:
            retrieved_text = "\n".join(retrieved_docs)
            
            # **4️⃣ Use LLM (Groq) to Format the Response Based on Retrieved Data**
            system_prompt = (
                "You are an AI assistant analyzing customer data. "
                "Answer questions using the provided dataset. Be concise and factual."
            )

            try:
                response = client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Dataset:\n{retrieved_text}\n\nUser Query: {query}"}
                    ],
                    temperature=0.3,
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"❌ Groq API Error: {e}")
                return "❌ Error fetching data from AI model."

    return "I couldn't find relevant data in the dataset. Can you clarify your question?"


# Flask Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle user queries via API"""
    data = request.get_json()
    user_query = data.get("message", "").strip()

    if not user_query:
        return jsonify({"error": "❌ No message provided"}), 400

    response = get_response(user_query)
    return jsonify({"response": response})



if __name__ == "__main__":
    app.run(debug=True)
