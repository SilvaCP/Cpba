from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from datetime import date
import json

# ---------- Dados dos treinos ----------
treinos = {
    "Treino A": [
        "Supino reto: 4 x 10",
        "Supino inclinado: 4 x 10",
        "Crossover: 3 x 10",
        "Supino Declinado: 3 x 10",
        "Mergulho na paralela (com ajuda): 3 x 10",
        "Tríceps francês unilateral: 3 x 12 cada braço",
        "Tríceps testa: 3 x 10",
        "Tríceps corda: 3 x até a falha",
        "Abdômen prancha: 3 x 60 segundos"
    ],
    "Treino B": [
        "Puxada frente pegada aberta: 4 x 10",
        "Remada baixa: 4 x 10",
        "Remada hammer: 3 x 10",
        "Pulldown na polia (pegada neutra): 3 x 12",
        "Remada unilateral com Halter: 3 x 10 cada lado",
        "Rosca direta: 4 x 10",
        "Rosca alternada martelo: 3 x 10",
        "Prancha com remada: 3 x 12",
        "Alongamento lombar leve"
    ]
}

# ---------- Função para registrar histórico ----------
def registrar_treino(nome_treino):
    hoje = str(date.today())
    try:
        with open("historico.json", "r") as f:
            dados = json.load(f)
    except FileNotFoundError:
        dados = {}

    if hoje not in dados:
        dados[hoje] = []

    if nome_treino not in dados[hoje]:
        dados[hoje].append(nome_treino)

    with open("historico.json", "w") as f:
        json.dump(dados, f, indent=2)

# ---------- Telas ----------
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Label(text="🏋️ Projeto Monstro Treino Avançado", font_size=24))

        for treino in treinos.keys():
            btn = Button(text=treino)
            btn.bind(on_press=self.ir_para_treino)
            layout.add_widget(btn)

        btn_timer = Button(text="Timer de Prancha/Descanso")
        btn_timer.bind(on_press=self.ir_para_timer)
        layout.add_widget(btn_timer)

        btn_hist = Button(text="Ver Histórico")
        btn_hist.bind(on_press=self.ir_para_historico)
        layout.add_widget(btn_hist)

        self.add_widget(layout)

    def ir_para_treino(self, instance):
        registrar_treino(instance.text)
        self.manager.current = instance.text

    def ir_para_timer(self, instance):
        self.manager.current = "timer"

    def ir_para_historico(self, instance):
        self.manager.current = "historico"

class TreinoScreen(Screen):
    def __init__(self, nome_treino, **kwargs):
        super().__init__(name=nome_treino, **kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Label(text=nome_treino, font_size=20))
        for exercicio in treinos[nome_treino]:
            layout.add_widget(Label(text=exercicio))
        btn_voltar = Button(text="Voltar")
        btn_voltar.bind(on_press=self.voltar)
        layout.add_widget(btn_voltar)
        self.add_widget(layout)

    def voltar(self, instance):
        self.manager.current = "menu"

class TimerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(name="timer", **kwargs)
        self.seconds = 0
        self.timer_event = None
        self.sound = SoundLoader.load("beep.wav")

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.label = Label(text="Timer de Prancha/Descanso", font_size=24)
        self.timer_label = Label(text="Escolha o tempo", font_size=32)

        self.btn_30 = Button(text="30 segundos")
        self.btn_45 = Button(text="45 segundos")
        self.btn_90 = Button(text="90 segundos")

        for btn, t in zip([self.btn_30, self.btn_45, self.btn_90], [30, 45, 90]):
            btn.bind(on_press=lambda instance, tempo=t: self.set_time(tempo))
            self.layout.add_widget(btn)

        self.start_btn = Button(text="Iniciar Timer")
        self.start_btn.bind(on_press=self.start_timer)
        self.back_btn = Button(text="Voltar")
        self.back_btn.bind(on_press=self.voltar)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.timer_label)
        self.layout.add_widget(self.start_btn)
        self.layout.add_widget(self.back_btn)
        self.add_widget(self.layout)

    def set_time(self, tempo):
        self.seconds = tempo
        self.timer_label.text = f"{self.seconds} segundos selecionados"

    def start_timer(self, instance):
        if self.seconds > 0:
            self.timer_label.text = f"{self.seconds} segundos restantes"
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        if self.seconds > 0:
            self.seconds -= 1
            self.timer_label.text
App().run()
