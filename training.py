from pathlib import Path


def get_urls_from_file(path: str):
    p = Path(path)
    with p.open() as f:
        lines = f.readlines()
    clean_lines = [line.strip(', \n"') for line in lines if line.strip(', \n"') and not line.strip().startswith("#")]
    return clean_lines


print(get_urls_from_file("URLS.txt"))