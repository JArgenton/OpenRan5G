# OpenRan5G
Scripts utilizados para testar e avaliar a qualidade de rede OpenRan5G

Mapa do repositorio

vpn_network_tests/
├── tests/
│   ├── iperf3_test.py      # Script para realizar testes com iperf3
│   ├── ping_test.py        # Script para realizar testes com ping
│   ├── netperf_test.py     # Script para realizar testes com netperf
│   └── traceroute_test.py  # (Opcional) Script para realizar testes de traceroute
├── automation/
│   ├── run_tests.py        # Automatiza a execução de uma sequência de testes
│   └── config.json         # Arquivo de configuração com a sequência de testes
├── visualization/
│   ├── plot_graphs.py      # Gera gráficos e ilustrações dos dados
│   └── templates/          # (Opcional) Modelos para relatórios automatizados
└── README.md               # Documentação do projeto
