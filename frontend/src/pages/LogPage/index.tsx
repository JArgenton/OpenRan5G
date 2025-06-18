import DefaultHeader from "../../Components/DefaultHeader";
import { useEffect, useState } from "react";
import style from "./style.module.css"; 
import { ResultJson } from "../../Components/ResultCard";
import  ResultCard  from "../../Components/ResultCard";
import { ClipLoader } from "react-spinners";


export default function LogPage(){

    const [result, setResult] = useState<{ results: ResultJson[] } | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

        useEffect(() => {
        async function runTests() {
            const res = await fetch("http://localhost:8000/api/log", {
            method: "GET",
            headers: { "Content-Type": "application/json" },
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

    if(loading){
        return(
            <div className={style.loaderWrapper}>
                <div className={style.loaderWrapper}>
                    <div className={style.loaderBox}>
                        <ClipLoader size={60} color="#00bfff" />
                        <p>Carregando dados dos testes por favor aguarde...</p>
                    </div>
                </div>
            </div>
        )
    }


    return(
        <>
        <DefaultHeader title="Test Log" />
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
    )
}