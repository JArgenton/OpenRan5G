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
  duration: string,
  packetSize: string,
  bandwidth: string,
  pingPackets: string,
  tcp: boolean,
  udp: boolean,
  ping: boolean,
  default: boolean
}

export default function TestForm({ onSubmit, text }: TestFormProps) {
  const [ping, setPing] = useState<boolean>(false)
  const [ip, setIp] = useState<string>("");
  const [duration, setDuration] = useState<string>("");
  const [ntests, setNtests] = useState<string>("");
  const [udp, setUdp] = useState<boolean>(false);
  const [tcp, setTcp] = useState<boolean>(false);
  const [deflt, setDefault] = useState<boolean>(false);
  const [packetSize, setPacketSize] = useState<string>("")
  const [count, setCount] = useState<string>("")
  const [bandwidth, setBandwidth] = useState<string>("")

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
      setPing(ativo)
    }
  };

  const handleRunButton = () => {
    const test: Test = {
      ip,
      duration,
      packetSize,
      bandwidth,
      pingPackets: count,
      tcp,
      udp,
      ping,
      default: deflt
    }
    const tests: Test[]= []
    const n = +ntests < 10 ? +ntests : 10
    for(let i=0; i< +n; i++){
      tests.push(test)
    }

    onSubmit(tests);
    setIp("");
    setDuration("")
    setNtests("")
    setBandwidth("")
    setCount("")
    setPacketSize("")
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
            <>
              <div className={style.inputWrapper}>
                <input
                  type="text"
                  className={style.ipInput}
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                  placeholder="Select test duration"
                />
              </div>
              <div className={style.inputWrapper}>
                <input
                  type="text"
                  className={style.ipInput}
                  value={packetSize}
                  onChange={(e) => setPacketSize(e.target.value)}
                  placeholder="Select packet size"
                />
              </div>
            </>
          )}
          {(tcp || udp) && !deflt && (
            <>
              <div className={style.inputWrapper}>
                <input
                  type="text"
                  className={style.ipInput}
                  value={bandwidth}
                  onChange={(e) => setBandwidth(e.target.value)}
                  placeholder="Enter bandwidth"
                />
              </div>
            </>
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

          {ping && !deflt && (
              <div className={style.inputWrapper}>
                <input
                  type="text"
                  className={style.ipInput}
                  value={count}
                  onChange={(e) => setCount(e.target.value)}
                  placeholder="Number of ping packets"
                />
              </div>
          )}
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


