import { createContext, useContext, useState, useEffect } from "react";
import { onIdTokenChanged } from "firebase/auth";
import { auth } from "../services/firebase.js";
import { useLoading } from "../../../context/LoadingProvider.jsx";
import { getEmail } from "../pages/PasswordLess/utils.js";

const TokenContext = createContext();

export const useToken = () => useContext(TokenContext);

function TokenProvider({ children }) {
  const [token, setToken] = useState("");
  const { setLoading } = useLoading();

  useEffect(() => {
    const unsubscribe = onIdTokenChanged(auth, (user) => {
      if (user) {
        user.getIdToken().then((token) => {
          setToken(token);
        });
      } else {
        setToken("");
      }
      setLoading(!(getEmail() === ""));
    });

    return () => unsubscribe();
  }, []);

  return (
    <TokenContext.Provider value={{ token }}>{children}</TokenContext.Provider>
  );
}

export default TokenProvider;
