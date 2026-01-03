import { useState } from "react";
import axios from "axios";

export default function Feedback() {
  const [promptId, setPromptId] = useState("");
  const [feedback, setFeedback] = useState("");

  const sendFeedback = async () => {
    await axios.post("http://127.0.0.1:8000/feedback", {
      prompt_id: promptId,
      user_email: "test@test.com",
      feedback,
    });
    alert("Feedback sent");
    setPromptId("");
    setFeedback("");
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-4 border rounded">
      <h2 className="text-xl font-bold mb-4">Feedback</h2>
      <input
        type="text"
        placeholder="Prompt ID"
        className="border p-2 w-full mb-2"
        value={promptId}
        onChange={(e) => setPromptId(e.target.value)}
      />
      <textarea
        placeholder="Your feedback"
        className="border p-2 w-full mb-2"
        value={feedback}
        onChange={(e) => setFeedback(e.target.value)}
      />
      <button className="bg-green-600 text-white p-2 w-full" onClick={sendFeedback}>
        Send Feedback
      </button>
    </div>
  );
}
