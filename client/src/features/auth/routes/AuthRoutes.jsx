import { Routes, Route } from "react-router-dom";
import Landing from "../pages/Landing/Landing.jsx";

function AuthRoutes() {
  return (
    <Routes>
      <Route path="landing" element={<Landing />} />
      <Route path="login" element={<h1>Login Page</h1>} />
      <Route path="register" element={<h1>Sign up Page</h1>} />
    </Routes>
  );
}

export default AuthRoutes;
