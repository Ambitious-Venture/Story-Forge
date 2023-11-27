def load_jinja_as_string(jinja_fp: str) -> str:
    with open(jinja_fp) as f:
        raw = f.readlines()
    lines = [line.replace("\n", "").strip() for line in raw]
    jinja_string = "".join(lines)
    return jinja_string