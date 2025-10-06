def get_version_info(version_file="version.txt"):
    info = {"Program": "Ksieg-OCR", "Commit": "-", "PR": "-"}
    try:
        with open(version_file, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    info[key.strip()] = value.strip()
    except Exception:
        pass
    return info
