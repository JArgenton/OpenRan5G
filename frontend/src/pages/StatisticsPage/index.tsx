// Atualização no React para usar os valores idênticos às colunas do banco

import DefaultHeader from "../../Components/DefaultHeader";
import { useState } from "react";
import style from "./style.module.css";
import DefaultButton from "../../Components/DefaultButton";

interface plotParams {
    server: string,
    routineName?: string,
    startDate?: string,
    finalDate?: string,
    xParam?: string,
    yParam: string
}

export default function StatisticsPage() {
    const [activeTab, setActiveTab] = useState<"Time interval" | "Routine">("Time interval");
    const [startDate, setStartDate] = useState<string>("");
    const [finalDate, setFinalDate] = useState<string>("");

    const [xParam, setXParam] = useState<string>("PACKET_SIZE");
    const [yParam, setYParam] = useState<string>("AVG_LATENCY");
    const [routineParam, setRoutineParam] = useState<string>("AVG_LATENCY");
    const [routineName, setRoutineName] = useState<string>("");
    const [server, setServer] = useState<string>("");

    const [plotUrl, setPlotUrl] = useState<string | null>(null);

    const entryParams = [
        { label: "Tamanho do pacote", value: "PACKET_SIZE" },
        { label: "Duração do teste", value: "DURATION_SECONDS" },
        { label: "Contagem de pacotes", value: "PACKET_COUNT" }
    ];

    const resultParams = [
        { label: "Latência mínima", value: "MIN_LATENCY" },
        { label: "Latência média", value: "AVG_LATENCY" },
        { label: "Latência máxima", value: "MAX_LATENCY" },
        { label: "Bits por segundo", value: "BITS_PER_SECOND" },
        { label: "Bytes transferidos", value: "BYTES_TRANSFERED" },
        { label: "Jitter", value: "JITTER" },
        { label: "Retransmissões", value: "RETRANSMITS" },
        { label: "Perda de pacotes (%)", value: "LOST_PERCENT" }
    ];

    async function handlePlotGraphic() {
        console.log("[RUN TESTS] iniciando fetch", new Date().toISOString());

        if(server === "" || (activeTab === "Time interval" && (startDate === "" || finalDate === "") || (activeTab === "Routine" && (routineName === "")))){
            console.log("Complete as informações corretamente")
            return
        }  

        let plotParams: plotParams = {
            server: "",
            yParam: ""
        };

        if (activeTab === "Routine") {
            plotParams = {
                server,
                routineName,
                yParam: routineParam
            };
        } else {
            plotParams = {
                server,
                startDate,
                finalDate,
                xParam,
                yParam,
            };
        }
        console.log(plotParams)

        const res = await fetch("http://localhost:8000/api/plotting", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(plotParams),
        });

        if (!res.ok) {
            console.error("Erro ao buscar gráfico");
            return;
        }

        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        setPlotUrl(url);
    }

    return (
        <>
            <DefaultHeader title="Statistics" />

            <div className={style.tabWrapper}>
                <div
                    className={`${style.tab} ${activeTab === "Time interval" ? style.activeTab : ""}`}
                    onClick={() => setActiveTab("Time interval")}
                >
                    Time interval
                </div>
                <div
                    className={`${style.tab} ${activeTab === "Routine" ? style.activeTab : ""}`}
                    onClick={() => setActiveTab("Routine")}
                >
                    Routine
                </div>
            </div>

            {!plotUrl && (
                <div className={style.formWrapper}>
                    <input
                        type="text"
                        placeholder="Server"
                        value={server}
                        onChange={(e) => setServer(e.target.value)}
                    />

                    {activeTab === "Time interval" && (
                        <>
                            <div className={style.inlineInputs}>
                                <div className={style.inputGroup}>
                                    <label>Start date:</label>
                                    <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
                                </div>
                                <div className={style.inputGroup}>
                                    <label>Final date:</label>
                                    <input type="date" value={finalDate} onChange={(e) => setFinalDate(e.target.value)} />
                                </div>
                            </div>

                            <div className={style.inputGroup}>
                                <label>Parâmetro de entrada (eixo X):</label>
                                <select value={xParam} onChange={(e) => setXParam(e.target.value)}>
                                    {entryParams.map((param) => (
                                        <option key={param.value} value={param.value}>{param.label}</option>
                                    ))}
                                </select>
                            </div>

                            <div className={style.inputGroup}>
                                <label>Parâmetro de saída (eixo Y):</label>
                                <select value={yParam} onChange={(e) => setYParam(e.target.value)}>
                                    {resultParams.map((param) => (
                                        <option key={param.value} value={param.value}>{param.label}</option>
                                    ))}
                                </select>
                            </div>
                        </>
                    )}

                    {activeTab === "Routine" && (
                        <>
                            <div className={style.inputGroup}>
                                <label>Nome da rotina:</label>
                                <input
                                    type="text"
                                    placeholder="Routine name"
                                    value={routineName}
                                    onChange={(e) => setRoutineName(e.target.value)}
                                />
                            </div>

                            <div className={style.inputGroup}>
                                <label>Parâmetro a ser estudado (eixo Y):</label>
                                <select value={routineParam} onChange={(e) => setRoutineParam(e.target.value)}>
                                    {resultParams.map((param) => (
                                        <option key={param.value} value={param.value}>{param.label}</option>
                                    ))}
                                </select>
                            </div>
                        </>
                    )}
                    <DefaultButton text="Plot Graphic" callback={handlePlotGraphic} />
                </div>
            )}

            {plotUrl && (
                <div style={{ marginTop: "2rem", textAlign: "center" }} onClick={() => setPlotUrl(null)}>
                    <img
                        src={plotUrl}
                        alt="Gráfico gerado"
                        style={{ maxWidth: "100%", border: "1px solid #2ecc71", borderRadius: "8px" }}
                    />
                </div>
            )}
        </>
    );
}