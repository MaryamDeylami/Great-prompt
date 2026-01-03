import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav style={styles.nav}>
      <h3>Prompt Management System</h3>
      <div>
        <Link to="/login" style={styles.link}>Login</Link>
        <Link to="/register" style={styles.link}>Register</Link>
        <Link to="/dashboard" style={styles.link}>Dashboard</Link>
        <Link to="/feedback" style={styles.link}>Feedback</Link>
      </div>
    </nav>
  );
}

const styles = {
  nav: {
    padding: "10px 20px",
    background: "#222",
    color: "#fff",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center"
  },
  link: {
    color: "#fff",
    marginLeft: "15px",
    textDecoration: "none"
  }
};

export default Navbar;
