import { useState } from "react"
import DefaultButton from "../../Components/DefaultButton"
import DefaultHeader from "../../Components/DefaultHeader"
import TestForm, { Test } from "../../Components/TestForm"
import style from "./style.module.css"

interface routineParams{
    params: {
        routineName: string,
        server: string,
        time: string
    },
    tests: Test[]
}

export default function AddRoutine() {
    const [tests, setTests] = useState<Test[]>([])
    const [time, setTime] = useState<string>("")
    const [activeTab, setActiveTab] = useState<"client" | "server">("client")
    const [routineName, setRoutineName] = useState<string>("")

    async function handleSaveRoutine(){
        if(!tests.length || routineName === "" || time === "")
            return

        const rtParams: routineParams = {
            params: {
                routineName,
                server: tests[0].ip,
                time
            },
            tests
        }

        const res = await fetch("http://localhost:8000/api/routine", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(rtParams)
        });

        if(!res.ok) console.log("Erro ao inserir rotina")

        setTests([]);
        setRoutineName("");
        setTime("");
    }

    function handleTestForm(test: Test[]) {
        console.log(test)
        setTests([...tests, ...test])
        console.log(tests)
        //console.log(test)
    }

    return (
        <>
            <DefaultHeader title="Routine" />

            <div className={style.tabWrapper}>
                <div
                    className={`${style.tab} ${activeTab === "client" ? style.activeTab : ""}`}
                    onClick={() => setActiveTab("client")}
                >
                    Client Routine
                </div>
                <div
                    className={`${style.tab} ${activeTab === "server" ? style.activeTab : ""}`}
                    onClick={() => setActiveTab("server")}
                >
                    Server Routine
                </div>
            </div>

            {activeTab === "client" && (
                <div style={{ display: 'flex', height: '100vh' }}>
                    <section style={{ width: '50%', padding: '2rem' }}>
                        <h2 style={{ paddingLeft: "5%" }}>Add new test routine</h2>
                        <TestForm onSubmit={handleTestForm} text="Add" />
                    </section>

                    <section style={{ width: '50%', padding: '2rem', borderLeft: '1px solid #444' }}>
                        <h2>Current Routine</h2>
                        {tests.map((test, i) => {
                            let type = ""
                            if (test.default) type = "Default Test"
                            else {
                                if (test.ping) type += "PING "
                                if(test.protocol !== 'none') type += test.protocol.toUpperCase()
                            }

                            return (
                                <div key={i}>
                                    <h2>{type}</h2>
                                    <p>Ip: {test.ip}</p>
                                    {test.packetSize && <p>Packet size: {test.packetSize}</p>}
                                    <hr />
                                </div>
                            )
                        })}
                        <div className={style.inputWrapper}>
                            <input
                                type="time"
                                className={style.ipInput}
                                value={time}
                                onChange={(e) => setTime(e.target.value)}
                                placeholder="Enter the test time"
                            />
                        </div>
                        <div className={style.inputWrapper}>
                            <input
                                type="text"
                                className={style.ipInput}
                                value={routineName}
                                onChange={(e) => setRoutineName(e.target.value)}
                                placeholder="Routine name"
                            />
                        </div>
                        <div className={style.buttonWrapper}>
                            <DefaultButton text="Save Routine" callback={handleSaveRoutine} />
                        </div>
                    </section>
                </div>
            )}

            {activeTab === "server" && (
                <div style={{ padding: '2rem' }}>
                    <h2 style={{ marginBottom: "1.5rem", textAlign: "center" }}>Set routine time (server-side)</h2>
                    <div className={style.inputWrapper}>
                        <input
                            type="time"
                            className={style.ipInput}
                            value={time}
                            onChange={(e) => setTime(e.target.value)}
                            placeholder="Enter the test time"
                        />
                    </div>
                    <div className={style.buttonWrapper}>
                        <DefaultButton text="Save Server Routine" callback={() => {}} />
                    </div>
                </div>
            )}
        </>
    )
}