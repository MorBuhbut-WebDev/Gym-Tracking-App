import { useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import AuthRoutes from "./features/auth/routes/AuthRoutes.jsx";
import PrivateRoutes from "./routes/PrivateRoutes.jsx";

function App() {
  useMobileHeight();

  return (
    <Routes>
      <Route path="/auth/*" element={<AuthRoutes />} />
      <Route
        path="/"
        element={
          <PrivateRoutes>
            <h1>Hello From Home</h1>
          </PrivateRoutes>
        }
      />
    </Routes>
  );
}

function useMobileHeight() {
  useEffect(() => {
    const setHeight = () => {
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty("--vh", `${vh}px`);
    };
    setHeight();

    window.addEventListener("resize", setHeight);

    return () => window.removeEventListener("resize", setHeight);
  }, []);
}

export default App;
