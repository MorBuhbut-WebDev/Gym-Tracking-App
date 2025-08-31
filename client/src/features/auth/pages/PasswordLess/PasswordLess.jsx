import { useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
import { sendLinkToEmail } from "./utils.js";
import styles from "./PasswordLess.module.css";
import goBackIcon from "../../../../assets/go-back-icon.svg";

function PasswordLess() {
  const emailRef = useRef(null);
  const navigate = useNavigate();

  return (
    <main className={styles.page}>
      <Link to="/auth/landing" className={styles.goBackBtn} replace>
        <img src={goBackIcon} alt="Go back btn" />
      </Link>
      <form
        className={styles.form}
        onSubmit={async (e) => {
          e.preventDefault();
          await sendLinkToEmail({
            email: emailRef.current.value,
            navigate,
          });
        }}
      >
        <div className={styles.textContainer}>
          <h1>Welcome To Tracker</h1>
          <p>Sign in or sign up down below</p>
        </div>
        <div className={styles.fieldsContainer}>
          <div className={styles.inputContainer}>
            <label htmlFor="email" className={styles.label}>
              Email
            </label>
            <input
              className={styles.input}
              ref={emailRef}
              type="email"
              id="email"
              placeholder="example@gmail.com"
              required
            />
          </div>
          <p className={styles.desc}>
            A link will be sent to your email to complete the authentication
            process.
          </p>
          <button className={styles.submitBtn} type="submit">
            Submit
          </button>
        </div>
      </form>
    </main>
  );
}

export default PasswordLess;
