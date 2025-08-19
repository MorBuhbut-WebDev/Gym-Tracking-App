import { useToken } from "../features/auth/context/TokenProvider.jsx";
import { useLoading } from "../context/LoadingProvider.jsx";
import { Navigate } from "react-router-dom";

function PrivateRoutes({ children }) {
  const { token } = useToken();
  const { loading } = useLoading();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!token) {
    return <Navigate to="/auth/landing" replace />;
  }

  return children;
}

export default PrivateRoutes;
