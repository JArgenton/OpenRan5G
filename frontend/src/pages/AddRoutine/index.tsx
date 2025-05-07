import { useState } from "react"
import DefaultButton from "../../Components/DefaultButton"
import DefaultHeader from "../../Components/DefaultHeader"
import TestForm from "../../Components/TestForm"
import { Test } from "../../Components/TestForm"
import style from "./style.module.css"

export default function AddRoutine(){
    const [tests, setTests] = useState<Test[]>([])
    const [time, setTime] = useState<string>("")

    function handleTestForm(test: Test[]){
        setTests([...tests, ...test])
    }

    

    return(
        <>
            <DefaultHeader title="Routine" />

            <div style={{ display: 'flex', height: '100vh' }}>
                <section style={{ width: '50%', padding: '2rem' }}>
                    <h2 style={{ paddingLeft: "5%" }}>Add new test routine</h2>
                    <TestForm onSubmit={handleTestForm} text="Add"/>
                </section>

                <section style={{ width: '50%', padding: '2rem', borderLeft: '1px solid #444' }}>
                    <h2>Current Routine</h2>
                    {tests.map((test) => {
                        let type: string = ""
                        test.udp ? type += "UDP " : null
                        test.tcp ? type += "TCP " : null
                        test.ping ? type += "PING " : null
                        test.default ? type = "Default Test" : null
                        return(
                            <>
                                <div>
                                    <h2>{type}</h2>
                                    <p>Ip: {test.ip}</p>
                                    {test.npackets && (
                                        <>
                                            <p>Packet number {test.npackets}</p>
                                        </>
                                    )}
                                    <hr />
                                </div>
                            </>
                        )
                    })}
                    <div className={style.inputWrapper}>
                        <input
                        type="text"
                        className={style.ipInput}
                        value={time}
                        onChange={(e) => setTime(e.target.value)}
                        placeholder="Enter the test time"
                        />
                        
                    </div>
                    <div className={style.buttonWrapper}>
                        <DefaultButton text="Save Routine" callback={() => {}} />
                    </div>
                    
                </section>
            </div>
        </>
    )
}