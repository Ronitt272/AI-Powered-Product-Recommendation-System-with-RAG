# AI-Powered-Product-Recommendation-System-with-RAG
This project implements a Retrieval-Augmented Generation (RAG) based recommendation system using a FastAPI backend and a React frontend. The system provides AI-powered product recommendations based on user queries, leveraging semantic search for retrieval and LLM-based augmentation for enhanced descriptions of recommended products.

## Tech Stack
- Backend: FastAPI, Sentence-Transformers, OpenAI GPT-4o-mini
- Frontend: React.js
- Data: JSON-based mock product and ingredient datasets

## How to Run the Prototype
1. Clone the Repository
```
git clone https://github.com/Ronitt272/AI-Powered-Product-Recommendation-System-with-RAG.git
cd AI-Powered-Product-Recommendation-System-with-RAG
```
3. Setup and Run the Backend (FastAPI)
- Install the dependencies
```
pip install -r requirements.txt
```
- Run the FastAPI Server
```
python app.py
```
3. Setup and Run the Frontend (React)
- Navigate to the React Frontend
```
cd react-frontend
```

- Install Dependencies
```
npm install
```

- Start the React App
```
npm start
```

Frontend will be available at: `http://localhost:3000`. Just navigate to the above link on your local browser to access the app.

## Approach for recommendation algorithm and RAG Implementation

1. Semantic Search for Retrieval 
The system converts product descriptions into embeddings using sentence-transformers/all-MiniLM-L6-v2. When a user provides a query, the system calculates cosine similarity between the query and each product description to retrieve the top 3 most relevant products.

2. Retreival-Augmented Generation (RAG) System
Once the relevant products are retrieved, the system fetches additional contextual information from ingredient properties. This context is passed to GPT-4o-mini, which generates an enriched product description that enhances the original details.

## Design Decisions and Tradeoffs
1. Use of FastAPI Backend:
- Decision: I chose FastAPI because of it's high performance, asynch capabilities and automatic API documentation.
- Tradeoff: Flask is simpler, but FastAPI provides better performance and also has better aynchronous capabilities, making it ideal for handling concurrent requests in a recommendation system.

2. Use of GPT 4o MiniL:
- Decision: I chose GPT 4o Mini because it's a high performance model to generate enriched product descriptions based on retrieved information.
- Tradeoff: I feel that GPT 4o Mini provides an optimal tradeoff here because GPT 3.5 turbo or other variants of GPT 3.5 provide weaker performance than GPT 4o Mini, and GPT 4o even though provides much higher performance than GPT 4o but at the cost of much higher API cost. As such a system scales, the number of API requests would increase drastically, therefore API cost is an important concern, and GPT 4o Mini is good enough to satisfy the need.

3. React Frontend:
- Decision: React is used to create a simple UI for displaying the recommendations.
- Tradeoff: I am using a FastAPI backend, so I could have used a Streamlit frontend instead but I decided not to, as even though React introduces extra dependencies, it allows for creating structured and scalable UI compared to Streamlit or other simpler javascript frontend frameworks, such as vue.js 

## Assumptions and Simplifications
- Use of Mock Data: Only Mock data is used (stored in the json files), and no live database is used.
- Basic RAG Implementation: Uses semantic similarity rather than full-text retrieval.
- GPT-Generated Augmentations: Uses prompt engineering for enhancing descriptions dynamically.
- No User Personalization: The system does not consider past user behavior.

## Potential Areas for Improvement
 - Personalized Recommendations: Integrating user history for personalized results that are tailored for the specific user.
 - Expanded Knowledge Base: Enhancing RAG with structured product metadata.
 - Use of proper Database: Replacing static JSON with a database.
 - Optimized Search: Implementing FAISS indexing for faster vector search instead of simple brute force search over the knowledge base.

## Results of Test Query

![Image 1](images/AG_Reco_Sys_Test_Query_img1.png)
![Image 2](images/AG_Reco_Sys_Test_Query_img2.png)

