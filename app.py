import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# --- 1. CONFIGURAZIONE PAGINA E TESTI ---
st.set_page_config(page_title="Autodiagnosi: Gestione del Tempo", layout="centered")

# Opzioni di risposta (Scala Likert a 4 punti)
OPZIONI = {"Mai": 1, "Raramente": 2, "Spesso": 3, "Sempre": 4}

# Dizionari delle domande
LADRI_DI_TEMPO = {
    "Pianificazione 'Rosa'": "Sottovaluto sistematicamente quanto tempo ci vorrà per finire un compito.",
    "Fuga Emotiva": "Rimando i compiti difficili non per pigrizia, ma perché mi generano ansia.",
    "Trappola del 'Sì'": "Accetto compiti altrui per bisogno di approvazione, sacrificando i miei.",
    "Zapping Mentale": "Passo continuamente da un'app all'altra pensando di essere produttivo.",
    "Pompierismo": "La mia giornata è un'emergenza continua; risolvo crisi invece di prevenirle.",
    "CC-ite Cronica": "Perdo ore a leggere email in cui sono in copia per 'conoscenza' ma non per azione.",
    "Blocco Perfezionista": "Mi fermo sui dettagli perché ho paura che il risultato non sia impeccabile."
}

COMPETENZE = {
    "Visione Strategica": "So riconoscere il 'momento giusto' per agire invece di seguire solo l'orologio.",
    "Architettura delle Priorità": "Utilizzo attivamente la Matrice di Eisenhower per proteggere le attività importanti.",
    "Focus Profondo": "Riesco a lavorare per 90 minuti senza controllare notifiche o smartphone.",
    "Assertività Empatica": "So dire di 'no' a una richiesta senza sentirmi in colpa o sembrare scortese.",
    "Metacognizione": "Ogni settimana analizzo come ho usato il mio tempo e correggo il tiro."
}

CAMBIAMENTI = {
    "Patto di Ulisse": "Ho creato barriere fisiche (es. telefono in un'altra stanza) per proteggere il mio lavoro.",
    "Time Blocking": "Il mio calendario non ha solo appuntamenti, ma blocchi fissi per il lavoro profondo.",
    "Protocollo Asincrono": "Ho smesso di pretendere (e dare) risposte istantanee a ogni messaggio.",
    "Mentalità 'Satisficing'": "Accetto di produrre bozze 'imperfette' pur di superare l'inerzia iniziale.",
    "Azione Successiva": "Non scrivo 'Progetto X' nella lista, ma solo il primo micro-passo concreto da fare."
}

# --- 2. LOGICA FUNZIONALE E GRAFICA ---
def crea_grafico_radar(punteggio_ladri, punteggio_competenze, punteggio_cambiamenti):
    # Calcolo percentuali (per i ladri, invertiamo il punteggio in modo che un valore alto = buon controllo)
    max_ladri = len(LADRI_DI_TEMPO) * 4
    max_competenze = len(COMPETENZE) * 4
    max_cambiamenti = len(CAMBIAMENTI) * 4
    
    perc_controllo_ladri = 100 - ((punteggio_ladri - len(LADRI_DI_TEMPO)) / (max_ladri - len(LADRI_DI_TEMPO)) * 100)
    perc_competenze = ((punteggio_competenze - len(COMPETENZE)) / (max_competenze - len(COMPETENZE))) * 100
    perc_cambiamenti = ((punteggio_cambiamenti - len(CAMBIAMENTI)) / (max_cambiamenti - len(CAMBIAMENTI))) * 100

    categorie = ['Controllo Sabotatori', 'Competenze Attive', 'Azioni Pratiche']
    valori = [perc_controllo_ladri, perc_competenze, perc_cambiamenti]
    valori += valori[:1] # Chiude il poligono

    angoli = [n / float(len(categorie)) * 2 * pi for n in range(len(categorie))]
    angoli += angoli[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    
    plt.xticks(angoli[:-1], categorie, color='grey', size=12)
    ax.set_rlabel_position(0)
    plt.yticks([25, 50, 75, 100], ["25%", "50%", "75%", "100%"], color="grey", size=8)
    plt.ylim(0, 100)

    ax.plot(angoli, valori, color='#1f77b4', linewidth=2, linestyle='solid')
    ax.fill(angoli, valori, color='#1f77b4', alpha=0.4)
    
    return fig, perc_controllo_ladri, perc_competenze, perc_cambiamenti

def genera_feedback_narrativo(perc_ladri, perc_competenze, perc_cambiamenti):
    feedback = "### 📊 La tua Diagnosi\n\n"
    
    if perc_ladri < 50:
        feedback += "🚨 **Attenzione ai Sabotatori:** I ladri di tempo stanno prosciugando le tue energie. Il problema principale non è l'orologio, ma la gestione dei confini e delle emozioni. Inizia a dire qualche 'no' in più.\n\n"
    else:
        feedback += "🛡️ **Buon Controllo:** Riesci a tenere a bada le distrazioni principali e le emergenze fittizie.\n\n"
        
    if perc_competenze < 50:
        feedback += "🛠️ **Cassetta degli attrezzi vuota:** Ti manca un sistema solido. Lavora sulla Matrice di Eisenhower e sulla pianificazione strategica. Lavorare tanto non significa lavorare bene.\n\n"
    else:
        feedback += "🧠 **Ottime Competenze:** Hai una buona consapevolezza teorica e pratica degli strumenti di produttività.\n\n"
        
    if perc_cambiamenti < 50:
        feedback += "🛑 **Inerzia Operativa:** Hai la teoria, ma ti manca l'azione chirurgica. Devi trasformare le intenzioni in abitudini (es. Time Blocking rigoroso e distacco dalle notifiche).\n\n"
    else:
        feedback += "🚀 **Piena Azione:** Stai implementando attivamente strategie difensive e proattive per proteggere il tuo tempo. Continua così!\n\n"
        
    return feedback

# --- 3. INTERFACCIA UTENTE (UI) ---
def main():
    st.title("⏱️ Autodiagnosi: Gestione del Tempo e Sabotatori")
    st.markdown("Scopri quali sono i tuoi veri limiti nella gestione del tempo e come trasformare la consapevolezza in azione chirurgica.")

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    if not st.session_state.submitted:
        with st.form("questionario"):
            st.header("1. I Miei Ladri di Tempo")
            st.markdown("Quanto spesso ti ritrovi in queste situazioni?")
            risposte_ladri = {}
            for chiave, domanda in LADRI_DI_TEMPO.items():
                risp = st.radio(f"**{chiave}**: {domanda}", list(OPZIONI.keys()), horizontal=True, key=f"l_{chiave}")
                risposte_ladri[chiave] = OPZIONI[risp]

            st.header("2. Le Mie Competenze")
            st.markdown("Quanto spesso applichi queste tecniche?")
            risposte_competenze = {}
            for chiave, domanda in COMPETENZE.items():
                risp = st.radio(f"**{chiave}**: {domanda}", list(OPZIONI.keys()), horizontal=True, key=f"c_{chiave}")
                risposte_competenze[chiave] = OPZIONI[risp]

            st.header("3. Cambiamenti Necessari")
            st.markdown("Quanto sono presenti queste abitudini nella tua routine?")
            risposte_cambiamenti = {}
            for chiave, domanda in CAMBIAMENTI.items():
                risp = st.radio(f"**{chiave}**: {domanda}", list(OPZIONI.keys()), horizontal=True, key=f"m_{chiave}")
                risposte_cambiamenti[chiave] = OPZIONI[risp]

            submit_button = st.form_submit_button(label="Genera Profilo 🚀")

            if submit_button:
                st.session_state.punteggio_ladri = sum(risposte_ladri.values())
                st.session_state.punteggio_competenze = sum(risposte_competenze.values())
                st.session_state.punteggio_cambiamenti = sum(risposte_cambiamenti.values())
                st.session_state.submitted = True
                st.rerun()

    else:
        st.success("Analisi completata con successo!")
        
        # Mostra Grafico
        fig, p_ladri, p_comp, p_camb = crea_grafico_radar(
            st.session_state.punteggio_ladri, 
            st.session_state.punteggio_competenze, 
            st.session_state.punteggio_cambiamenti
        )
        st.pyplot(fig)
        
        # Mostra Feedback Narrativo
        testo_feedback = genera_feedback_narrativo(p_ladri, p_comp, p_camb)
        st.markdown(testo_feedback)
        
        # Pulsante per resettare
        if st.button("Ripeti il Test"):
            st.session_state.submitted = False
            st.rerun()

if __name__ == "__main__":
    main()
