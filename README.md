# Automação para obtenção de dados GNSS de Estações da RBMC

Este repositório contém um script Python que automatiza o processo de download, descompactação, conversão e filtragem de dados GNSS RINEX com estações da Rede Brasileira de Monitoramento Contínuo dos Sistemas GNSS (RBMC/IBGE).

### Requisitos
Este script foi desenvolvido para automatizar o acesso a dados gnss no formato RINEX.
Adaptações complementares padronizam os dados conforme requisitos do algoritmo para modelagem GNSS-IR desenvolvido por Nievinski e Larson (2014a, b, c, d).
Maiores detalhes em:
> Euriques et al., 2024. *Soil Moisture Estimation by GNSS-IR from Active Stations: Case Study – RBMC/IBGE, UFPR Station*


### Funcionalidades
1. **Download de Dados RINEX**: Realiza o download automático dos arquivos RINEX compactados (.crx.gz) das estações da RBMC para o intervalo de datas definido.
2. **Descompactação e Conversão de Arquivos**:
   - Descompacta arquivos `.crx.gz` para `.crx`.
   - Converte arquivos `.crx` para `.rnx` usando a ferramenta `crx2rnx`.
3. **Renomeação e Filtragem de Arquivos**:
   - Converte os arquivos `.rnx` para o formato `.oyy` (RINEX de observação, yy indica o ano)usando a ferramenta `gfzrnx`.
   - Renomeia os arquivos para o padrão especificado (ssssdoy0.0yy), em que s é o código da estação, seguido o day of year, e o dígito 0 para arquivo de 24h
   - Filtra os dados para manter apenas observações dos sistemas GPS (G) e Glonass (R).

### Estrutura do Código
- **Definição do Intervalo de Datas e Estação**: O usuário define as datas de início e fim e o nome da estação RBMC.
- **Download e Descompactação**: O script baixa os arquivos e os descompacta.
- **Conversão e Renomeação**: Converte arquivos para `.rnx` e, em seguida, para `.oyy`, renomeando-os conforme especificado.
- **Filtragem Final**: Filtra para manter observações apenas dos satélites GPS e Glonass.

### Pré-requisitos

Para executar este script, você precisará de:
- Python 3.x com as bibliotecas `requests`, `os`, `datetime`, `gzip`, `shutil`, e `subprocess`.
- A ferramenta `crx2rnx` instalada e disponível no sistema.
- A ferramenta `gfzrnx` instalada e disponível no sistema.
- Acesso à internet para baixar os arquivos da RBMC.

### Instruções de Uso

1. **Configuração do Script**:
   - Defina as datas de início e fim da campanha, em formato `AAAA-MM-DD`.
   - Especifique o código da estação RBMC (os quatro primeiros caracteres).
   - Informe o caminho para a ferramenta `crx2rnx` e para o `gfzrnx` no script.

2. **Executando o Script**:
   Execute o script no terminal ou em um ambiente Python:

   ```bash
   python gnssdata_rbmc.py
   
3. **Resultado**:
	- Os arquivos RINEX serão baixados, descompactados, convertidos e renomeados conforme o padrão esperado.
	- Será gerada uma saída com mensagens de status para cada etapa do processo.
	
Estrutura do Projeto
├── gnssdatarbmc.py             # Script principal para download e conversão de dados GNSS
├── README.md                   # Documentação do projeto
└── dados/                      # Diretório para salvar os dados convertidos

Observações
Aviso: Certifique-se de que os caminhos dos executáveis crx2rnx e gfzrnx estejam corretos para evitar erros de execução.
Filtragem Final: A filtragem para manter apenas GPS e Glonass é aplicada como última etapa.

Autor
Desenvolvido por [Euriques et al., 2024. *Soil Moisture Estimation by GNSS-IR from Active Stations: Case Study – RBMC/IBGE, UFPR Station*] 

Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.




   
   
