import { sendSignInLinkToEmail } from "firebase/auth";
import { auth } from "../../services/firebase.js";

export async function sendLinkToEmail({ email, navigate }) {
  try {
    await sendSignInLinkToEmail(auth, email, {
      url: import.meta.env.VITE_FIREBASE_SIGNIN_URL,
      handleCodeInApp: true,
    });

    saveEmail(email);
    navigate("/auth/check-email", { replace: true });
  } catch (error) {
    console.error("Error sending email link:", error);
    return null;
  }
}

export function saveEmail(email) {
  localStorage.setItem("emailForSignIn", email);
}

export function getEmail({ clearStorage = false } = {}) {
  const email = localStorage.getItem("emailForSignIn");
  if (clearStorage) localStorage.removeItem("emailForSignIn");
  return email || "";
}
