import { useState } from "react"
import DefaultButton from "../../Components/DefaultButton"
import DefaultHeader from "../../Components/DefaultHeader"
import TestForm, { Test } from "../../Components/TestForm"
import style from "./style.module.css"
import { useNavigate } from "react-router-dom"


export default function TestSelector() {
  
  const [tests, setTests] = useState<Test[]>([])
  
  function handleTestForm(test: Test[]) {
    if(tests.length !== 0)
        test[0].ip === tests[0].ip ? setTests([...tests, ...test]) : console.log("Os endereços ips devem ser iguais")
    else
        setTests([...test])
  }

  const navigate = useNavigate();

  function handleRun() {
    if (tests.length === 0) {
        alert("Adicione ao menos um teste antes de continuar.");
        return;
    }

    console.log(tests)

    navigate("/results", { state: { tests } });
  }

  return (
    <>
      <DefaultHeader title="Run Tests" />
      <div style={{ display: 'flex', height: '100vh' }}>
        <section style={{ width: '50%', padding: '2rem' }}>
            <TestForm onSubmit={handleTestForm} text="Add" />
        </section>

        <section style={{ width: '50%', padding: '2rem', borderLeft: '1px solid #444' }}>
            <h2>Current Test</h2>
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
                        {test.packetSize !== "0" && <p>Packet size: {test.packetSize}</p>}
                        <hr />
                    </div>
                )
            })}
          
            <div className={style.buttonWrapper}>
                <DefaultButton text="Run tests" callback={handleRun} />
            </div>
        </section>
    </div>
    </>
  )
}