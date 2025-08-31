import styles from "./Loader.module.css";

function Loader() {
  return (
    <div className={styles.container}>
      <span className={`${styles.ball} ${styles.ball1}`}></span>
      <span className={`${styles.ball} ${styles.ball2}`}></span>
      <span className={`${styles.ball} ${styles.ball3}`}></span>
    </div>
  );
}

export default Loader;
