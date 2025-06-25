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
  pingPackets: string,
  protocol: string,
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
  const [packetSize, setPacketSize] = useState<string>("")
  const [PingPackets, setPingPackets] = useState<string>("")

  const [error, setError] = useState<string>("");

  const handleTypeSelector = (label: string, ativo: boolean) => {
    if (label === "TCP" || label === "UDP") {
      if (ativo) {
        if (label === "TCP") setUdp(false);
        else setTcp(false);
      }
    } else {
      if (!ativo) setPingPackets("-1")
      setPing(ativo)
    }
  };

  const validateFields = (): boolean => {
    if (!ip.match(/^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)(\.|$)){4}$/)) {
      setError("Invalid IP address");
      return false;
    }

    if (tcp === false && udp === false && ping === false) {
      setError("Select at least 1 type of test");
      return false;
    }

    if ((tcp || udp) && (!packetSize || isNaN(Number(packetSize)) || Number(packetSize) <= 0)) {
      setError("Packet size must be a positive number");
      return false;
    }

    if ((tcp || udp) && (!duration || isNaN(Number(duration)) || Number(duration) <= 0)) {
      setError("Duration must be a positive number");
      return false;
    }

    if (ping && (!PingPackets || isNaN(Number(PingPackets)) || Number(PingPackets) <= 0)) {
      setError("Number of ping packets must be a positive number");
      return false;
    }

    const n = Number(ntests);
    if (!ntests || isNaN(n) || n < 1 || n > 10) {
      setError("Number of tests must be between 1 and 10");
      return false;
    }

    setError("");
    return true;
  };

  const handleRunButton = () => {
    if (!validateFields()) return;

    let protocol
    if (tcp) protocol = 'TCP'
    else if (udp) protocol = 'UDP'
    else protocol = 'none'

    const test: Test = {
      ip,
      duration: duration === "" ? "0" : duration,
      packetSize: packetSize === "" ? "0" : packetSize,
      pingPackets: PingPackets === "" ? "0" : PingPackets,
      protocol,
      ping,
      default: false
    }

    const tests: Test[] = []
    const n = Math.min(Number(ntests), 10)
    for (let i = 0; i < n; i++) {
      tests.push(test)
    }

    onSubmit(tests);
    setDuration("")
    setNtests("")
    setPingPackets("")
    setPacketSize("")
  };

  return (
    <>
      <div className={style.wrapper}>
        <div>
          <h2 className={style.sectionTitle}>Select test types</h2>
          <div className={style.parameters}>
            <ToggleButton label="Ping" onToggle={handleTypeSelector} />
            <ToggleButton label="TCP" onToggle={handleTypeSelector} active={tcp} setActive={setTcp} />
            <ToggleButton label="UDP" onToggle={handleTypeSelector} active={udp} setActive={setUdp} />
          </div>

          <div className={style.inputWrapper}>
            <input
              type="text"
              className={style.ipInput}
              value={ip}
              onChange={(e) => setIp(e.target.value)}
              placeholder="Enter IP address"
            />
          </div>

          {(tcp || udp) && (
            <>
              <div className={style.inputWrapper}>
                <input
                  type="text"
                  className={style.ipInput}
                  value={packetSize}
                  onChange={(e) => setPacketSize(e.target.value)}
                  placeholder="Select packet size"
                />
              </div>
              <div className={style.inputWrapper}>
                <input
                  type="text"
                  className={style.ipInput}
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                  placeholder="Select test duration"
                />
              </div>
            </>
          )}

          {ping && (
            <div className={style.inputWrapper}>
              <input
                type="text"
                className={style.ipInput}
                value={PingPackets}
                onChange={(e) => setPingPackets(e.target.value)}
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

        {error && (
          <div style={{ color: "red", marginBottom: "1rem" , textAlign: "center"}}>
            {error}
          </div>
        )}

        <div className={style.actions}>
          <DefaultButton text={text} callback={handleRunButton} />
        </div>
      </div>
    </>
  );
}
