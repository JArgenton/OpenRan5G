interface BandwidthResultTCP {
  bits_per_second: number;
  retransmits: number;
  bytes_transferred: number;
}

interface BandwidthResultUDP {
  bits_per_second: number;
  lost_packets: number;
  lost_percent: number;
  bytes_transferred: number;
  Jitter: number;
  packets: number;
}

interface BandwidthTest {
  timestamp: string;
  test_type: "bandwidth";
  protocol: "tcp" | "udp";
  parameters: {
    server: string;
    duration_seconds: number;
    packet_size: number;
  };
  results: BandwidthResultTCP | BandwidthResultUDP;
}

interface LatencyTest {
  timestamp: string;
  test_type: "latency";
  tool: "ping";
  parameters: {
    target: string;
    packet_count: number;
  };
  results: {
    min_latency_ms: number;
    avg_latency_ms: number;
    max_latency_ms: number;
  };
}

export interface ResultJson {
  bandwidth?: BandwidthTest;
  latency?: LatencyTest;
}

interface ResultCardProps {
  test_result: ResultJson;
}

import styles from "./style.module.css";

export default function ResultCard({ test_result }: ResultCardProps) {
  const { bandwidth, latency } = test_result;
  const isUDP = bandwidth?.protocol === "udp";

  return (
    <div className={styles.card}>
      <h2 className={styles.title}>
        {bandwidth
          ? `Teste de ${bandwidth.protocol.toUpperCase()}`
          : "Teste de Latência (Ping)"}
      </h2>

      {bandwidth && (
        <>
          <div className={styles.pair}>
            <span className={styles.label}>Timestamp:</span>{" "}
            <span className={styles.value}>{bandwidth.timestamp}</span>
          </div>
          <div className={styles.pair}>
            <span className={styles.label}>Servidor:</span>{" "}
            <span className={styles.value}>{bandwidth.parameters.server}</span>
          </div>
          <div className={styles.pair}>
            <span className={styles.label}>Duração:</span>{" "}
            <span className={styles.value}>{bandwidth.parameters.duration_seconds}s</span>
          </div>
          <div className={styles.pair}>
            <span className={styles.label}>Tamanho do pacote:</span>{" "}
            <span className={styles.value}>{bandwidth.parameters.packet_size} bytes</span>
          </div>
          <div className={styles.pair}>
            <span className={styles.label}>Taxa de bits:</span>{" "}
            <span className={styles.value}>
              {(bandwidth.results.bits_per_second / 1e6).toFixed(2)} Mbps
            </span>
          </div>
          <div className={styles.pair}>
            <span className={styles.label}>Bytes transferidos:</span>{" "}
            <span className={styles.value}>
              {(bandwidth.results.bytes_transferred / 1024 / 1024).toFixed(2)} MB
            </span>
          </div>

          {isUDP ? (
            <>
              <div className={styles.pair}>
                <span className={styles.label}>Perda de pacotes:</span>{" "}
                <span className={styles.value}>
                  {(bandwidth.results as any).lost_percent}%
                </span>
              </div>
              <div className={styles.pair}>
                <span className={styles.label}>Jitter:</span>{" "}
                <span className={styles.value}>
                  {(bandwidth.results as any).Jitter.toFixed(3)} ms
                </span>
              </div>
            </>
          ) : (
            <div className={styles.pair}>
              <span className={styles.label}>Retransmissões:</span>{" "}
              <span className={styles.value}>
                {(bandwidth.results as any).retransmits}
              </span>
            </div>
          )}
        </>
      )}

      {latency && (
        <div className={styles.section}>
          <h3 className={styles.title}>Latência (Ping)</h3>
          <div className={styles.pair}>
            <span className={styles.label}>Destino:</span>{" "}
            <span className={styles.value}>{latency.parameters.target}</span>
          </div>
          <div className={styles.pair}>
            <span className={styles.label}>Timestamp:</span>{" "}
            <span className={styles.value}>{latency.timestamp}</span>
          </div>
          <div className={styles.pair}>
            <span className={styles.label}>Mínimo:</span>{" "}
            <span className={styles.value}>{latency.results.min_latency_ms} ms</span>
          </div>
          <div className={styles.pair}>
            <span className={styles.label}>Médio:</span>{" "}
            <span className={styles.value}>{latency.results.avg_latency_ms} ms</span>
          </div>
          <div className={styles.pair}>
            <span className={styles.label}>Máximo:</span>{" "}
            <span className={styles.value}>{latency.results.max_latency_ms} ms</span>
          </div>
        </div>
      )}
    </div>
  );
}
