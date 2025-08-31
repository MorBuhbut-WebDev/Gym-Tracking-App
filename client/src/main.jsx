import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import "./main.css";
import App from "./App.jsx";
import TokenProvider from "./features/auth/context/TokenProvider.jsx";
import LoadingProvider from "./context/LoadingProvider.jsx";

createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <LoadingProvider>
      <TokenProvider>
        <App />
      </TokenProvider>
    </LoadingProvider>
  </BrowserRouter>
);
