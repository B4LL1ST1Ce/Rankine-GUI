import tkinter as tk
from tkinter import ttk
import CoolProp.CoolProp as CP
import state_class as SC
import matplotlib.pyplot as plt
import numpy as np

s1 = SC.States()
s2 = SC.States()
s3 = SC.States()
s4 = SC.States()
s5 = SC.States()
s6 = SC.States()

def createStateTable():
    state = {
        1: {'H': s1.h, 'P': s1.p, 'T': s1.t, 'S': s1.s, 'Q': s1.q, 'D': s1.d, 'V': s1.v},
        2: {'H': s2.h, 'P': s2.p, 'T': s2.t, 'S': s2.s, 'Q': s2.q, 'D': s2.d, 'V': s2.v},
        3: {'H': s3.h, 'P': s3.p, 'T': s3.t, 'S': s3.s, 'Q': s3.q, 'D': s3.d, 'V': s3.v},
        4: {'H': s4.h, 'P': s4.p, 'T': s4.t, 'S': s4.s, 'Q': s4.q, 'D': s4.d, 'V': s4.v},
        5: {'H': s5.h, 'P': s5.p, 'T': s5.t, 'S': s5.s, 'Q': s5.q, 'D': s5.d, 'V': s5.v},
        6: {'H': s6.h, 'P': s6.p, 'T': s6.t, 'S': s6.s, 'Q': s6.q, 'D': s6.d, 'V': s6.v}
        }
    if cycleSelected.get() == "reheat":
        return state
    elif cycleSelected.get() == "simple":
        state = {s: p for s, p in state.items() if s in range(1,5)}
        return state
    elif cycleSelected.get() == "single":
        state = {s: p for s, p in state.items() if s in range(1, 2)}
        return state

def matchStateValues(state):
    if cycleSelected.get() == "single":
        return state

    if cycleSelected.get() == "reheat":
        matched = [
            (1, 2, 'S'),
            (3, 4, 'S'),
            (5, 6, 'S'),
            (1, 6, 'P'),
            (2, 3, 'P'),
            (4, 5, 'P')
        ]

    elif cycleSelected.get() =="simple":
        matched = [
            (1, 2, 'S'),
            (3, 4, 'S'),
            (1, 4, 'P'),
            (2, 3, 'P')
        ]

    for x, y, inp in matched:
        if state[x].get(inp) != None and state[y].get(inp) == None:
            state[y][inp] = state[x][inp]
        elif state[y].get(inp) != None and state[x].get(inp) == None:
            state[x][inp] = state[y][inp]

def solveStateValues(state):

    updated = False

    knownProps = {prop: value for prop, value in state.items() if value != None}
    unknownProps = {prop: value for prop, value in state.items() if value == None}

    if len(knownProps) <= 1:
        return updated
    
    (prop1, val1), (prop2, val2) = list(knownProps.items())[:2]
    for uprop, val in unknownProps.items():
        state[uprop] = CP.PropsSI(uprop, prop1, val1, prop2, val2, 'water')
        updated = True
    
    return updated

def convertFloat(input):
    if input == '':
        return None
    try:
        return float(input)
    except ValueError:
        return None

def calcClick():
    s1_6 = [s1, s2, s3, s4, s5, s6]
    for i in s1_6:
        i.resetValues()

    s1.enterValues(S1_1Dropdown.get(), convertFloat(S1_1Entry.get()), S1_2Dropdown.get(), convertFloat(S1_2Entry.get()), pressureDropdown.get(), temperatureDropdown.get())
    s2.enterValues(S2_1Dropdown.get(), convertFloat(S2_1Entry.get()), S2_2Dropdown.get(), convertFloat(S2_2Entry.get()), pressureDropdown.get(), temperatureDropdown.get())
    s3.enterValues(S3_1Dropdown.get(), convertFloat(S3_1Entry.get()), S3_2Dropdown.get(), convertFloat(S3_2Entry.get()), pressureDropdown.get(), temperatureDropdown.get())
    s4.enterValues(S4_1Dropdown.get(), convertFloat(S4_1Entry.get()), S4_2Dropdown.get(), convertFloat(S4_2Entry.get()), pressureDropdown.get(), temperatureDropdown.get())
    s5.enterValues(S5_1Dropdown.get(), convertFloat(S5_1Entry.get()), S5_2Dropdown.get(), convertFloat(S5_2Entry.get()), pressureDropdown.get(), temperatureDropdown.get())
    s6.enterValues(S6_1Dropdown.get(), convertFloat(S6_1Entry.get()), S6_2Dropdown.get(), convertFloat(S6_2Entry.get()), pressureDropdown.get(), temperatureDropdown.get())

    state = createStateTable()

    for i in range(20):
        updated_any = False
        matchStateValues(state)
        for x in state.values():
            updated = solveStateValues(x)
            updated_any = updated_any or updated
        if not updated_any:
            break

    if cycleSelected.get() == "reheat":
        h = {i: s['H'] for i, s in state.items()}
        for i in range(1, 7):
            s1_6[i-1].updateValues('H', h[i])
        s = {i: s['S'] for i, s in state.items()}
        for i in range(1, 7):
            s1_6[i-1].updateValues('S', s[i])
        t = {i: s['T'] for i, s in state.items()}
        for i in range(1, 7):
            s1_6[i-1].updateValues('T', t[i])
        p = {i: s['P'] for i, s in state.items()}
        for i in range(1, 7):
            s1_6[i-1].updateValues('P', p[i])
        q = {i: s['Q'] for i, s in state.items()}
        for i in range(1, 7):
            s1_6[i-1].updateValues('Q', q[i])
        d = {i: s['D'] for i, s in state.items()}
        for i in range(1, 7):
            s1_6[i-1].updateValues('D', d[i])
        v = {i: s['V'] for i, s in state.items()}
        for i in range(1, 7):
            s1_6[i-1].updateValues('V', v[i])
        try:
            w_t_HP = h[3]-h[4]
            w_t_LP = h[5]-h[6]
            w_turb = w_t_HP+w_t_LP  # in J/kg
            w_pump = h[2]-h[1]
            w_net = w_turb-w_pump
            q_inB = h[3]-h[2]
            q_inR = h[5]-h[4]
            q_in = q_inB+q_inR
            eff = (w_net/q_in)*100

            textbox.config(state="normal")
            textbox.delete(1.0, 'end')
            textbox.insert('end', f"-------- Energy Values --------")
            textbox.insert('end', f"\nHP Turbine Work Output: {w_t_HP/1000:.2f}kJ/kg")
            textbox.insert('end', f"\nLP Turbine Work Output: {w_t_LP/1000:.2f}kJ/kg")
            textbox.insert('end', f"\nTurbine Work Output:    {w_turb/1000:.2f}kJ/kg")
            textbox.insert('end', f"\nPump Work Input:        {w_pump/1000:.2f}kJ/kg")
            textbox.insert('end', f"\nNet Work Output:        {w_net/1000:.2f}kJ/kg")
            textbox.insert('end', f"\nNet Heat Input:         {q_in/1000:.2f}kJ/kg")
            textbox.insert('end', f"\nThermal Efficiency:     {eff:.2f}%")
            textbox.config(state="disabled")

            plotTsButton.config(state="normal")
            plotPvButton.config(state="normal")
        except: 
            textbox.config(state="normal")
            textbox.delete(1.0, 'end')
            textbox.insert(1.0, "TypeError: The given values are either unsolvable or inputted incorrectly.")
            textbox.config(state="disabled")
            raise TypeError("Unsolvable with the given values.")
    elif cycleSelected.get() == "simple":
        h = {i: s['H'] for i, s in state.items()}
        for i in range(1, 5):
            s1_6[i-1].updateValues('H', h[i])
        s = {i: s['S'] for i, s in state.items()}
        for i in range(1, 5):
            s1_6[i-1].updateValues('S', s[i])
        t = {i: s['T'] for i, s in state.items()}
        for i in range(1, 5):
            s1_6[i-1].updateValues('T', t[i])
        p = {i: s['P'] for i, s in state.items()}
        for i in range(1, 5):
            s1_6[i-1].updateValues('P', p[i])
        q = {i: s['Q'] for i, s in state.items()}
        for i in range(1, 5):
            s1_6[i-1].updateValues('Q', q[i])
        d = {i: s['D'] for i, s in state.items()}
        for i in range(1, 5):
            s1_6[i-1].updateValues('D', d[i])
        v = {i: s['V'] for i, s in state.items()}
        for i in range(1, 5):
            s1_6[i-1].updateValues('V', v[i])

        try: 
            w_turb = h[3]-h[4]
            w_pump = h[2]-h[1]
            w_net = w_turb-w_pump
            q_in = h[3]-h[2]
            eff = (w_net/q_in)*100

            textbox.config(state="normal")
            textbox.delete(1.0, 'end')
            textbox.insert('end', f"======== Energy Analysis ========")
            textbox.insert('end', f"\nTurbine Work Output: {w_turb/1000:.2f}kJ/kg")
            textbox.insert('end', f"\nPump Work Input:     {w_pump/1000:.2f}kJ/kg")
            textbox.insert('end', f"\nNet Work Output:     {w_net/1000:.2f}kJ/kg")
            textbox.insert('end', f"\nHeat Input:          {q_in/1000:.2f}kJ/kg")
            textbox.insert('end', f"\nThermal Efficiency:  {eff:.2f}%")
            textbox.config(state="disabled")

            plotTsButton.config(state="normal")
            plotPvButton.config(state="normal")
        except: 
            textbox.config(state="normal")
            textbox.delete(1.0, 'end')
            textbox.insert(1.0, "TypeError: The given values are either unsolvable or inputted incorrectly.")
            textbox.config(state="disabled")
            raise TypeError("Unsolvable with the given values.")
    elif cycleSelected.get() == "single":
        try:
            h = state[1]['H']
            s = state[1]['S']
            t = state[1]['T']
            p = state[1]['P']
            q = state[1]['Q']
            d = state[1]['D']
            textbox.config(state="normal")
            textbox.delete(1.0, 'end')
            textbox.insert('end', f"===== Single State Values =====")
            textbox.insert('end', f"\nSpecific Enthalpy (h): {h/1000:.2f}kJ/kg")
            textbox.insert('end', f"\nSpecific Entropy (s):  {s/1000:.2f}kJ/kgK")
            textbox.insert('end', f"\nTemperature (T):       {t:.2f}K")
            textbox.insert('end', f"\nPressure (P):          {p/1000:.2f}kPa")
            textbox.insert('end', f"\nDryness Factor:        {q*100:.2f}%")
            textbox.config(state="disabled")
        except: 
            textbox.config(state="normal")
            textbox.delete(1.0, 'end')
            textbox.insert(1.0, "TypeError: The given values are either unsolvable or inputted incorrectly.")
            textbox.config(state="disabled")
            raise TypeError("Unsolvable with the given values.")
    stateDetails(state)

def plotClick_Ts():
    if cycleSelected.get() == "reheat":
        T = [s1.t, s2.t, s3.t, s4.t, s5.t, s6.t]
        P = [s1.p, s2.p, s3.p, s4.p, s5.p, s6.p]
        S = [s1.s, s2.s, s3.s, s4.s, s5.s, s6.s]

        s1_2 = [s1.s, s2.s]
        T1_2 = [s1.t, s2.t]
        s2_3 = np.linspace(S[1], S[2], 100)
        T2_3 = [CP.PropsSI('T', 'P', P[2], 'S', s, 'water') for s in s2_3]
        s3_4 = [s3.s, s4.s]
        T3_4 = [s3.t, s4.t]
        s4_5 = np.linspace(S[3], S[4], 100)
        T4_5 = [CP.PropsSI('T', 'P', P[4], 'S', s, 'water') for s in s4_5]
        s5_6 = [s5.s, s6.s]
        T5_6 = [s5.t, s6.t]
        s6_1 = np.linspace(S[5], S[0], 100)
        T6_1 = [CP.PropsSI('T', 'P', P[0], 'S', s, 'water') for s in s6_1]

        plt.plot(s1_2, T1_2, 'r')
        plt.plot(s2_3, T2_3, 'r')
        plt.plot(s3_4, T3_4, 'r')
        plt.plot(s4_5, T4_5, 'r')
        plt.plot(s5_6, T5_6, 'r')
        plt.plot(s6_1, T6_1, 'r')
    elif cycleSelected.get() == "simple":
        T = [s1.t, s2.t, s3.t, s4.t]
        P = [s1.p, s2.p, s3.p, s4.p]
        S = [s1.s, s2.s, s3.s, s4.s]

        s1_2 = [s1.s, s2.s]
        T1_2 = [s1.t, s2.t]
        s2_3 = np.linspace(S[1], S[2], 100)
        T2_3 = [CP.PropsSI('T', 'P', P[2], 'S', s, 'water') for s in s2_3]
        s3_4 = [s3.s, s4.s]
        T3_4 = [s3.t, s4.t]
        s4_1 = np.linspace(S[3], S[0], 100)
        T4_1 = [CP.PropsSI('T', 'P', P[0], 'S', s, 'water') for s in s4_1]

        plt.plot(s1_2, T1_2, 'r')
        plt.plot(s2_3, T2_3, 'r')
        plt.plot(s3_4, T3_4, 'r')
        plt.plot(s4_1, T4_1, 'r')

    T_min = CP.PropsSI('Ttriple', 'water')
    T_crit = CP.PropsSI('Tcrit', 'water')
    Tvalues = np.linspace(T_min, T_crit, 500)
    s_liq = [CP.PropsSI('S', 'T', t, 'Q', 0, 'water') for t in Tvalues]
    s_vap = [CP.PropsSI('S', 'T', t, 'Q', 1, 'water') for t in Tvalues]
    plt.plot(s_liq, Tvalues, '--')
    plt.plot(s_vap, Tvalues, '--')
    plt.plot(S, T, 'ko')
    plt.xlabel("Specific Entropy (s)")
    plt.ylabel("Temperature (K)")
    plt.title("T-s Graph")
    plt.show()

def plotClick_Pv():
    D = [s1.d, s2.d, s3.d, s4.d, s5.d, s6.d, s1.d]
    P = [s1.p, s2.p, s3.p, s4.p, s5.p, s6.p, s1.p]
    V = []
    for i in D:
        V.append(1/i)
    
    V1_2 = [V[0], V[1]]
    P1_2 = [P[0], P[1]]
    V2_3 = [V[1], V[2]]
    P2_3 = [P[1], P[2]]
    V3_4 = np.linspace(V[2], V[3], 100)
    D3_4 = np.linspace(s3.d, s4.d, 100)
    P3_4 = [CP.PropsSI('P', 'D', d, 'S', s4.s, 'water') for d in D3_4]
    V4_5 = [V[3], V[4]]
    P4_5 = [P[3], P[4]]
    V5_6 = np.linspace(V[4], V[5], 100)
    D5_6 = np.linspace(D[4], D[5], 100)
    P5_6 = [CP.PropsSI('P', 'D', d, 'S', s6.s, 'water') for d in D5_6]
    V6_1 = [V[5], V[0]]
    P6_1 = [P[5], P[0]]

    plt.plot(V1_2, P1_2, 'r')
    plt.plot(V2_3, P2_3, 'r')
    plt.plot(V3_4, P3_4, 'r')
    plt.plot(V4_5, P4_5, 'r')
    plt.plot(V5_6, P5_6, 'r')
    plt.plot(V6_1, P6_1, 'r')

    plt.plot(V, P, 'ko')
    plt.xscale("log")
    plt.xlabel("Specific Volume (v)")
    plt.ylabel("Pressure (Pa)")
    plt.title("P-v Graph")
    plt.show()

def updatedWindow():
    entries = [S2_1Entry, S2_2Entry, S3_1Entry, S3_2Entry, S4_1Entry, S4_2Entry, S5_1Entry, S5_2Entry, S6_1Entry, S6_2Entry]
    dropdowns = [S2_1Dropdown, S2_2Dropdown, S3_1Dropdown, S3_2Dropdown, S4_1Dropdown, S4_2Dropdown, S5_1Dropdown, S5_2Dropdown, S6_1Dropdown, S6_2Dropdown]
    labels = [S2Label, S3Label, S4Label, S5Label, S6Label]

    plotTsButton.config(state="disabled")
    plotPvButton.config(state="disabled")
    if cycleSelected.get() == "reheat":
        for i in entries + labels:
            i.config(state="normal")
        for i in dropdowns:
            i.config(state="readonly")
        stateDetails(createStateTable())
    elif cycleSelected.get() == "simple":
        for i in entries[6:10] + dropdowns[6:10] + labels[3:5]:
            i.config(state="disabled")
        for i in entries[0:6] + labels[0:3]:
            i.config(state="normal")
        for i in dropdowns[0:6]:
            i.config(state="readonly")
        stateDetails(createStateTable())
    elif cycleSelected.get() == "single":
        for i in entries + dropdowns + labels:
            i.config(state="disabled")
        stateDetails(createStateTable())

def stateDetails(state):
    stateFrame.pack(padx=5, pady=5)
    if showStateValues.get() == False:
        stateFrame.pack_forget()
        for widget in stateFrame.winfo_children(): # Blessings be upon gavin for telling this function exists after I spent many a time trying to figure out how to delete each thing individually... sigh. I should've read the documentation.
            widget.destroy()
    elif showStateValues.get() == True:
        authorLabel.pack_forget()
        versionLabel.pack_forget()
        for i in range(len(state)):
            stateLabel = tk.Label(stateFrame, text=f"State {i+1}:", borderwidth=1, relief="raised", width=15, height=1, pady=2)
            stateLabel.grid(row=0, column=i)

        values = ['H', 'S', 'P', 'T', 'Q', 'D']

        for i in range(len(values)):
            for j in range(1, len(state)+1):
                propLabel = tk.Label(stateFrame, text=f"{values[i]}: {roundWithNone(state[j][values[i]])}", borderwidth=1, relief="raised", width=15, height=1, pady=3)
                propLabel.grid(row=i+1, column=j-1)
        authorLabel.pack(side='left', padx=5)
        versionLabel.pack(side='right', padx=5)

def roundWithNone(val):
    if val == None:
        return None
    else:
        return round(val, 2)
### GUI STUFF ============================================================================================================================

window = tk.Tk()
window.title("Rankine Cycle Calculator")
window.config(width=700, height=500)

standardPressureValue = tk.StringVar(value="MPa")
standardTemperaturevalue = tk.StringVar(value="\u00b0C")
cycleSelected = tk.StringVar(value="reheat")
showStateValues = tk.BooleanVar(value=False)
pressureValues = ["MPa", "bar", "kPa", "Pa"]
temperatureValues = ["\u00b0C", "K", "\u00b0F", "\u00b0R"]
inputValues = ["P", "T", "S", "Q", "H", "D"]

dropdownWidth = 2
entryWidth = 12
entrypadX = (5, 0)
entrypadY = (0, 10)

titleLabel = tk.Label(window, text="Ideal Rankine Calculator", font=("Arial", 24))
titleLabel.pack(padx=5, pady=(5, 5))

textbox = tk.Text(window, height=15, state="disabled")
textbox.pack(padx=5, pady=2.5)

inputFrame = tk.Frame(window)
inputFrame.pack(padx=5, pady=(2.5, 2.5))

S1Label = tk.Label(inputFrame, text="State 1:")
S1Frame = tk.Frame(inputFrame)
S1_1Entry = tk.Entry(S1Frame, justify="center", width=entryWidth)
S1_1Dropdown = ttk.Combobox(S1Frame, values=inputValues, state="readonly", width=dropdownWidth)
S1_2Entry = tk.Entry(S1Frame, justify="center", width=entryWidth)
S1_2Dropdown = ttk.Combobox(S1Frame, values=inputValues, state="readonly", width=dropdownWidth)
S1Label.grid(row=0, column=0)
S1Frame.grid(row=1, column=0)
S1_1Entry.grid(row=0, column=0, padx=entrypadX, pady=entrypadY)
S1_1Dropdown.grid(row=0, column=1, pady=entrypadY)
S1_2Entry.grid(row=1, column=0, padx=entrypadX, pady=entrypadY)
S1_2Dropdown.grid(row=1, column=1, pady=entrypadY)

S2Label = tk.Label(inputFrame, text="State 2:")
S2Frame = tk.Frame(inputFrame)
S2_1Entry = tk.Entry(S2Frame, justify="center", width=entryWidth)
S2_1Dropdown = ttk.Combobox(S2Frame, values=inputValues, state="readonly", width=dropdownWidth)
S2_2Entry = tk.Entry(S2Frame, justify="center", width=entryWidth)
S2_2Dropdown = ttk.Combobox(S2Frame, values=inputValues, state="readonly", width=dropdownWidth)
S2Label.grid(row=0, column=1)
S2Frame.grid(row=1, column=1)
S2_1Entry.grid(row=0, column=0, padx=entrypadX, pady=entrypadY)
S2_1Dropdown.grid(row=0, column=1, pady=entrypadY)
S2_2Entry.grid(row=1, column=0, padx=entrypadX, pady=entrypadY)
S2_2Dropdown.grid(row=1, column=1, pady=entrypadY)

S3Label = tk.Label(inputFrame, text="State 3:")
S3Frame = tk.Frame(inputFrame)
S3_1Entry = tk.Entry(S3Frame, justify="center", width=entryWidth)
S3_1Dropdown = ttk.Combobox(S3Frame, values=inputValues, state="readonly", width=dropdownWidth)
S3_2Entry = tk.Entry(S3Frame, justify="center", width=entryWidth)
S3_2Dropdown = ttk.Combobox(S3Frame, values=inputValues, state="readonly", width=dropdownWidth)
S3Label.grid(row=0, column=2)
S3Frame.grid(row=1, column=2)
S3_1Entry.grid(row=0, column=0, padx=entrypadX, pady=entrypadY)
S3_1Dropdown.grid(row=0, column=1, pady=entrypadY)
S3_2Entry.grid(row=1, column=0, padx=entrypadX, pady=entrypadY)
S3_2Dropdown.grid(row=1, column=1, pady=entrypadY)

S4Label = tk.Label(inputFrame, text="State 4:")
S4Frame = tk.Frame(inputFrame)
S4_1Entry = tk.Entry(S4Frame, justify="center", width=entryWidth)
S4_1Dropdown = ttk.Combobox(S4Frame, values=inputValues, state="readonly", width=dropdownWidth)
S4_2Entry = tk.Entry(S4Frame, justify="center", width=entryWidth)
S4_2Dropdown = ttk.Combobox(S4Frame, values=inputValues, state="readonly", width=dropdownWidth)
S4Label.grid(row=0, column=3)
S4Frame.grid(row=1, column=3)
S4_1Entry.grid(row=0, column=0, padx=entrypadX, pady=entrypadY)
S4_1Dropdown.grid(row=0, column=1, pady=entrypadY)
S4_2Entry.grid(row=1, column=0, padx=entrypadX, pady=entrypadY)
S4_2Dropdown.grid(row=1, column=1, pady=entrypadY)

S5Label = tk.Label(inputFrame, text="State 5:")
S5Frame = tk.Frame(inputFrame)
S5_1Entry = tk.Entry(S5Frame, justify="center", width=entryWidth)
S5_1Dropdown = ttk.Combobox(S5Frame, values=inputValues, state="readonly", width=dropdownWidth)
S5_2Entry = tk.Entry(S5Frame, justify="center", width=entryWidth)
S5_2Dropdown = ttk.Combobox(S5Frame, values=inputValues, state="readonly", width=dropdownWidth)
S5Label.grid(row=0, column=4)
S5Frame.grid(row=1, column=4)
S5_1Entry.grid(row=0, column=0, padx=entrypadX, pady=entrypadY)
S5_1Dropdown.grid(row=0, column=1, pady=entrypadY)
S5_2Entry.grid(row=1, column=0, padx=entrypadX, pady=entrypadY)
S5_2Dropdown.grid(row=1, column=1, pady=entrypadY)

S6Label = tk.Label(inputFrame, text="State 6:")
S6Frame = tk.Frame(inputFrame)
S6_1Entry = tk.Entry(S6Frame, justify="center", width=entryWidth)
S6_1Dropdown = ttk.Combobox(S6Frame, values=inputValues, state="readonly", width=dropdownWidth)
S6_2Entry = tk.Entry(S6Frame, justify="center", width=entryWidth)
S6_2Dropdown = ttk.Combobox(S6Frame, values=inputValues, state="readonly", width=dropdownWidth)
S6Label.grid(row=0, column=5)
S6Frame.grid(row=1, column=5)
S6_1Entry.grid(row=0, column=0, padx=entrypadX, pady=entrypadY)
S6_1Dropdown.grid(row=0, column=1, padx=(0, 5), pady=entrypadY)
S6_2Entry.grid(row=1, column=0, padx=entrypadX, pady=entrypadY)
S6_2Dropdown.grid(row=1, column=1, padx=(0, 5), pady=entrypadY)

selectionFrame = tk.Frame(window, width=700, height=50)
selectionFrame.pack(padx=5)

PTDropdownFrame = tk.Frame(selectionFrame, padx=5)
PTDropdownFrame.place(relx=0.1, rely=0.5, anchor="center")
pressureLabel = tk.Label(PTDropdownFrame, text="P")
pressureLabel.grid(row=0, column=0)
pressureDropdown = ttk.Combobox(PTDropdownFrame, textvariable=standardPressureValue, values=pressureValues, state="readonly", width=5)
pressureDropdown.grid(row=1, column=0)
temperatureLabel = tk.Label(PTDropdownFrame, text="T")
temperatureLabel.grid(row=0, column=1)
temperatureDropdown = ttk.Combobox(PTDropdownFrame, textvariable=standardTemperaturevalue, values=temperatureValues, state="readonly", width=5)
temperatureDropdown.grid(row=1, column=1)

cycleFrame = tk.Frame(selectionFrame, padx=5)
cycleFrame.place(relx=0.5, rely=0.5, anchor='center')
reheatCycleCheckbox = tk.Radiobutton(cycleFrame, variable=cycleSelected, value="reheat", command=lambda:updatedWindow())
reheatCycleLabel = tk.Label(cycleFrame, text="Reheat Cycle")
simpleCycleCheckbox = tk.Radiobutton(cycleFrame, variable=cycleSelected, value="simple", command=lambda:updatedWindow())
simplelCycleLabel = tk.Label(cycleFrame, text="Simple Cycle")
singleStateCheckbox = tk.Radiobutton(cycleFrame, variable=cycleSelected, value="single", command=lambda:updatedWindow())
singleStateLabel = tk.Label(cycleFrame, text="Single State")
reheatCycleCheckbox.grid(row=0, column=0)
reheatCycleLabel.grid(row=1, column=0, padx=10, pady=entrypadY)
simpleCycleCheckbox.grid(row=0, column=1)
simplelCycleLabel.grid(row=1, column=1, padx=10, pady=entrypadY)
singleStateCheckbox.grid(row=0, column=2)
singleStateLabel.grid(row=1, column=2, padx=10, pady=entrypadY)

calcPlotFrame = tk.Frame(window)
calcPlotFrame.pack(padx=5)
calculateButton = tk.Button(calcPlotFrame, text="Calculate", justify="center" , command=lambda:calcClick())
calculateButton.grid(row=0, column=0, padx=5)
plotTsButton = tk.Button(calcPlotFrame, text="Plot T-s Diagram", justify="center", state="disabled", command=lambda:plotClick_Ts())
plotTsButton.grid(row=0, column=1, padx=5)
plotPvButton = tk.Button(calcPlotFrame, text="Plot P-v Diagram", justify="center", state="disabled", command=lambda:plotClick_Pv())
plotPvButton.grid(row=0, column=2, padx=5)

authorLabel = tk.Label(window, text="Ethan W.")
versionLabel = tk.Label(window, text="v2.1")

stateFrame = tk.Frame(window)
stateFrame.pack()
stateDetails(createStateTable())
showStateDetails = tk.Checkbutton(calcPlotFrame, text="State Details", variable=showStateValues, onvalue=True, offvalue=False, command=lambda:stateDetails(createStateTable()))
showStateDetails.grid(row=0, column=3, padx=5)
authorLabel.pack(side='left', padx=5)
versionLabel.pack(side='right', padx=5)

window.mainloop()