# So, I will use FastAPI Backend for the prototype 
# this file contains the backend
# I will simply use a vector embedding approach for the RAG
# So, basically I will use similarity search to simulate the retrieval aspect of the RAG System.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import openai
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (React frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Now, I will load the mock product and ingredient data
with open("products.json", "r") as f:
    PRODUCTS = json.load(f)

with open("ingredients.json", "r") as f:
    INGREDIENTS = json.load(f)

# Loading the embedding model for retrieval aspect
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# here i will generate the embeddings for product descriptions
product_embeddings = np.array([embedding_model.encode(p["description"]) for p in PRODUCTS])

# So, I will implement the similarity based recommendation approach
# this simply means that the products will be recommended based on the similarity of the product with the query
OPENAI_API_KEY = "<OPENAI_API_KEY>"

# the below function is used to generate an enriched representation of the product using gpt
# for this purpose i have used gpt-4o-mini model
# I will make use of prompt engineering for this very purpose
def generate_augmented_description(product, context):
    openai.api_key = OPENAI_API_KEY
    prompt = f"""
    Write a **neutral, well-structured, and factual product description** in third-person. 
    The description should be informative, focusing on what the product is and its key qualities, without sounding like a marketing pitch.

    **Product Name:** {product["name"]}
    
    **Base Description:** {product["description"]}
    
    **Additional Context (about ingredients and effects):** {context}

    **Guidelines:**
    - Maintain an **objective and descriptive tone**.
    - Write in **third-person** (avoid addressing the reader directly).
    - Focus on **product qualities, key ingredients, and effects** without exaggerated language.
    - Ensure the description **reads like an informative passage**, not an advertisement.
    - Keep it **concise yet detailed**, around **4-6 sentences** in a single flowing paragraph.

    Generate a well-written, **fact-based** product description in third-person.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an expert e-commerce assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Building up on the recommendation based RAG that I had ideated
# So, basically the first step involves retrieving the 3 most relevant products from the Knowledge Base (which is basically just provided by the json files here)
# The retrieval step involves using cosine similarity as the measure to compute the semantic similarity between the query and each of the products (using the product description)
# After the products are retrieved, the ingredients corresponding to the products are also retrieved using ingredients extracted from the ingredients.json file
# the ingredient properties extracted here will just provide additional context for the rag
def recommend_products_with_rag(user_id: int, query: str):
    # firstly, using the embedding-based similarity approach to get the closest products to the query, based on the product description
    query_embedding = embedding_model.encode(query)
    scores = cosine_similarity([query_embedding], product_embeddings)[0]
    top_indices = np.argsort(scores)[-3:][::-1]  
    recommended_products = []
    
    for i in top_indices:
        product = PRODUCTS[i]
        ingredient_context = " ".join([ing["properties"] for ing in INGREDIENTS if ing["name"] in product["ingredients"]])
        # here will use the above created function to generate the enriched descriptions
        augmented_description = generate_augmented_description(product, ingredient_context)
        product["description"] = augmented_description
        recommended_products.append(product)
    
    return recommended_products

# Creating API for getting product recommenations, along with enriched representations from the rag
@app.get("/recommend", response_model=dict)
def get_recommendations(user_id: int, query: str):
    recommendations = recommend_products_with_rag(user_id, query)
    return {"recommended_products": recommendations}

# this API gives all the products
@app.get("/products", response_model=dict)
def get_products():
    return {"products": PRODUCTS}

# this API gives the details of a particular product
@app.get("/product/{product_id}", response_model=dict)
def get_product(product_id: int):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product:
        return product
    raise HTTPException(status_code=404, detail=f"Product with ID: {product_id} not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)