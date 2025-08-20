import styles from "./Landing.module.css";

function Landing() {
  return (
    <main className={styles.landing}>
      <p className={styles.logo}>TRACKER</p>
      <h1 className={styles.motivation}>
        "Track your workouts and crush your fitness goals"
      </h1>
      <div className={styles.buttons}>
        <button className={styles.signInPassword}>
          Sign in with Email & Password
        </button>
        <button className={styles.signInPasswordless}>
          Sign in with Email Link (No Password)
        </button>
      </div>
    </main>
  );
}

export default Landing;
