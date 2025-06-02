import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { ClipLoader } from "react-spinners";
import style from "./style.module.css"; // <- CSS Module aqui

export default function ResultsPage() {
  const location = useLocation();
  const tests = location.state?.tests;

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const runTests = async () => {
      if (!tests) return;

      try {
        const response = await fetch("http://localhost:8000/api/tests", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(tests),
        });

        if (!response.ok) throw new Error("Erro ao chamar a API");

        const data = await response.json();
        setResult(data);
      } catch (error) {
        console.error("Erro ao rodar testes:", error);
      } finally {
        setLoading(false);
      }
    };

    runTests();
  }, [tests]);

  if (loading) {
    return (
      <div className={style.loaderContainer}>
        <ClipLoader size={60} color="#00bfff" />
        <p>Executando testes, por favor aguarde...</p>
      </div>
    );
  }

  return (
    <div className={style.resultContainer}>
      <h2>Resultados:</h2>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}

