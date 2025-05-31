import requests

def get_character_info_with_exp(name):
    base_url = "https://api.tibiadata.com/v4"

    # Busca personagem
    char_url = f"{base_url}/character/{name}"
    try:
        r = requests.get(char_url, timeout=15)
        r.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Erro de conexão: {e}"}

    char_data = r.json()
    if "character" not in char_data:
        return {"error": "Personagem não encontrado."}

    char = char_data["character"]["character"]
    world = char.get("world", None)
    if not world:
        return {"error": "Mundo do personagem não encontrado."}

    # Busca experiência no ranking do mundo (até 20 páginas)
    exp = None
    for page in range(1, 21):
        hs_url = f"{base_url}/highscores/{world}/experience/all/{page}"
        try:
            hs_r = requests.get(hs_url, timeout=15)
            hs_r.raise_for_status()
        except requests.RequestException:
            continue
        hs_data = hs_r.json()
        highscores = hs_data.get("highscores", {}).get("highscore_list", [])
        for entry in highscores:
            if entry["name"].lower() == name.lower():
                exp = entry.get("value")
                break
        if exp is not None:
            break

    # Monta resultado
    result = {
        "name": char.get("name"),
        "level": char.get("level"),
        "vocation": char.get("vocation"),
        "world": world,
        "experience": exp,
        "online": char_data["character"].get("online", False),
        "last_login": char.get("last_login"),
        "deaths": len(char_data["character"].get("deaths", []))
    }
    return result
