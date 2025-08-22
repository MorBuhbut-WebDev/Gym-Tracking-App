import { Link } from "react-router-dom";
import styles from "./Landing.module.css";

function Landing() {
  return (
    <main className={styles.landing}>
      <p className={styles.logo}>TRACKER</p>
      <h1 className={styles.motivation}>
        "Track your workouts and crush your fitness goals"
      </h1>
      <div className={styles.buttons}>
        <Link to="/auth/register" className={styles.link} replace>
          <button className={styles.signInPassword}>
            Sign in with Email & Password
          </button>
        </Link>
        <Link to="/auth/passwordless" className={styles.link} replace>
          <button className={styles.signInPasswordless}>
            Sign in with Email Link (No Password)
          </button>
        </Link>
      </div>
    </main>
  );
}

export default Landing;
