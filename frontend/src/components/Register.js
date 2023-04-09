import React, { useState } from "react";
import axios from "axios";

const Register = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [company_name, setCompanyName] = useState("");
  const [error, setError] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("/api/register/", {
        username,
        password,
        company_name,
      });
      if (response.data.token) {
        localStorage.setItem("token", response.data.token);
        window.location.reload();
      } else {
        setError("Registration failed");
      }
    } catch (err) {
      setError("Registration failed");
    }
  };

  return (
    <section className="hero">
    <div className="container">
      <h1>Register</h1>
      <form onSubmit={handleRegister}>
        <div className="form-group">
          <label htmlFor="company_name">Company Name:</label>
          <input
            type="text"
            className="form-control"
            id="company_name"
            value={company_name}
            onChange={(e) => setCompanyName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            className="form-control"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            className="form-control"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p className="text-danger">{error}</p>}
        <button type="submit" className="btn btn-primary">
          Register
        </button>
      </form>
    </div>
    </section>
  );
};

export default Register;
