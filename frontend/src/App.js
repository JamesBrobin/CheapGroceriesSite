import { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [products, setProducts] = useState([]);
  const [sortField, setSortField] = useState("calories_per_dollar");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/products")
      .then((res) => setProducts(res.data))
      .catch((err) => console.error(err));
  }, []);

  // Sort products by selected field (descending)
  const sortedProducts = [...products].sort(
    (a, b) => (b[sortField] || 0) - (a[sortField] || 0)
  );

  return (
    <div style={{ padding: "20px" }}>
      <h1>King Soopers: Calories per Dollar</h1>

      <label>
        Sort by:{" "}
        <select
          value={sortField}
          onChange={(e) => setSortField(e.target.value)}
        >
          <option value="calories_per_dollar">Calories / $</option>
          <option value="calories_per_package">Calories per Package</option>
          <option value="calories_per_100g">Calories per 100g</option>
          <option value="price">Price</option>
          <option value="grams">Weight (g)</option>
        </select>
      </label>

      <table
        border="1"
        cellPadding="5"
        style={{ marginTop: "20px", width: "100%", borderCollapse: "collapse" }}
      >
        <thead style={{ backgroundColor: "#f4f4f4" }}>
          <tr>
            <th>Name</th>
            <th>Brand</th>
            <th>Store</th>
            <th>Zipcode</th>
            <th>USDA Description</th>
            <th>Size</th>
            <th>Size in grams</th>
            <th>Price ($)</th>
            <th>Calories / Package</th>
            <th>Calories / 100g</th>
            <th>Calories / $</th>
            <th>Source for Calories</th>
          </tr>
        </thead>
        <tbody>
          {sortedProducts.map((p, idx) => (
            <tr key={idx}>
              <td>{p.name || "—"}</td>
              <td>{p.brand || "—"}</td>
              <td>{p.store || "—"}</td>
              <td>{p.zipcode || "—"}</td>
              <td>{p.usda_description || "—"}</td>
              <td>{p.size_from_kroger || "—"}</td>
              <td>{p.size_in_grams?.toFixed(0) || "N/A"}</td>
              <td>{p.price?.toFixed(2) || "N/A"}</td>
              <td>{p.calories_per_package?.toFixed(0) || "N/A"}</td>
              <td>{p.calories_per_100_grams?.toFixed(0) || "N/A"}</td>
              <td>{p.calories_per_dollar?.toFixed(0) || "N/A"}</td>
              <td>{p.source || "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;