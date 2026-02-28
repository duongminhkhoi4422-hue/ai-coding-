SUPPORTED_LANGUAGES = {
    "python": "python",
    "py": "python",

    "javascript": "javascript",
    "js": "javascript",

    "c++": "c++",
    "cpp": "c++",

    "java": "java",
    "html": "html"
}


def normalize_language(language: str) -> str:
    if not language:
        return "python"

    lang = language.strip().lower()

    if lang not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")

    return SUPPORTED_LANGUAGES[lang]