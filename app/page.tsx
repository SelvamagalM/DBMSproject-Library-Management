import styles from './page.module.css';

export default function Home() {
  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <h1 className={styles.title}>
          Library Management System
        </h1>

        <p className={styles.description}>
          A DBMS-powered library management application with Vercel Web Analytics
        </p>

        <div className={styles.grid}>
          <div className={styles.card}>
            <h2>Books &rarr;</h2>
            <p>Browse and manage the library&apos;s book collection</p>
          </div>

          <div className={styles.card}>
            <h2>Members &rarr;</h2>
            <p>View and manage library members</p>
          </div>

          <div className={styles.card}>
            <h2>Loans &rarr;</h2>
            <p>Track book loans and returns</p>
          </div>

          <div className={styles.card}>
            <h2>Analytics &rarr;</h2>
            <p>View library statistics and reports</p>
          </div>
        </div>
      </main>
    </div>
  );
}
