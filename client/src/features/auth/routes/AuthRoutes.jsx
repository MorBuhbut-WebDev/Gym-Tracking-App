import { Routes, Route } from "react-router-dom";
import Landing from "../pages/Landing/Landing.jsx";
import PasswordLess from "../pages/PasswordLess/PasswordLess.jsx";
import CheckEmail from "../pages/CheckEmail/CheckEmail.jsx";
import FinishSignIn from "../pages/FinishSignIn/FinishSignIn.jsx";

function AuthRoutes() {
  return (
    <Routes>
      <Route path="landing" element={<Landing />} />
      <Route path="passwordless" element={<PasswordLess />} />
      <Route path="check-email" element={<CheckEmail />} />
      <Route path="finish-sign-in" element={<FinishSignIn />} />
      <Route path="login" element={<h1>Login Page</h1>} />
      <Route path="register" element={<h1>Sign up Page</h1>} />
    </Routes>
  );
}

export default AuthRoutes;
