from ..database.resultados import ResultadosDAO

class Result:
    database = ResultadosDAO()
    def __init__(self):
        ...
        
    @staticmethod
    def load_results_data(where: str = "", select: str = ""):
        results_params = Result.database.get_results_params(where, select)
        formated_results = []
        #print(results_params)
        for result in results_params:
            formatted = Result.format_result_json(result)
            if formatted:  
                formated_results.append(formatted)
        return {"results": formated_results}
    
    @staticmethod
    def format_save_json(result, protocol, ping, id, server: str, routine_id: int = -1):
        
        obj = {}
        if routine_id != -1:
            obj["ROUTINE_ID"] = routine_id
        if protocol == "":
            obj["TIMESTAMP_RESULT"] =  result["latency"]["timestamp"]
        else:
            obj["TIMESTAMP_RESULT"] = result["bandwidth"]["timestamp"]
        obj["TEST_ID"] = id

        obj["SERVER"] = server

        if ping:
            obj["MIN_LATENCY"] = result["latency"]["results"]["min_latency_ms"]
            obj["AVG_LATENCY"] = result["latency"]["results"]["avg_latency_ms"]
            obj["MAX_LATENCY"] = result["latency"]["results"]["max_latency_ms"]
        
        if protocol == "UDP":
            obj["LOST_PACKETS"] = result["bandwidth"]["results"]["lost_packets"]
            obj["LOST_PERCENT"] = result["bandwidth"]["results"]["lost_percent"]
            obj["BITS_PER_SECOND"] = result["bandwidth"]["results"]["bits_per_second"]
            obj["BYTES_TRANSFERED"] = result["bandwidth"]["results"]["bytes_transferred"]
            obj["JITTER"] = result["bandwidth"]["results"]["Jitter"]

        if protocol == "TCP":
            obj["BITS_PER_SECOND"] = result["bandwidth"]["results"]["bits_per_second"]
            obj["BYTES_TRANSFERED"] = result["bandwidth"]["results"]["bytes_transferred"]
            obj["RETRANSMITS"] = result["bandwidth"]["results"]["retransmits"]
        
        return obj
    

    @staticmethod
    def format_result_json(row: tuple) -> dict:
        (
            _,              # RESULT_ID
            _,     # ROUTINE_ID
            _,              # TEST_ID
            timestamp,      # TIMESTAMP_RESULT
            server,
            min_latency,    # MIN_LATENCY
            avg_latency,    # AVG_LATENCY
            max_latency,    # MAX_LATENCY
            lost_packets,   # LOST_PACKETS
            lost_percent,   # LOST_PERCENT
            bits_per_second,# BITS_PER_SECOND
            bytes_transferred, # BYTES_TRANSFERED
            jitter,         # JITTER
            retransmits,    # RETRANSMITS
            protocol,       # PROTOCOL
            duration,       # DURATION_SECONDS
            packet_size,    # PACKET_SIZE
            packet_count    # PACKET_COUNT
        ) = row

        result: dict = {}

        # Latency (ping)
        if min_latency is not None and avg_latency is not None and max_latency is not None:
            result["latency"] = {
                "timestamp": timestamp,
                "test_type": "latency",
                "tool": "ping",
                "parameters": {
                    "target": server or "",
                    "packet_count": packet_count or 0
                },
                "results": {
                    "min_latency_ms": min_latency,
                    "avg_latency_ms": avg_latency,
                    "max_latency_ms": max_latency
                }
            }

        # Bandwidth (iperf3)
        if bits_per_second is not None and bytes_transferred is not None:
            bandwidth = {
                "timestamp": timestamp,
                "test_type": "bandwidth",
                "parameters": {
                    "server": server or "",
                    "duration_seconds": duration or 0,
                    "packet_size": packet_size or 0
                },
                "results": {}
            }

            if protocol and protocol.upper() == "UDP":
                bandwidth["protocol"] = "udp"
                bandwidth["results"] = {
                    "bits_per_second": bits_per_second,
                    "lost_packets": lost_packets or 0,
                    "lost_percent": lost_percent or 0,
                    "bytes_transferred": bytes_transferred,
                    "Jitter": jitter or 0,
                    "packets": packet_count or 0
                }

            elif protocol and protocol.upper() == "TCP":
                bandwidth["protocol"] = "tcp"
                bandwidth["results"] = {
                    "bits_per_second": bits_per_second,
                    "retransmits": retransmits or 0,
                    "bytes_transferred": bytes_transferred
                }

            result["bandwidth"] = bandwidth

        #print(result)

        return result

    