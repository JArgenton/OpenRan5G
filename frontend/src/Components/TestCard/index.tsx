import { useNavigate } from "react-router-dom";
import styles from "./style.module.css";

export interface TestData {
  TEST_ID: number;
  PROTOCOL?: number;
  DURATION_SECONDS?: number;
  PACKET_SIZE?: number;
  PACKET_COUNT?: number;
}

interface TestCardProps {
  test: TestData,
  r_id: string | undefined
}

export default function TestCard({ test, r_id }: TestCardProps) {
  const navigate = useNavigate();

  const handleViewDetails = () => {
    navigate(`/results/${test.TEST_ID}/${r_id}`);
  };

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>Teste #{test.TEST_ID}</h2>

      <div className={styles.pair}>
        <span className={styles.label}>Protocolo:</span>
        <span className={styles.value}>{test.PROTOCOL ?? "N/A"}</span>
      </div>

      <div className={styles.pair}>
        <span className={styles.label}>Duração (s):</span>
        <span className={styles.value}>{test.DURATION_SECONDS ?? "N/A"}</span>
      </div>

      <div className={styles.pair}>
        <span className={styles.label}>Tamanho do Pacote:</span>
        <span className={styles.value}>{test.PACKET_SIZE ?? "N/A"} bytes</span>
      </div>

      <div className={styles.pair}>
        <span className={styles.label}>Qtd. de Pacotes:</span>
        <span className={styles.value}>{test.PACKET_COUNT ?? "N/A"}</span>
      </div>

      <div className={styles.buttonGroup}>
        <button className={styles.cardButton} onClick={handleViewDetails}>
          Ver Detalhes
        </button>
      </div>
    </div>
  );
}
