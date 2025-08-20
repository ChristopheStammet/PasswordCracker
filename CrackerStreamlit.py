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
    "Hannah": "5ebe2294ecd0e0f08eab7690d2a6ee69",
    "Ilsa": "b085d1bf4cff8b1045750706b11f8662",
    "Jhempi": "b850780bb2b06e0cf81afb7a2efebb1a",
    "Klara": "4fc963e213bba362778f5c175eb4d5ff",
    "Louis": "20f67615263a20bab5a20b903b92b4be",
    "Maren": "41e4652a622b10077ff4c22717dc57fd",
    "Nico": "5de2bcf647b707104e4513262903866c",
    "Olivia": "6ae860c71585153c82dd6cff37048b12",
    "Pedro": "bacce9269a7cfddeddae9ebe4c08205e",
    "Qi": "691d86337f15e81b7d245b7c7fc200a6",
    "Robert": "48e6c9d963b4ec1c7507c505d577a6ad",
    "Svenja": "fb4ab6f83b490f6220ad2a4163f88904",
    "Tom": "f1174e62d60a92010c4a72fe87805ae1",
    "Ulrike": "1ee3f5963241d4a05e786c9f7aae7a14",
    "Victor": "4de8e33e649c6ee317c7937804b63fc1",
    "Wilhelmina": "c00271e856c0921bc0b7e900e8f9bcd1",
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
    st.write(
        "Hier werden alle Kombinationen von Kleinbuchstaben mit einer bestimmten Länge ausprobiert. "
        "Achtung: Je länger das Passwort, desto mehr dauert die Suche!"
    )
    testlength = st.slider("Passwortlänge auswählen", min_value=1, max_value=8, value=4)
    run_bruteforce = st.button("Bruteforce starten")

    if run_bruteforce:
        charlist = list("abcdefghijklmnopqrstuvwxyz")
        total_permutations = len(charlist) ** testlength
        progress_bar = st.progress(0)
        found = False

        # Add status text and placeholder for result display
        status = st.empty()
        result_placeholder = st.empty()
        for i, pw in enumerate(generate_strings(charlist, testlength)):
            pw_hash = hash_password(pw)
            if pw_hash in dataleak:
                name = get_name_by_hash(dataleak_dict, pw_hash)
                result_placeholder.success(f"✅ Passwort gefunden: {pw} ({name})")
                found = True
                break
            if i % 50000 == 0 or i == total_permutations - 1:
                progress_bar.progress((i + 1) / total_permutations)
                status.text(f"Teste Kombination {i + 1} von {total_permutations} ...")
        if not found:
            result_placeholder.info("Kein Passwort aus der Datenbank gefunden.")
        status.text("Bruteforce abgeschlossen.")

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
        "Zeichensätze auswählen", list(char_options.keys()), default=["Kleinbuchstaben"]
    )
    custom_chars = st.text_input("Zusätzliche Zeichen (optional)", value="")
    charlist = []
    for s in picked_sets:
        charlist.extend(char_options[s])
    charlist.extend(list(custom_chars))
    charlist = list(set(charlist))
    tlength = st.slider("Passwortlänge", min_value=1, max_value=8, value=4, key="tab3len")

    if st.button("Starten (Verschiedene Charaktere)"):
        if not charlist:
            st.error("Bitte mind. einen Zeichensatz auswählen oder eigene Zeichen angeben!")
        else:
            total_perm = len(charlist)**tlength
            progress_bar = st.progress(0)
            found = False
            status = st.empty()
            result_placeholder = st.empty()
            for idx, pw in enumerate(generate_strings(charlist, tlength)):
                pw_hash = hash_password(pw)
                if pw_hash in dataleak:
                    name = get_name_by_hash(dataleak_dict, pw_hash)
                    result_placeholder.success(f"✅ Passwort gefunden: {pw} ({name})")
                    found = True
                    break
                if idx % 1000 == 0 or idx == total_perm - 1:
                    progress_bar.progress((idx + 1) / total_perm)
                    status.text(f"Kombination {idx+1} von {total_perm} wird getestet ...")
            if not found:
                result_placeholder.info("Kein Passwort aus der Datenbank.")
            status.text("Bruteforce abgeschlossen.")

with tab4:
    st.header("🎭 Angriff Nummer 4: Gezielte Veränderungen")
    st.write(
        "Viele Passwörter werden mit typischen Ersetzungen variiert,\n"
        "z.B. a→@, e→3, s→$ usw. Definiere Deine eigenen Ersetzungen unten "
        "und lasse den Computer alle Möglichkeiten testen – natürlich mit Fortschrittsanzeige!"
    )

    subs_input = st.text_area(
        "Substitutionsregeln (Python-Dictionary-Syntax, z.B.: {'a': ['a', '@'], 'e': ['e', '3']})",
        "{'a': ['a', '@', ''], 'e': ['e', '3', '']}"
    )
    try:
        substitutions = ast.literal_eval(subs_input)
        assert isinstance(substitutions, dict), "Muss ein Dictionary sein."
    except Exception as e:
        st.error(f"Fehler beim Parsen der Regeln: {e}")
        substitutions = {'a': ['a', '@', ''], 'e': ['e', '3', '']}
    
    charlist = st.text_input(
        "Verwendbare Zeichen für Grundwort (als durchgehender String)",
        value="abcdefghijklmnopqrstuvwxyz"
    )
    try:
        basechars = list(charlist)
        assert basechars, "Zeichenliste darf nicht leer sein."
    except:
        basechars = list("abcdefghijklmnopqrstuvwxyz")
    tlength = st.slider("Passwortlänge", min_value=1, max_value=6, value=4, key="tab4len")

    if st.button("Varianten-Test starten"):
        total_base = len(basechars)**tlength
        progress_bar = st.progress(0)
        status = st.empty()
        result_placeholder = st.empty()
        checked = 0
        found = False
        for idx, base_word in enumerate(generate_strings(basechars, tlength)):
            found_this_round = False
            variant_count = 0
            for variant in apply_substitutions(base_word, substitutions):
                checked += 1
                variant_count += 1
                pw_hash = hash_password(variant)
                if pw_hash in dataleak:
                    name = get_name_by_hash(dataleak_dict, pw_hash)
                    result_placeholder.success(f"✅ Passwort gefunden: {variant} ({name})")
                    found = True
                    found_this_round = True
                    break
            if idx % 100 == 0 or idx == total_base - 1:
                progress_bar.progress((idx + 1) / total_base)
                status.text(f"Wort {idx+1} von {total_base} ({checked} Varianten gesamt geprüft...)")
            if found_this_round:
                break
        if not found:
            result_placeholder.info("Kein Passwort mit Ersetzungen gefunden.")
        status.text("Fertig.")
