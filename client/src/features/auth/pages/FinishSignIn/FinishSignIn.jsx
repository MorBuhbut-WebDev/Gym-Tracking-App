import { useState, useEffect } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { isSignInWithEmailLink, signInWithEmailLink } from "firebase/auth";
import { auth } from "../../services/firebase.js";
import { getEmail } from "../PasswordLess/utils.js";
import Loader from "../../../../components/Loader/Loader.jsx";

function FinishSignIn() {
  const [error, setError] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (isSignInWithEmailLink(auth, window.location.href)) {
      const email = getEmail({
        clearStorage: true,
      });
      signInWithEmailLink(auth, email, window.location.href)
        .then(() => {
          navigate("/", { replace: true });
        })
        .catch((e) => {
          console.log(e);
          setError(true);
        });
    } else setError(true);
  }, []);

  if (error) {
    return <Navigate to="/auth/landing" replace />;
  }

  return <Loader />;
}

export default FinishSignIn;
