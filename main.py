import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import time
import random

from deep_translator import MyMemoryTranslator

duration = 3  # segundos de gravação
sample_rate = 44100

words_by_level = {
    "fácil": ["gato", "cachorro", "maçã", "leite", "sol", "lua", "flor", "carro", "livro", "bola"],
    "médio": ["casa", "escola", "amigo", "janela", "amarelo", "cidade", "cabeça", "música", "trabalho", "viagem"],
    "difícil": ["tecnologia", "universidade", "informação", "pronúncia", "imaginação", "telefone", "mundo", "literalmente", "dificuldade", "roupas"]
}

dificuldade = {
    "1": ["1", "fácil", "facil", "fácil", "Facil", "Fácil"],
    "2": ["2", "médio", "Médio", "medio", "Medio"],
    "3": ["3", "difícil", "Difícil", "dificil", "Dificil"]
}

idiomas = {
    "Inglês": ["1", "en-US", "en", "english", "English", "ingles", "Inglês", "Ingles", "inglês"],
    "Espanhol": ["2", "es-ES", "es", "spanish", "Spanish", "espanhol", "Espanhol"],
    "Alemão": ["3", "de-DE", "de", "german", "German", "alemão", "Alemão", "Alemao", "alemao"],
    "Italiano": ["4", "it-IT", "it", "italian", "Italian", "italiano", "Italiano"],
    "Japonês": ["5", "ja-JP", "ja", "japanese", "Japanese", "japonês", "Japonês", "Japones", "japones"]
}

print("""
                                   _______________________________________

                                   👋 Olá! Bem-vindo ao Translate Game 👋
                                   _______________________________________

Neste jogo, você receberá uma palavra em português e terá que traduzi-la para um idioma de sua escolha e pronunciá-la corretamente.
___________________________________________________________________________________________________________________________________

""")

vida = 3  # número de vidas do jogador
pontuação = 0  # pontuação inicial do jogador

input_level = input("""Escolha o nível de dificuldade:
1. Fácil
2. Médio
3. Difícil
Digite a dificuldade: """)

if input_level in dificuldade["1"] or input_level in dificuldade["2"] or input_level in dificuldade["3"]:
    if input_level in dificuldade["1"]:
        input_level = "Fácil"
    elif input_level in dificuldade["2"]:
        input_level = "Médio"
    elif input_level in dificuldade["3"]:
        input_level = "Difícil"

    print(f"Você escolheu o nível de dificuldade: {input_level}")

    input_target = input("""
Para começar, digite o idioma de saída para a tradução
Inglês
Espanhol
Alemão
Italiano
Japonês: """)

    if input_target in idiomas["Alemão"] or input_target in idiomas["Espanhol"] or input_target in idiomas["Inglês"] or input_target in idiomas["Italiano"] or input_target in idiomas["Japonês"]:
        if input_target in idiomas["Inglês"]:
            input_target = "Inglês"
        elif input_target in idiomas["Espanhol"]:
            input_target = "Espanhol"
        elif input_target in idiomas["Alemão"]:
            input_target = "Alemão"
        elif input_target in idiomas["Italiano"]:
            input_target = "Italiano"
        elif input_target in idiomas["Japonês"]:
            input_target = "Japonês"
        
        
        print(f"Você escolheu o idioma: {input_target}")
        time.sleep(1)

        if input_target in idiomas["Inglês"]:
            input_target = "en-US"
        elif input_target in idiomas["Espanhol"]:
            input_target = "es-ES"
        elif input_target in idiomas["Alemão"]:
            input_target = "de-DE"
        elif input_target in idiomas["Italiano"]:
            input_target = "it-IT"
        elif input_target in idiomas["Japonês"]:
            input_target = "ja-JP"

        while vida > 0 and pontuação < 5:
            if input_level in dificuldade["1"]:
                print("Você escolheu o nível de dificuldade: Fácil")
                time.sleep(0.5)
                words = words_by_level["fácil"]
                random_word = random.choice(words)
                words.remove(random_word)
                print(f"A palavra escolhida é: {random_word}")
                time.sleep(3)
                print("""Você terá 3 segundos para se preparar antes de gravar sua tradução...
                """)
                time.sleep(2.5)
                for j in range(3, 0, -1):
                    print(f"""Você tem {j} segundos para se preparar...
                    """)
                    time.sleep(1)
                print("Traduza a palavra...")
                recording = sd.rec(
                int(duration * sample_rate), # o número de amostras a serem registradas
                samplerate=sample_rate,      # taxa de amostras
                channels=1,                  # 1 significa gravação mono
                dtype="int16")               # tipo de dados para as amostras registradas
                for i in range(duration, 0, -1):
                    print(f"""Gravação concluída em {i} segundos...
                    """)
                    time.sleep(1)
                sd.wait()
                wav.write("teste.wav", sample_rate, recording)
                print("""Gravação concluída, estou reconhecendo...
                """)
                
                recognizer = sr.Recognizer()
                text = ""

                with sr.AudioFile("teste.wav") as source:
                    audio = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio, language=input_target)
                except sr.UnknownValueError:             # - se o Google não conseguiu entender a fala devido a ruídos ou silêncio
                    print("""A fala não pôde ser reconhecida.
                    
                    """)
                except sr.RequestError as e:             # - se não houver conexão com a Internet ou a API estiver indisponível
                    print(f"""Service error: {e}

        """)

                traducao = MyMemoryTranslator(source="pt-BR",target=input_target).translate(random_word)
                if text == traducao:
                    pontuação += 1
                    print(f"""✅ CORRETO!
    +1 ponto!

    {"❤️" * vida}  Vidas: {vida}
    🏆 Pontuação: {pontuação}

    resposta correta era: {traducao}
            """)
                    time.sleep(1)
                else:
                    vida -= 1
                    print(f"""❌ INCORRETO!

    {"❤️" * vida}  Vidas: {vida}
    🏆 Pontuação: {pontuação}

    A resposta correta era: {traducao}
            """)
                    time.sleep(1)
            elif input_level in dificuldade["2"]:
                    print("Você escolheu o nível de dificuldade: Médio")
                    time.sleep(0.5)
                    words = words_by_level["médio"]
                    random_word = random.choice(words)
                    words.remove(random_word)
                    print(f"A palavra escolhida é: {random_word}")
                    time.sleep(3)
                    print("""Você terá 3 segundos para se preparar antes de gravar sua tradução...
                    """)
                    time.sleep(1)
                    for j in range(3, 0, -1):
                        print(f"""Você tem {j} segundos para se preparar...
                        """)
                        time.sleep(1)
                    print("Traduza a palavra...")
                    recording = sd.rec(
                    int(duration * sample_rate), # o número de amostras a serem registradas
                    samplerate=sample_rate,      # taxa de amostras
                    channels=1,                  # 1 significa gravação mono
                    dtype="int16")               # tipo de dados para as amostras registradas
                    for i in range(duration, 0, -1):
                        print(f"""Gravação concluída em {i} segundos...
                        """)
                        time.sleep(1)
                    sd.wait()
                    wav.write("teste.wav", sample_rate, recording)
                    print("""Gravação concluída, estou reconhecendo...
                    """)
                    time.sleep(1)
                    
                    recognizer = sr.Recognizer()
                    text = ""
            
                    with sr.AudioFile("teste.wav") as source:
                        audio = recognizer.record(source)
                    try:
                        text = recognizer.recognize_google(audio, language=input_target)
                    except sr.UnknownValueError:             # - se o Google não conseguiu entender a fala devido a ruídos ou silêncio
                        print("""A fala não pôde ser reconhecida.
                        
                        """)
                    except sr.RequestError as e:             # - se não houver conexão com a Internet ou a API estiver indisponível
                        print(f"""Service error: {e}
            
            """)
            
                    traducao = MyMemoryTranslator(source="pt-BR",target=input_target).translate(random_word)
                    if text == traducao:
                        pontuação += 1
                        print(f"""✅ CORRETO!
    +1 ponto!
            
    {"❤️" * vida}  Vidas: {vida}
    🏆 Pontuação: {pontuação}
            
    resposta correta era: {traducao}
                """)
                        time.sleep(1)
                    else:
                        vida -= 1
                        print(f"""❌ INCORRETO!
            
    {"❤️" * vida}  Vidas: {vida}
    🏆 Pontuação: {pontuação}
            
    A resposta correta era: {traducao}
                """)
                        time.sleep(1)
            elif input_level in dificuldade["3"]:
                        print("Você escolheu o nível de dificuldade: Difícil")
                        time.sleep(0.5)
                        words = words_by_level["difícil"]
                        random_word = random.choice(words)
                        words.remove(random_word)
                        print(f"A palavra escolhida é: {random_word}")
                        time.sleep(3)
                        print("""Você terá 3 segundos para se preparar antes de gravar sua tradução...
                        """)
                        time.sleep(1)
                        for j in range(3, 0, -1):
                            print(f"""Você tem {j} segundos para se preparar...
                            """)
                            time.sleep(1)
                        print("Traduza a palavra...")
                        recording = sd.rec(
                        int(duration * sample_rate), # o número de amostras a serem registradas
                        samplerate=sample_rate,      # taxa de amostras
                        channels=1,                  # 1 significa gravação mono
                        dtype="int16")               # tipo de dados para as amostras registradas
                        for i in range(duration, 0, -1):
                            print(f"""Gravação concluída em {i} segundos...
                            """)
                            time.sleep(1)
                        sd.wait()
                        wav.write("teste.wav", sample_rate, recording)
                        print("""Gravação concluída, estou reconhecendo...
                        """)
                        time.sleep(1)
                        
                        recognizer = sr.Recognizer()
                        text = ""
                
                        with sr.AudioFile("teste.wav") as source:
                            audio = recognizer.record(source)
                        try:
                            text = recognizer.recognize_google(audio, language=input_target)
                        except sr.UnknownValueError:             # - se o Google não conseguiu entender a fala devido a ruídos ou silêncio
                            print("""A fala não pôde ser reconhecida.
                            
                            """)
                        except sr.RequestError as e:             # - se não houver conexão com a Internet ou a API estiver indisponível
                            print(f"""Service error: {e}
                
                """)
                
                        traducao = MyMemoryTranslator(source="pt-BR",target=input_target).translate(random_word)
                        if text == traducao:
                            pontuação += 1
                            print(f"""✅ CORRETO!
    +1 ponto!
        
    {"❤️" * vida}  Vidas: {vida}
    🏆 Pontuação: {pontuação}
                
    resposta correta era: {traducao}
                    """)
                            time.sleep(1)
                        else:
                            vida -= 1
                            print(f"""❌ INCORRETO!
                
    {"❤️" * vida}  Vidas: {vida}
    🏆 Pontuação: {pontuação}
        
    A resposta correta era: {traducao}
                    """)
                            time.sleep(1)
    else:
        print("""
Idioma inválido. Por favor, escolha as opções validas.""")
else:
    print("""
Nível de dificuldade inválido. Por favor, escolha as opções validas.""")
if vida == 0:
    print("Game Over!")
    print(f"Sua pontuação final foi: {pontuação}")
