import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import DefaultHeader from "../../Components/DefaultHeader";
import ResultCard from "../../Components/ResultCard";
import { ResultJson } from "../../Components/ResultCard";
import style from "./style.module.css";

export default function RoutineTests() {
  const { id } = useParams();
  const [tests, setTests] = useState<ResultJson[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchTests() {
      try {
        const res = await fetch(`http://localhost:8000/api/routine/${id}/tests`);
        const data = await res.json();
        setTests(data.tests || []);
      } catch (error) {
        console.error("Erro ao buscar testes:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchTests();
  }, [id]);

  return (
    <>
      <DefaultHeader title={`Testes da Rotina ${id}`} />
      <div className={style.resultContainer}>
        {loading ? (
          <p>Carregando testes...</p>
        ) : tests.length === 0 ? (
          <p>Nenhum teste encontrado.</p>
        ) : (
          tests.map((test, index) => (
            <ResultCard key={index} test_result={test} />
          ))
        )}
      </div>
    </>
  );
}
