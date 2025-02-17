import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./Login";
import WeedDetection from "./WeedDetection";
import ProtectedRoute from "./ProtectedRoute";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/detect" element={<ProtectedRoute><WeedDetection /></ProtectedRoute>} />
    </Routes>
  );
}
