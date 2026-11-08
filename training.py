from pathlib import Path


def get_urls_from_file(path: str):
    p = Path(path)
    try:

        with p.open(encoding="utf-8") as f:
            lines = f.readlines()
        clean_lines = [
    url
    for line in lines
    if (url := line.strip(', \n"'))
    and not url.startswith("#")
    and url.startswith(("https://", "http://"))
]
        clean_urls = list(dict.fromkeys(clean_lines))
        return clean_urls
    except Exception as e:
        print(f"File {path} not found")
        raise str(e).strip()

print(get_urls_from_file("URLS.txt"))