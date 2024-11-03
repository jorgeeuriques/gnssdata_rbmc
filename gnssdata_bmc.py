import requests
import os
from datetime import datetime, timedelta
import gzip
import shutil
import subprocess

#Automatização da obteção de dados RINEX a partir da RBMC
#Padronização dos arquivos conforme requisitos de modelagem GNSS-IR pelo algoritmo Nievinski e Larson (2014a,b,c,d)
#Consultar/citar Euriques et al 2024 Soil Moisture estimation by GNSS-IR from Active Stations: Case Study – RBMC/IBGE, UFPR station

# 1 - Definir as datas de início e fim (formato: AAAA-MM-DD)
start_date = "2024-01-01"#Data de início da campanha
end_date = "2024-01-02"#Data de fim da campanha

# 2 - Nome da estação (alterar os 4 primeiros dígitos conforme código IBGE)
station = "UFPR00BRA"

# Convertendo as datas para objetos datetime
start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

# 3 - Caminho para a ferramenta crx2rnx (Atenção para o sentido das barras)
crx2rnx_path = "G:/Meu Drive/2024/5 TESE/CAP 5 RBMC UFPR/crx2rnx"

# 4 - Caminho para a ferramenta GFZ (para conversão)
gfzrnx_path = "G:/Meu Drive/2024/5 TESE/CAP 5 RBMC UFPR/gfzrnx"

# Iterando sobre as datas no intervalo
current_date_dt = start_date_dt
while current_date_dt <= end_date_dt:
    # Obtendo o ano e o DOY (Dia do Ano)
    year = current_date_dt.strftime('%Y')
    doy = current_date_dt.strftime('%j')
    
    # Construindo o nome do arquivo e a URL
    file_name = f"{station}_R_{year}{doy}0000_01D_15S_MO.crx.gz"
    base_url = "https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados_RINEX3/"
    url = f"{base_url}{year}/{doy}/{file_name}"
    
    # Caminho completo para o arquivo .gz
    gz_file_path = os.path.join(os.getcwd(), file_name)
    
    # Verificando se o arquivo já foi baixado
    if not os.path.isfile(gz_file_path):
        try:
            # Baixando o arquivo
            response = requests.get(url)
            response.raise_for_status()
            with open(gz_file_path, 'wb') as f:
                f.write(response.content)
            print(f"Download de {file_name} concluído!")
        except requests.RequestException as e:
            print(f"Falha ao baixar {file_name}. Erro: {e}")
            current_date_dt += timedelta(days=1)
            continue  # Passa para o próximo dia

    # Descompactando o arquivo .gz para .crx
    crx_file_name = gz_file_path[:-3]  # Remove a extensão .gz
    if not os.path.isfile(crx_file_name):
        try:
            with gzip.open(gz_file_path, 'rb') as f_in:
                with open(crx_file_name, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"Arquivo {crx_file_name} descompactado com sucesso!")
        except Exception as e:
            print(f"Falha ao descompactar {gz_file_path}. Erro: {e}")
            current_date_dt += timedelta(days=1)
            continue  # Passa para o próximo dia

    # Convertendo o arquivo .crx para .rnx
    rnx_file_name = crx_file_name[:-4] + ".rnx"
    if not os.path.isfile(rnx_file_name):
        # Verificando se o arquivo é um CRX antes de converter
        if crx_file_name.endswith('.crx'):
            # Construindo o comando de conversão
            command = [crx2rnx_path, crx_file_name]
            print(f"Executando comando: {' '.join(command)}")
            
            # Executando o comando de conversão
            try:
                result = subprocess.run(command, check=True, capture_output=True, text=True)
                print(f"Arquivo {rnx_file_name} convertido com sucesso!")
                print("Saída do comando:", result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Falha ao converter {crx_file_name}. Erro: {e}")
                print("Saída do comando:", e.output)
            except Exception as e:
                print(f"Ocorreu um erro inesperado: {e}")
        else:
            print(f"O arquivo {crx_file_name} não é um arquivo CRX válido para conversão.")

    # Passando para o próximo dia
    current_date_dt += timedelta(days=1)


# 5 - Indicar o diretório para efetuar a renomeação e filtragem final
rnx_folder_path = "G:/Meu Drive/2024/5 TESE/CAP 5 RBMC UFPR/"

# Iterando sobre os arquivos na pasta
for file_name in os.listdir(rnx_folder_path):
    if file_name.endswith(".rnx"):
        # Caminho completo para o arquivo .rnx
        rnx_file_path = os.path.join(rnx_folder_path, file_name)

        # Extraindo os dois últimos dígitos do ano para a extensão
        year_suffix = file_name[14:16]
        output_extension = f".{year_suffix}o"

        # Construindo o nome de saída com a extensão correta
        output_file_name = file_name[:-4] + output_extension
        output_file_path = os.path.join(rnx_folder_path, output_file_name)

        # Executando a conversão com o gfzrnx
        conversion_command = f'"{gfzrnx_path}" -finp "{rnx_file_path}" -fout "{output_file_path}"'
        print(f"Executando comando: {conversion_command}")
        result = subprocess.run(conversion_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Arquivo {output_file_name} convertido com sucesso!")

            # Renomeando o arquivo 
            new_name = f"ufpr{file_name[16:20]}{output_extension}"
            new_file_path = os.path.join(rnx_folder_path, new_name)

            # Verificando se o arquivo com o novo nome já existe
            if os.path.isfile(new_file_path):
                print(f"O arquivo {new_file_path} já existe. Removendo o arquivo existente.")
                os.remove(new_file_path)

            # Renomeando o arquivo
            os.rename(output_file_path, new_file_path)
            print(f"Arquivo renomeado para {new_name}")

            # Filtragem final dos dados (Manter apenas GPS-G e Glonass-R )
            filter_command = f'"{gfzrnx_path}" -finp "{new_file_path}" -fout "{new_file_path}" -satsys GR -f'
            print(f"Executando comando de filtragem: {filter_command}")
            filter_result = subprocess.run(filter_command, shell=True, capture_output=True, text=True)

            if filter_result.returncode == 0:
                print(f"Arquivo {new_file_path} filtrado com sucesso!")
            else:
                print(f"Falha ao filtrar {new_file_path}. Erro: {filter_result.stderr}")
        else:
            print(f"Falha ao converter {rnx_file_path}. Erro: {result.stderr}")

print("Processo de conversão, renomeação e filtragem concluído!")
