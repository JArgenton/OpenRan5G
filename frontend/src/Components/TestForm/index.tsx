import { useState } from "react";
import ToggleButton from "../../Components/ToggleButton";
import style from "./style.module.css"
import DefaultButton from "../../Components/DefaultButton";

interface TestFormProps {
  onSubmit: (test: Test[]) => void;
  text: string;
}

export interface Test {
  ip: string,
  npackets: string,
  tcp: boolean,
  udp: boolean,
  ping: boolean,
  default: boolean
}

export default function TestForm({ onSubmit, text }: TestFormProps) {
  const [ping, setPing] = useState<boolean>(false)
  const [ip, setIp] = useState("");
  const [npackets, setNpackets] = useState("");
  const [ntests, setNtests] = useState("");
  const [udp, setUdp] = useState(false);
  const [tcp, setTcp] = useState(false);
  const [deflt, setDefault] = useState(false);

  const handleDefaultButton = (_: string, ativo: boolean) => {
    setDefault(ativo);  
  };

  const handleTypeSelector = (label: string, ativo: boolean) => {
    if (label === "TCP" || label === "UDP") {
      if (ativo) {
        if (label === "TCP") setUdp(false);
        else setTcp(false);
      }
    }
    else{
      setPing(!ativo)
    }
  };

  const handleRunButton = () => {
    if (!ip || !ntests || (udp && !npackets)) {
        alert("Please fill in all required fields.");
        return;
    }
    
    const test: Test = {
      ip,
      npackets,
      tcp,
      udp,
      ping,
      default: deflt
    }
    const tests: Test[]= []
    for(let i=0; i< +ntests; i++){
      tests.push(test)
    }

    onSubmit(tests);
    setIp("");
    setNpackets("")
    setNtests("")
  };

  return (
    <>
      <div className={style.wrapper}>
        <ToggleButton label="Default Test" onToggle={handleDefaultButton} />
        <div>
          {!deflt && (
            <>
              <h2 className={style.sectionTitle}>Select test types</h2>
              
              <div className={style.parameters}>
                <ToggleButton label="Ping" onToggle={handleTypeSelector} />
                <ToggleButton label="TCP" onToggle={handleTypeSelector} active={tcp} setActive={setTcp} />
                <ToggleButton label="UDP" onToggle={handleTypeSelector} active={udp} setActive={setUdp} />
              </div>
            </>
          )}

          {udp && !deflt && (
            <div className={style.inputWrapper}>
              <input
                type="text"
                className={style.ipInput}
                value={npackets}
                onChange={(e) => setNpackets(e.target.value)}
                placeholder="Select number of packets"
              />
            </div>
          )}

          <div className={style.inputWrapper}>
            <input
              type="text"
              className={style.ipInput}
              value={ip}
              onChange={(e) => setIp(e.target.value)}
              placeholder="Enter IP address"
            />
          </div>

          <div className={style.inputWrapper}>
            <input
              type="text"
              className={style.ipInput}
              value={ntests}
              onChange={(e) => setNtests(e.target.value)}
              placeholder="Enter number of tests"
            />
          </div>
        </div>

        <div className={style.actions}>
          <DefaultButton text={text} callback={handleRunButton} />
        </div>
      </div>
    </>
  );
}


