import json


def clean_strings(value):
    if isinstance(value, dict):
        return {key: clean_strings(item) for key, item in value.items()}
    if isinstance(value, list):
        return [clean_strings(item) for item in value]
    if isinstance(value, str):
        return value.replace(' ', '').replace('\n', '')
    return value


def main():
    file_path = "/home/exti/Desktop/HDD/some-shit/code/gitReposses/HH_pars_HW/meta_data/vacancy_data.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = clean_strings(data)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()