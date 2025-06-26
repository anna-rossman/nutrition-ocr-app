import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("image", file);

    try {
      const res = await axios.post("http://localhost:5000/api/ocr", formData);
      setText(res.data.ingredientsText);
    } catch (err) {
      console.error("OCR failed", err);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Ingredient OCR Scanner</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleSubmit}>Scan</button>
      <h3>Extracted Ingredients:</h3>
      <p>{text}</p>
    </div>
  );
}

export default App;
