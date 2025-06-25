import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import ResultCard from "../../Components/ResultCard";
import { ResultJson } from "../../Components/ResultCard";
import styles from "./style.module.css";
import DefaultHeader from "../../Components/DefaultHeader";

export default function TestResultPage() {
  const { testId, routineId } = useParams<{ testId: string; routineId: string }>();
  const [results, setResults] = useState<ResultJson[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/results/${testId}/${routineId}`);
        console.log("teste")
        if (!res.ok) throw new Error("Erro ao buscar resultados.");
        const data = await res.json();
        console.log(data.results)
        setResults(data.results || []);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
      
    };

    if (testId && routineId) {
      fetchResults();
    }
  }, [testId, routineId]);

  if (loading) return <p className={styles.loading}>Carregando resultados...</p>;
  if (!results.length) return <><DefaultHeader title={"Test Results"} /><p className={styles.error}>Nenhum resultado encontrado.</p></>;

  return (
    <>
        <DefaultHeader title={"Test Results"} />
        <div className={styles.container}>
        {results.map((res, index) => (
            <ResultCard key={index} test_result={res} />
        ))}
        </div>
    </>
  );
}
