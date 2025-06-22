import DefaultHeader from "../../Components/DefaultHeader";
import { useState } from "react";
import style from "./style.module.css";
import DefaultButton from "../../Components/DefaultButton";

export default function StatisticsPage() {
    const [activeTab, setActiveTab] = useState<"Time interval" | "Routine">("Time interval");
    const [startDate, setStartDate] = useState<string>("");
    const [finalDate, setFinalDate] = useState<string>("");

    const [xParam, setXParam] = useState<string>("packet_size");
    const [yParam, setYParam] = useState<string>("avg_latency_ms");
    const [routineParam, setRoutineParam] = useState<string>("avg_latency_ms");
    const [routineID, setRoutineID] = useState<string>("");
    const [routineError, setRoutineError] = useState<string>("");
    const [server, setServer] = useState<string>("");

    const [plotUrl, setPlotUrl] = useState<string | null>(null);

    const entryParams = [
        { label: "Tamanho do pacote", value: "packet_size" },
        { label: "Duração do teste", value: "duration_seconds" },
        { label: "Contagem de pacotes", value: "packet_count" }
    ];

    const resultParams = [
        { label: "Latência mínima", value: "min_latency_ms" },
        { label: "Latência média", value: "avg_latency_ms" },
        { label: "Latência máxima", value: "max_latency_ms" },
        { label: "Bits por segundo", value: "bits_per_second" },
        { label: "Bytes transferidos", value: "bytes_transferred" },
        { label: "Jitter", value: "jitter" },
        { label: "Retransmissões", value: "retransmits" },
        { label: "Perda de pacotes (%)", value: "lost_percent" }
    ];

    function handleRoutineIdChange(value: string) {
        const onlyNumbers = value.replace(/\D/g, "");
        setRoutineID(onlyNumbers);

        const parsed = parseInt(onlyNumbers);
        if (!onlyNumbers || isNaN(parsed) || parsed < 0) {
            setRoutineError("Insira um ID numérico válido.");
        } else {
            setRoutineError("");
        }
    }

    async function handlePlotGraphic() {
        if ((routineID === "" && activeTab === "Routine") ||
            (activeTab === "Time interval" && (startDate === "" || finalDate === "")) ||
            !server.match(/^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)(\.|$)){4}$/)) {
            console.warn("Verificação de entrada falhou");
            return;
        }

        console.log("[RUN TESTS] iniciando fetch", new Date().toISOString());

        let plotParams = {};

        if (activeTab === "Routine") {
            plotParams = {
                server,
                RoutineID: routineID,
                RoutineParam: routineParam,
            };
        } else {
            plotParams = {
                server,
                StartDate: startDate,
                FinalDate: finalDate,
                xParam,
                yParam,
            };
        }

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
                                <label>ID da rotina:</label>
                                <input
                                    type="text"
                                    placeholder="Routine ID"
                                    value={routineID}
                                    onChange={(e) => handleRoutineIdChange(e.target.value)}
                                />
                                {routineError && <p style={{ color: "#e74c3c", marginTop: "4px" }}>{routineError}</p>}
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
                <div style={{ marginTop: "2rem", textAlign: "center" }}>
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
