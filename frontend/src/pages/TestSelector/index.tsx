import { useState } from "react";
import ToggleButton from "../../Components/ToggleButton";
import style from "./style.module.css"

export default function TestSelector() {
  const [selecionados, setSelecionados] = useState<string[]>([]);
  const [ip, setIp] = useState<string>("")

  const atualizarSelecao = (label: string, ativo: boolean) => {
    setSelecionados(prev => {
      if (ativo) {
        return [...prev, label]; // adiciona
      } else {
        return prev.filter(item => item !== label); // remove
      }
    });
  };

  function handleRunButton(){
    console.log(selecionados, ip)
    setIp("")
  }

  return (
    <div className={style.wrapper}>
      <div>
        <h2 className={style.sectionTitle}>Select test parameters</h2>
        <div className={style.parameters}>
          <ToggleButton label="Ping" onToggle={atualizarSelecao} />
          <ToggleButton label="Jitter" onToggle={atualizarSelecao} />
          <ToggleButton label="Packet Loss" onToggle={atualizarSelecao} />
        </div>
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