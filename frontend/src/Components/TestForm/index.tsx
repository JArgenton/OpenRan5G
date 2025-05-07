import { useState } from "react";
import ToggleButton from "../../Components/ToggleButton";
import style from "./style.module.css"
import DefaultButton from "../../Components/DefaultButton";

interface TestFormProps {
  onSubmit: (parameters: string[], protocol: boolean[]) => void;
}

export default function TestForm({ onSubmit }: TestFormProps) {
  const [selecionados, setSelecionados] = useState<string[]>([]);
  const [ip, setIp] = useState("");
  const [npackets, setNpackets] = useState("");
  const [ntests, setNtests] = useState("");
  const [udp, setUdp] = useState(false);
  const [tcp, setTcp] = useState(false);
  const [deflt, setDefault] = useState(false);

  const handlePropSelector = (label: string, ativo: boolean) => {
    setSelecionados(prev =>
      ativo ? [...prev, label] : prev.filter(item => item !== label)
    );
  };

  const handleDefaultButton = (_: string, ativo: boolean) => {
    setDefault(ativo);
    setSelecionados([]);
  };

  const handleTypeSelector = (label: string, ativo: boolean) => {
    if (label === "TCP" || label === "UDP") {
      if (ativo) {
        if (label === "TCP") setUdp(false);
        else setTcp(false);
      }
    }
  };

  const handleRunButton = () => {
    if (!ip || !ntests || (udp && !npackets)) {
        alert("Please fill in all required fields.");
        return;
    }
    onSubmit([ip, npackets, ntests, ...selecionados], [tcp, udp, deflt]);
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
                <ToggleButton label="Ping" onToggle={handlePropSelector} />
                <ToggleButton label="TCP" onToggle={handleTypeSelector} active={tcp} setActive={setTcp} />
                <ToggleButton label="UDP" onToggle={handleTypeSelector} active={udp} setActive={setUdp} />
              </div>
            </>
          )}

          {(tcp || udp) && (
            <>
              <h2 className={style.sectionTitle}>Select test parameters</h2>
              <div className={style.parameters}>
                <ToggleButton label="Jitter" onToggle={handlePropSelector} />
                {udp && <ToggleButton label="Packet Loss" onToggle={handlePropSelector} />}
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
          <DefaultButton text="Run Test" callback={handleRunButton} />
        </div>
      </div>
    </>
  );
}


