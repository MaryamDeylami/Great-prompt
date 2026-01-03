import { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const [user, setUser] = useState({});

  useEffect(() => {
    const token = localStorage.getItem("token");
    axios.get("http://127.0.0.1:8000/me", { params: { token } })
      .then(res => setUser(res.data));
  }, []);

  return <h1>Welcome {user.email}</h1>;
}
