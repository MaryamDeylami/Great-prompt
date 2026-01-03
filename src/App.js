import React, { useState } from "react";
import { registerUser, loginUser, askAI } from "./api";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [prompt, setPrompt] = useState("");
  const [aiResponse, setAIResponse] = useState("");

  const handleRegister = async () => {
  try {
    const res = await registerUser(email, password);
    if(res && res.data) {
      alert(res.data.message);
    } else {
      alert("Unexpected response from server");
    }
  } catch (err) {
    if(err.response && err.response.data && err.response.data.detail){
      alert(err.response.data.detail);
    } else {
      alert("Error connecting to server");
    }
  }
};
  const handleLogin = async () => {
    try {
      const res = await loginUser(email, password);
      localStorage.setItem("token", res.data.access_token);
      alert("Login successful");
    } catch (err) {
      alert(err.response.data.detail);
    }
  };

  const handleAskAI = async () => {
    try {
      const res = await askAI(prompt, email);
      setAIResponse(res.data.response);
    } catch (err) {
      alert("Error contacting AI");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Register</h2>
      <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button onClick={handleRegister}>Register</button>

      <h2>Login</h2>
      <button onClick={handleLogin}>Login</button>

      <h2>Ask AI</h2>
      <input placeholder="Your prompt" value={prompt} onChange={e => setPrompt(e.target.value)} />
      <button onClick={handleAskAI}>Ask</button>
      <p>Response: {aiResponse}</p>
    </div>
  );
}

export default App;
