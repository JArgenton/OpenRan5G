import { useNavigate } from "react-router-dom";
import styles from "./style.module.css";

export interface RoutineData {
  ROUTINE_ID: number;
  NAME: string;
  SERVER: string;
  TIME: string;
  ACTIVE: boolean;
}

interface RoutineCardProps {
  routine: RoutineData;
  onToggleActive: (id: number, newStatus: boolean, time: string) => Promise<void>;
}

export default function RoutineCard({ routine, onToggleActive }: RoutineCardProps) {
  const navigate = useNavigate();

  const handleToggle = () => {
    onToggleActive(routine.ROUTINE_ID, !routine.ACTIVE, routine.TIME);
  };

  const handleViewTests = () => {
    navigate(`/routine/${routine.ROUTINE_ID}/testes`);
  };

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>{routine.NAME}</h2>

      <div className={styles.pair}>
        <span className={styles.label}>Servidor:</span>
        <span className={styles.value}>{routine.SERVER}</span>
      </div>

      <div className={styles.pair}>
        <span className={styles.label}>Horário:</span>
        <span className={styles.value}>{routine.TIME}</span>
      </div>

      <div className={styles.pair}>
        <span className={styles.label}>Status:</span>
        <span className={styles.value}>
          {routine.ACTIVE ? (
            <span className={`${styles.status} ${styles.ativa}`}>Ativa</span>
          ) : (
            <span className={`${styles.status} ${styles.inativa}`}>Inativa</span>
          )}
        </span>
      </div>

      <div className={styles.buttonGroup}>
        <button className={styles.cardButton} onClick={handleViewTests}>
          Ver Testes
        </button>
        <button className={styles.cardButton} onClick={handleToggle}>
          {routine.ACTIVE ? "Desativar" : "Ativar"}
        </button>
      </div>
    </div>
  );
}
