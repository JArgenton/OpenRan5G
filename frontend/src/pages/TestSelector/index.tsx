import { useState } from "react";
import ToggleButton from "../../Components/ToggleButton";
import style from "./style.module.css"

export default function TestSelector() {
  const [selecionados, setSelecionados] = useState<string[]>([]);
  const [testType, setTestType] = useState<string>()
  const [ip, setIp] = useState<string>("")
  const [udp, setUdp] = useState<boolean>(false)
  const [tcp, setTcp] = useState<boolean>(false)
  const [deflt, setDefault] = useState<boolean>(false)

  const handlePropSelector = (label: string, ativo: boolean) => {
    setSelecionados(prev => {
      if (ativo) {
        return [...prev, label]; // adiciona
      } else {
        return prev.filter(item => item !== label); // remove
      }
    });
  }

  function handleDefaultButton(label: string, ativo: boolean){
    if(ativo)
      setDefault(true)
    else
      setDefault(false)

    setSelecionados([])
  }

  function handleTypeSelector(label: string, ativo: boolean){
    if (label === "TCP" || label === "UDP") {
      if(ativo)
        setTestType(() => (label));
        if(label === "TCP")
          setUdp(false)
        else
          setTcp(false)
      return;
    }
  }

  function handleRunButton(){
    console.log(selecionados, ip, testType)
    setIp("")
  }

  return (
    <div className={style.wrapper}>
      <ToggleButton label="Default Test" onToggle={handleDefaultButton} />
      
      <div>
          { (!deflt && (
            <>
              <h2 className={style.sectionTitle}>Select test parameters</h2>
              <div className={style.parameters}>
                <ToggleButton label="Ping" onToggle={handlePropSelector} />
                <ToggleButton label="Jitter" onToggle={handlePropSelector} />
                <ToggleButton label="Packet Loss" onToggle={handlePropSelector} />
              </div>
            </>
          ))}
    
        {(selecionados.find((value) => value === "Jitter") && !selecionados.find((value) => value === "Packet Loss")) && (
          <>
            <h2 className={style.sectionTitle}>Select test type</h2>
            <div className={style.parameters}>
              <ToggleButton label="TCP" onToggle={handleTypeSelector} active={tcp} setActive={setTcp} />
              <ToggleButton label="UDP" onToggle={handleTypeSelector} active={udp} setActive={setUdp}/>
            </div>
          </>
        )}

        <div className={style.inputWrapper}>
            <input
            type="text"
            id="ip"
            className={style.ipInput}
            value={ip}
            onChange={(e) => setIp(e.target.value)}
            placeholder="Enter IP address"
            />
        </div>
      </div>
      
      <div className={style.actions}>
        <button
          className={style.actionButton}
          onClick={handleRunButton}
        >
          Run test
        </button>
      </div>
    </div>
  )
}