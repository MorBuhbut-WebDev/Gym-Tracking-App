import { Link } from "react-router-dom";
import styles from "./PasswordLess.module.css";
import goBackIcon from "../../../../assets/go-back-icon.svg";

function PasswordLess() {
  return (
    <main className={styles.page}>
      <Link to="/auth/landing" className={styles.goBackBtn}>
        <img src={goBackIcon} alt="Go back btn" />
      </Link>
      <form className={styles.form}>
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
              type="email"
              id="email"
              placeholder="example@gmail.com"
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
