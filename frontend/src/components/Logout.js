import React, { useEffect } from "react";

const Logout = () => {
  useEffect(() => {
    localStorage.removeItem("token");
    window.location.href = "/";
  }, []);

  return (
    <div className="container">
      <h1>Logging Out...</h1>
    </div>
  );
};

export default Logout;
