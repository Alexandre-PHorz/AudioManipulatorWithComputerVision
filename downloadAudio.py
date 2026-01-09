import yt_dlp
import os
import json

def baixar_melhor_audio_youtube(url_video, diretorio_saida = "music"):
    """
    Baixa o áudio de um vídeo do YouTube no melhor formato de áudio disponível. O formato será tipicamente .m4a ou similar.

    Args:
        url_video (str): A URL do vídeo do Youtube.
        diretorio_saida (str): O diretório onde o arquivo de áudio será salvo.
                               O padrão é 'music'.
        
    Returns:
        str: O caminho completo para o arquivo de áudio baixado, ou None se ocorrer algum erro.
    """

    if not os.path.exists(diretorio_saida):
        try:
            os.makedirs(diretorio_saida)
            print(f"Diretório '{diretorio_saida}' criado.'")
        except OSError as e:
            print(f"Erro ao criar diretório '{diretorio_saida}': {e}")
            return None
        
    # Configurações para o yt-dlp para baixar o melhor áudio sem conversão específica
    ydl_opts = {
        'format': 'bestaudio/best',  # Seleciona o melhor áudio-somente disponível
        'outtmpl': os.path.join(diretorio_saida, 'notwav.%(ext)s'), # Nomeia o arquivo com o título e sua extensão original
        'keepvideo': False,          # Não mantém arquivos de vídeo se um formato de vídeo for baixado temporariamente
        'noplaylist': True,          # Baixa apenas o vídeo especificado, não a playlist inteira
        'quiet': False,              # Mostra o output do yt-dlp
        'progress': True,            # Mostra barra de progresso
        'nocheckcertificate': True,  # Pode ajudar com alguns erros de SSL
        # NENHUM postprocessor para forçar a conversão para WAV ou outro formato específico.
        # O yt-dlp tentará salvar o áudio no formato em que é oferecido (ex: m4a, opus em webm).
    }

    nome_arquivo_final = None

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Iniciando download do melhor áudio para: {url_video}")
            # O método extract_info com download=True fará o download.
            info_dict = ydl.extract_info(url_video, download=True)

            nome_arquivo_final = ydl.prepare_filename(info_dict)

            if os.path.exists(nome_arquivo_final):
                print(f"\nDownload de áudio concluído com sucesso!")
                print(f"Formato do arquivo: .{nome_arquivo_final.split('.')[-1]}")
                print(f"Arquivo salvo em: {os.path.abspath(nome_arquivo_final)}")
                return os.path.abspath(nome_arquivo_final)
            else:
                print(f"\nErro: O arquivo de áudio esperado ({nome_arquivo_final}) não foi encontrado após o processo de download.")
                print("Verifique se houve mensagens de erro durante o download.")
                print(f"Arquivos encontrados no diretório de saída ('{diretorio_saida}'):")
                if os.path.exists(diretorio_saida):
                    for item in os.listdir(diretorio_saida):
                        print(f"  - {item}")
                else:
                    print("  (Diretório de saída não encontrado)")
                return None    
    except yt_dlp.utils.DownloadError as e:
        print(f"\nErro de download do yt-dlp: {e}")
        if "Unsupported URL" in str(e):
            print("A URL fornecida parece não ser suportada ou é inválida.")
        elif "Video unavailable" in str(e):
            print("O vídeo pode estar indisponível (privado, removido, restrição de idade/geográfica).")
        elif "HTTP Error 403" in str(e) or "Access Denied" in str(e):
            print("Acesso negado. O vídeo pode ser privado ou requerer login, ou o YouTube pode estar bloqueando o acesso programático.")
        else:
            print("Verifique a URL do vídeo e sua conexão com a internet. Algumas vezes, tentar novamente mais tarde pode funcionar.")
        return None
    except Exception as e:
        print(f"\nOcorreu um erro inesperado durante a execução: {e}")
        return None

with open('settings.json','r') as j:
    data = json.load(j)


if __name__ == "__main__":
    # 🔽🔽🔽 MODIFIQUE A LINHA ABAIXO PARA A URL DO VÍDEO DESEJADO 🔽🔽🔽
    url_do_video_youtube = data['music']['URL']
    # Exemplo: url_do_video_youtube = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Substitua por uma URL real
    # 🔼🔼🔼 MODIFIQUE A LINHA ACIMA PARA A URL DO VÍDEO DESEJADO 🔼🔼🔼

    pasta_de_destino = "music"

    if url_do_video_youtube == "URL_DO_SEU_VIDEO_AQUI" or not url_do_video_youtube.startswith("http"):
        print("******************************************************************************************")
        print("* POR FAVOR, EDITE O SCRIPT!                                                             *")
        print("* Abra este arquivo Python e altere a variável 'url_do_video_youtube'                    *")
        print("* para a URL completa do vídeo do YouTube que você deseja baixar.                        *")
        print("* Exemplo de como deve ficar no código:                                                  *")
        print("* url_do_video_youtube = \"https://www.youtube.com/watch?v=videoID\"                 *") # Exemplo com aspas corretas
        print("******************************************************************************************")
    else:
        print(f"Música para download (melhor áudio disponível): {url_do_video_youtube}")
        caminho_do_arquivo_audio = baixar_melhor_audio_youtube(url_do_video_youtube, pasta_de_destino)

        if caminho_do_arquivo_audio:
            print(f"\nDownload da música concluído com sucesso!")
            # A mensagem sobre o local e formato já é impressa dentro da função.
        else:
            print("\nFalha no download da música. Verifique as mensagens de erro acima.")