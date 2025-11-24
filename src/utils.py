def clean_text(text: str) -> str:
    """Cleans the input text by removing unnecessary whitespace and special characters."""
    return ' '.join(text.split())

def extract_sections(text: str, section_titles: list) -> dict:
    """Extracts specified sections from the text based on section titles."""
    sections = {}
    for title in section_titles:
        start_index = text.find(title)
        if start_index != -1:
            end_index = text.find('\n', start_index)
            sections[title] = text[start_index:end_index].strip()
    return sections

def log_message(message: str) -> None:
    """Logs a message to the console."""
    print(f"[LOG] {message}")