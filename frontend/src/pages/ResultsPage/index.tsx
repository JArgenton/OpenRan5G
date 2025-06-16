import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { ClipLoader } from "react-spinners";
import  ResultCard  from "../../Components/ResultCard";
import style from "./style.module.css"; 
import { ResultJson } from "../../Components/ResultCard";
import DefaultHeader from "../../Components/DefaultHeader";

export default function ResultsPage() {
  const location = useLocation();
  const tests = location.state?.tests;

  const [result, setResult] = useState<{ results: ResultJson[] } | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function runTests() {
      if (!tests) return;
      console.log("[RUN TESTS] iniciando fetch", new Date().toISOString());

      const res = await fetch("http://localhost:8000/api/tests", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(tests),
      });

      console.log("[RUN TESTS] resposta recebida", res.status);

      const data = await res.json();
      if (!res.ok) {
        console.error("Erro ao buscar dados");
        setLoading(false);
        return;
      }
      
      console.log("[RUN TESTS] dados recebidos", data);

      setResult(data);
      setLoading(false);
    }

    runTests();
}, []);

  if (loading) {
  return (
    <div className={style.loaderWrapper}>
      <div className={style.loaderBox}>
        <ClipLoader size={60} color="#00bfff" />
        <p>Executando testes, por favor aguarde...</p>
      </div>
    </div>
  );
}

  return (
    <>
      <DefaultHeader title="Results" />
      <div className={style.resultContainer}>
        {result?.results && (
          <div className={style.cardList}>
            {result.results.map((r: ResultJson, idx: number) => (
              <ResultCard key={idx} test_result={r} />
            ))}
          </div>
        )}
      </div>
    </>
  );

}

