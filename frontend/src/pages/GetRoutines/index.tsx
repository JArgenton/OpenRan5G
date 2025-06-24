import DefaultHeader from "../../Components/DefaultHeader";
import RoutineCard, { RoutineData } from "../../Components/RoutineCard";
import { useEffect, useState } from "react";
import style from "./style.module.css";
import { ClipLoader } from "react-spinners";

export default function GetRoutines() {
  const [result, setResult] = useState<{ routines: RoutineData[] }>({ routines: [] });
  const [loading, setLoading] = useState<boolean>(true);

  // 🔁 Função reutilizável
  async function fetchRoutines() {
    const res = await fetch("http://localhost:8000/api/routine/saved", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!res.ok) {
      console.error("Erro ao buscar dados");
      setLoading(false);
      return;
    }

    const data = await res.json();
    setResult(data);
  }

  useEffect(() => {
    setLoading(true);
    fetchRoutines();
    setLoading(false);
  }, []);

  // 🔄 Chama o backend e recarrega rotinas
  async function handleActivate(id: number, active: boolean, time: string) {
    const res = await fetch("http://localhost:8000/api/routine/activate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ r_id: id, active , time}),
    });

    if (!res.ok) {
      console.error("Erro ao alterar rotina");
      return;
    }

    await fetchRoutines(); // 🔁 Recarrega rotinas atualizadas
  }

  if (loading) {
    return (
      <div className={style.loaderWrapper}>
        <div className={style.loaderBox}>
          <ClipLoader size={60} color="#00bfff" />
          <p>Carregando dados das rotinas, por favor aguarde...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <DefaultHeader title="Rotinas Salvas" />
      <div className={style.resultContainer}>
        <div className={style.cardList}>
          {result.routines.map((r) => (
            <RoutineCard key={r.ROUTINE_ID} routine={r} onToggleActive={handleActivate} />
          ))}
        </div>
      </div>
    </>
  );
}
