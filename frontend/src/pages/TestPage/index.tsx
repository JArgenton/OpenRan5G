import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import TestCard from "../../Components/TestCard";
import { TestData } from "../../Components/TestCard";
import styles from "./style.module.css"; // crie esse CSS como preferir
import DefaultHeader from "../../Components/DefaultHeader";

export default function TestPage() {
  const { routineId } = useParams<{ routineId: string }>();
  const [tests, setTests] = useState<TestData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
  async function fetchTests() {
    try {
      const response = await fetch(`http://localhost:8000/api/routine/${routineId}/tests`);
      if (!response.ok) throw new Error("Erro ao buscar os testes.");
      const data = await response.json();
      setTests(data.tests); // 👈 CORREÇÃO AQUI
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  fetchTests();
}, [routineId]);

  if (loading) return <p>Carregando testes...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!tests.length) return <><DefaultHeader title={"Routine Tests"} /><p>Nenhum teste encontrado.</p>;</>

  return (
    <>
      <DefaultHeader title={"Routine Tests"} />
      <div className={styles.container}>
        <h1>Testes da Rotina #{routineId}</h1>
        <div className={styles.testList}>
          {tests.map((test) => (
            <TestCard test={test} r_id={routineId}/>
          ))}
        </div>
      </div>
    </>
  );
}
