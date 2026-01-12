import streamlit as st
import hashlib
import itertools
import ast

def apply_substitutions(word, subs):
    # Generate all variants for a word by substituting each character
    lists_of_chars = [subs.get(c, [c]) for c in word]
    for variant_tuple in itertools.product(*lists_of_chars):
        yield "".join(variant_tuple)

# ------------ DATA: Imported once, not shown to pupils -------------
dataleak_dict = {
    "Alex": "83878c91171338902e0fe0fb97a8c47a",
    "Béatrice": "45c48cce2e2d7fbdea1afc51c7c6ad26",
    "Christophe": "2b9ed9314c9b75f085fcf7356337d30b",
    "Daniela": "5f4dcc3b5aa765d61d8327deb882cf99",
    "Elisabeth": "a384b6463fc216a5f8ecb6670f86456a",
    "Fernanda": "25d55ad283aa400af464c76d713c07ad",
    "Gilles": "5d793fc5b00a2348c3fb9ab59e5ca98a",
    "Hannah": "afdd0b4ad2ec172c586e2150770fbf9e",
    "Ilsa": "e7e06aff0e583c24313d7e96085aefa2",
    "Jhempi": "b850780bb2b06e0cf81afb7a2efebb1a",
    "Klara": "4fc963e213bba362778f5c175eb4d5ff",
    "Louis": "7f320b406a0956586fcc21c9f18e9180",
    "Maren": "41e4652a622b10077ff4c22717dc57fd",
    "Nico": "5de2bcf647b707104e4513262903866c",
    "Olivia": "a996822761d1ed5066d2a208d549442b",
    "Pedro": "8acef4050a09ce337a04186afd44ed33",
    "Quentin": "195f19b835efe9f0b7b4e276ef1a8515",
    "Robert": "48e6c9d963b4ec1c7507c505d577a6ad",
    "Svenja": "b365a69719188e80fdd9183e1f3f42cd",
    "Tom": "f1174e62d60a92010c4a72fe87805ae1",
    "Ulrike": "2caa178076a628d0958fee0eab337176",
    "Victor": "4de8e33e649c6ee317c7937804b63fc1",
    "Wilhelmina": "c5efd020ac6cb5ab5542c54c91cb45ea",
    "Xenia": "38b77d171bec2ddcadcbf434355b4184",
    "Yves": "5833fe44252e19198cb9310b3f54eaf2",
    "Zelda": "8327d03221693ccea6df43e600008383"
}
dataleak = list(dataleak_dict.values())

def hash_password(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()

def get_name_by_hash(d, hash_value):
    for name, h in d.items():
        if h == hash_value:
            return name
    return None

def generate_strings(chars, length):
    return ("".join(c) for c in itertools.product(chars, repeat=length))

# Ensure stop signals are saved in session state
if "stop_search" not in st.session_state:
    st.session_state.stop_search = False

# Stepsize for the progress bar
STEPSIZE = 100000

# ------------------------------------------------------------------

st.title("💻 Password Hacking Playground")

tab1, tab2, tab3, tab4 = st.tabs(["1. Einfach probieren", "2. Bruteforce", "3. Verschiedene Charaktere", "4. Einfaches Ersetzen"])

with tab1:
    st.header("🔑 Angriff Nummer 1: Direkt probieren")
    st.write("Viele Benutzer*innen nutzen sehr einfache Passwörter. Probiere ein Passwort aus:")

    test_password = st.text_input("Gib ein Passwort ein, um es im Satensatz zu suchen", value="test")
    if st.button("Checken"):
        pw_hash = hash_password(test_password)
        if pw_hash in dataleak:
            name = get_name_by_hash(dataleak_dict, pw_hash)
            st.success(f"✅ Passwort gefunden! Es gehört zu {name}.")
        else:
            st.error("❌ Passwort nicht gefunden.")

with tab2:
    st.header("⚙️ Angriff Nummer 2: Bruteforce (nur Kleinbuchstaben)")
    st.write("Teste alle Kombinationen von Kleinbuchstaben mit einer bestimmten Länge.")
    
    testlength = st.slider("Passwortlänge auswählen", min_value=1, max_value=8, value=4)
    start_btn = st.button("Bruteforce starten")
    stop_btn = st.button("Suche stoppen")

    if stop_btn:
        st.session_state.stop_search = True
    if start_btn:
        st.session_state.stop_search = False

    if start_btn or (st.session_state.stop_search == False and 'running' in st.session_state and st.session_state.running == True):
        st.session_state.running = True
        charlist = list("abcdefghijklmnopqrstuvwxyz")
        total_permutations = len(charlist) ** testlength
        progress_bar = st.progress(0)
        status = st.empty()
        result_placeholder = st.empty()
        found = False
        
        for i, pw in enumerate(generate_strings(charlist, testlength)):
            if st.session_state.stop_search:
                status.warning("Suche wurde vom Benutzer gestoppt!")
                break

            pw_hash = hash_password(pw)
            if pw_hash in dataleak_dict.values():
                name = get_name_by_hash(dataleak_dict, pw_hash)
                result_placeholder.success(f"✅ Passwort gefunden: {pw} ({name})")
                found = True

            if i % STEPSIZE == 0 or i == total_permutations - 1:
                progress_bar.progress((i) / total_permutations)
                status.text(f"Kombination {i} von {total_permutations} ({(100*i/total_permutations):.2f}%) wird getestet ...")

        if not found and not st.session_state.stop_search:
            result_placeholder.info("Kein Passwort gefunden.")
        status.text("Bruteforce abgeschlossen.")
        st.session_state.running = False

with tab3:
    st.header("🔀 Angriff Nummer 3: Verschiedene Charaktere")
    st.write(
        "Wähle Zeichensätze und experimentiere mit verschiedenen Passwortlängen. "
        "Erlebe, wie der Suchraum explodiert – und sehe die Fortschrittsanzeige live..."
    )
    char_options = {
        "Kleinbuchstaben": list("abcdefghijklmnopqrstuvwxyz"),
        "Großbuchstaben": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        "Zahlen": [str(i) for i in range(10)],
    }
    picked_sets = st.multiselect(
    "Zeichensätze auswählen", list(char_options.keys()), default=["Kleinbuchstaben"], key="charsets_tab3"
    )
    custom_chars = st.text_input("Zusätzliche Zeichen (z.B. @$!) ohne Leerzeichen und Komma hier eintragen", value="", key="custom_chars_tab3")
    charlist = []
    for s in picked_sets:
        charlist.extend(char_options[s])
    charlist.extend(list(custom_chars))
    charlist = list(set(charlist))
    tlength = st.slider("Passwortlänge", min_value=1, max_value=8, value=4, key="tab3len")

    start_btn_3 = st.button("Starten (Verschiedene Charaktere)")
    stop_btn_3 = st.button("Suche stoppen!")

    if stop_btn_3:
        st.session_state.stop_search = True
    if start_btn_3:
        st.session_state.stop_search = False

    if start_btn_3 or (not st.session_state.stop_search and 'running3' in st.session_state and st.session_state.running3):
        st.session_state.running3 = True
        total_perm = len(charlist) ** tlength
        progress_bar = st.progress(0)
        status = st.empty()
        result_placeholder = st.empty()
        found = False

        for idx, pw in enumerate(generate_strings(charlist, tlength)):
            if st.session_state.stop_search:
                status.warning("Suche wurde vom Benutzer gestoppt!")
                break

            pw_hash = hash_password(pw)
            if pw_hash in dataleak_dict.values():
                name = get_name_by_hash(dataleak_dict, pw_hash)
                result_placeholder.success(f"✅ Passwort gefunden: {pw} ({name})")
                found = True
                
            if idx % STEPSIZE == 0 or idx == total_perm - 1:
                progress_bar.progress((idx) / total_perm)
                status.text(f"Kombination {idx} von {total_perm} ({(100*idx/total_perm):.2f}%) wird getestet ...")

        if not found and not st.session_state.stop_search:
            result_placeholder.info("Kein Passwort aus der Datenbank.")
        status.text("Bruteforce abgeschlossen.")
        st.session_state.running3 = False

with tab4:
    st.header("🎭 Angriff Nummer 4: Gezielte Veränderungen (einfachere Eingabe)")
    st.write(
        "Definiere Ersetzungen zeilenweise in der Form Zeichen:Ersetzung1,Ersetzung2,...\n"
        "Beispiel:\n"
        "`a:@,3`\n"
        "`e:e,3`\n"
        "Verwende die Zeichensätze unten zur Auswahl des Grundwortes."
    )

    # Simplified substitution input: multi-line text box
    subs_simple = st.text_area(
        "Substitutionsregeln (einfaches Format, z.B. a:@,3 pro Zeile):",
        value="a:@,3\ns:$\ne:3"
    )

    # Parse the simple input into substitutions dict
    substitutions = {}
    for line in subs_simple.splitlines():
        line = line.strip()
        if not line:
            continue
        if ":" not in line:
            st.warning(f"Zeile ignoriert (kein ':'): {line}")
            continue
        key, vals = line.split(":", 1)
        key = key.strip()
        vals_list = [v.strip() for v in vals.split(",") if v.strip()]
        # Include the original character as valid substitution by default
        if key not in vals_list:
            vals_list.insert(0, key)
        substitutions[key] = vals_list

    # Character sets for base word (copied from tab3)
    char_options = {
        "Kleinbuchstaben": list("abcdefghijklmnopqrstuvwxyz"),
        "Großbuchstaben": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        "Zahlen": [str(i) for i in range(10)],
    }
    picked_sets = st.multiselect(
    "Zeichensätze auswählen", list(char_options.keys()), default=["Kleinbuchstaben"], key="charsets_tab4"
    )
    custom_chars = st.text_input("Zusätzliche Zeichen (z.B. @$!)", value="", key="custom_chars_tab4")
    base_chars = []
    for s in picked_sets:
        base_chars.extend(char_options[s])
    base_chars.extend(list(custom_chars))
    base_chars = list(set(base_chars))
    tlength_subs = st.slider("Passwortlänge", min_value=1, max_value=6, value=4, key="tab4len")

    start_btn_4 = st.button("Varianten-Test starten")
    stop_btn_4 = st.button("Suche stoppen.")

    if stop_btn_4:
        st.session_state.stop_search = True
    if start_btn_4:
        st.session_state.stop_search = False

    if start_btn_4 or (not st.session_state.stop_search and 'running4' in st.session_state and st.session_state.running4):
        st.session_state.running4 = True
        total_base = len(base_chars) ** tlength_subs
        progress_bar = st.progress(0)
        status = st.empty()
        result_placeholder = st.empty()
        found = False
        checked = 0

        for idx, base_word in enumerate(generate_strings(base_chars, tlength_subs)):
            if st.session_state.stop_search:
                status.warning("Suche wurde vom Benutzer gestoppt!")
                break

            for variant in apply_substitutions(base_word, substitutions):
                checked += 1
                pw_hash = hash_password(variant)
                if pw_hash in dataleak_dict.values():
                    name = get_name_by_hash(dataleak_dict, pw_hash)
                    result_placeholder.success(f"✅ Passwort gefunden: {variant} ({name})")
                    found = True
                    break
            if found:
                break
            if idx % STEPSIZE == 0 or idx == total_base - 1:
                progress_bar.progress((idx) / total_base)
                status.text(f"Wort {idx} von {total_base} getestet ({checked} Varianten gesamt) ...")

        if not found and not st.session_state.stop_search:
            result_placeholder.info("Kein Passwort mit Ersetzungen gefunden.")
        status.text("Fertig.")
        st.session_state.running4 = False
