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
    "fácil": ["gato", "cachorro", "maçã", "leite", "sol", "lua", "flor", "carro", "livro", "bola", "peixe"],
    "médio": ["casa", "escola", "amigo", "janela", "amarelo", "cidade", "cabeça", "música", "trabalho", "viagem"],
    "difícil": ["tecnologia", "universidade", "informação", "pronúncia", "imaginação", "telefone", "mundo", "literalmente", "dificuldade", "roupas"]
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
Digite a dificuldade com base no numero: """)

input_target = input("""Para começar, digite o idioma de saída para a tradução
            'en-US' para inglês
            'es-ES' para espanhol: """)


print(f"Você escolheu o idioma de saída: {input_target}")
time.sleep(1)

while vida > 0 and pontuação < 5:
    if input_level == "1":
        print("Você escolheu o nível de dificuldade: Fácil")
        time.sleep(0.5)
        words = words_by_level["fácil"]
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
    elif input_level == "2":
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
    elif input_level == "3":
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
if vida == 0:
    print("Game Over!")
    print(f"Sua pontuação final foi: {pontuação}")
