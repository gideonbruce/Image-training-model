import React, { useState } from "react";

export default function WeedDetection() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async () => {
    if (!image) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("image", image);

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to process image");

      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      setProcessedImage(imageUrl);

      // Auto-download processed image
      const link = document.createElement("a");
      link.href = imageUrl;
      link.download = "detected_image.jpg";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error("Error processing image:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <div className="container">
      <h1 className="title">Weed Detection System</h1>
      <input type="file" accept="image/*" onChange={handleImageUpload} className="file-input" />
      {preview && <img src={preview} alt="Uploaded Preview" className="image-preview" />}
      <button onClick={handleSubmit} disabled={!image || loading} className="detect-button">
        {loading ? "Processing..." : "Detect Weeds"}
      </button>
      {processedImage && <img src={processedImage} alt="Processed Image" className="image-preview" />}
      <button onClick={handleLogout} className="logout-button">Logout</button>
    </div>
  );
}
