import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { ClipLoader } from "react-spinners";
import style from "./style.module.css"; // <- CSS Module aqui

export default function ResultsPage() {
  const location = useLocation();
  const tests = location.state?.tests;

  const [result, setResult] = useState(null);
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
    <div className={style.resultContainer}>
      <h2>Resultados:</h2>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}

