import { useState } from "react";
import ToggleButton from "../../Components/ToggleButton";
import style from "./style.module.css"
import DefaultHeader from "../../Components/DefaultHeader";
import DefaultButton from "../../Components/DefaultButton";

export default function TestSelector() {
  const [selecionados, setSelecionados] = useState<string[]>([]);
  const [ip, setIp] = useState<string>("")
  const [npackets, setNpackets] = useState<string>("")
  const [udp, setUdp] = useState<boolean>(false)
  const [tcp, setTcp] = useState<boolean>(false)
  const [deflt, setDefault] = useState<boolean>(false)
  const [ntests, setNtests] = useState<string>("")

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
        if(label === "TCP")
          setUdp(false)
        else
          setTcp(false)
      return;
    }
  }

  function handleRunButton(){
    console.log(selecionados, ip, udp, tcp)
    setIp("")
  }

  return (
    <>
      <DefaultHeader title="Run Test"/>
      <div className={style.wrapper}>
      <ToggleButton label="Default Test" onToggle={handleDefaultButton} />
      
      <div>
          { (!deflt && (
            <>
              <h2 className={style.sectionTitle}>Select test type</h2>
              <div className={style.parameters}>
                <ToggleButton label="Ping" onToggle={handlePropSelector} />
                <ToggleButton label="TCP" onToggle={handleTypeSelector} active={tcp} setActive={setTcp} />
                <ToggleButton label="UDP" onToggle={handleTypeSelector} active={udp} setActive={setUdp}/>
                
              </div>
            </>
          ))}

        {(tcp || udp) && (
          <>
            <h2 className={style.sectionTitle}>Select test parameters</h2>
            <div className={style.parameters}>
              <ToggleButton label="Jitter" onToggle={handlePropSelector} />
              {udp && (
                <>
                  <ToggleButton label="Packet Loss" onToggle={handlePropSelector} />
                </>
              )}
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

        <div className={style.inputWrapper}>
            <input
            type="text"
            id="ntests"
            className={style.ipInput}
            value={ntests}
            onChange={(e) => setNtests(e.target.value)}
            placeholder="Enter number of tests"
            />
        </div>

        {udp && !deflt && (
          <div className={style.inputWrapper}>
              <input
              type="text"
              id="npackets"
              className={style.ipInput}
              value={npackets}
              onChange={(e) => setNpackets(e.target.value)}
              placeholder="Select number of packets"
              />
          </div>
        )}
      </div>
      
      <div className={style.actions}>
        <DefaultButton text="Run Test" callback={handleRunButton} />
      </div>
    </div>
    </>
    
  )
}