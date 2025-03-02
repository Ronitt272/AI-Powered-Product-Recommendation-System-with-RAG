import { useState } from "react";

export default function App() {
  const [query, setQuery] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState(null);

  const fetchRecommendations = async () => {
    setError(null);
    try {
      const res = await fetch(`http://127.0.0.1:8000/recommend?user_id=123&query=${query}`);
      if (!res.ok) {
        throw new Error("Failed to fetch recommendations");
      }
      const data = await res.json();
      setRecommendations(data.recommended_products || []); // Extract correct field
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "auto", padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ textAlign: "center" }}>AI-Powered Product Recommendations</h1>
      <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
        <input 
          type="text" 
          value={query} 
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter a search query..."
          style={{ flex: 1, padding: "10px", border: "1px solid #ccc", borderRadius: "5px" }}
        />
        <button 
          onClick={fetchRecommendations} 
          style={{ padding: "10px 15px", background: "#007bff", color: "white", border: "none", borderRadius: "5px", cursor: "pointer" }}
        >
          Get Recommendations
        </button>
      </div>
      {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
      <h2 style={{ borderBottom: "2px solid #ddd", paddingBottom: "5px" }}>Recommended Products:</h2>
      <div style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
        {recommendations.length > 0 ? (
          recommendations.map((product) => (
            <div key={product.id} style={{ padding: "15px", border: "1px solid #ddd", borderRadius: "5px", background: "#f9f9f9", marginBottom: "10px" }}>
              <h3 style={{ marginBottom: "5px" }}>{product.name}</h3>
              <p style={{ fontSize: "14px", color: "#555" }}>{product.description}</p>
              <p style={{ fontSize: "14px", fontWeight: "bold" }}>Ingredients: {product.ingredients.join(", ")}</p>
              <p style={{ fontSize: "14px", fontWeight: "bold", color: "#007bff" }}>Price: ${product.price}</p>
            </div>
          ))
        ) : (
          <p style={{ textAlign: "center", color: "#555" }}>No recommendations found.</p>
        )}
      </div>
    </div>
  );
}
