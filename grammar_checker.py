import re
from spellchecker import SpellChecker

spell = SpellChecker()


def split_sentences_with_lines(text):
    if text is None:
        return []

    text = str(text)
    lines = text.splitlines()
    results = []

    for line_no, line in enumerate(lines, start=1):
        clean_line = line.strip()

        if clean_line:
            sentences = re.split(r"(?<=[.!?])\s+", clean_line)

            for sentence in sentences:
                sentence = sentence.strip()
                if sentence:
                    results.append({
                        "line": line_no,
                        "sentence": sentence
                    })

    return results


def detect_spelling_errors(text):
    sentence_data = split_sentences_with_lines(text)
    spelling_results = []

    for item in sentence_data:
        words = re.findall(r"\b[a-zA-Z]{3,}\b", item["sentence"])

        clean_words = []
        for word in words:
            word = word.lower().strip()
            if word:
                clean_words.append(word)

        unknown_words = spell.unknown(clean_words)

        for wrong_word in unknown_words:
            try:
                candidates = spell.candidates(wrong_word)

                if candidates is None:
                    suggestions = []
                else:
                    suggestions = list(candidates)[:5]

            except Exception:
                suggestions = []

            spelling_results.append({
                "Line": item["line"],
                "Error Type": "Spelling Mistake",
                "Wrong Word": wrong_word,
                "Sentence": item["sentence"],
                "Suggestions": ", ".join(suggestions) if suggestions else "No suggestion"
            })

    return spelling_results


def detect_sentence_errors(text):
    sentence_data = split_sentences_with_lines(text)
    sentence_errors = []

    for item in sentence_data:
        sentence = item["sentence"].strip()

        if len(sentence.split()) < 3:
            sentence_errors.append({
                "Line": item["line"],
                "Error Type": "Short/Incomplete Sentence",
                "Issue": "Sentence seems too short or incomplete.",
                "Sentence": sentence
            })

        if sentence and sentence[0].islower():
            sentence_errors.append({
                "Line": item["line"],
                "Error Type": "Capitalization Error",
                "Issue": "Sentence should start with a capital letter.",
                "Sentence": sentence
            })

        if sentence and not sentence.endswith((".", "?", "!")):
            sentence_errors.append({
                "Line": item["line"],
                "Error Type": "Punctuation Error",
                "Issue": "Sentence may be missing ending punctuation.",
                "Sentence": sentence
            })

        if re.search(r"\s{2,}", sentence):
            sentence_errors.append({
                "Line": item["line"],
                "Error Type": "Spacing Error",
                "Issue": "Sentence contains extra spaces.",
                "Sentence": sentence
            })

    return sentence_errors


def generate_error_report(text):
    if text is None or str(text).strip() == "":
        return {
            "total_errors": 0,
            "spelling_errors": [],
            "sentence_errors": [],
            "spelling_count": 0,
            "sentence_count": 0
        }

    spelling_errors = detect_spelling_errors(text)
    sentence_errors = detect_sentence_errors(text)

    total_spelling = len(spelling_errors)
    total_sentence = len(sentence_errors)

    return {
        "total_errors": total_spelling + total_sentence,
        "spelling_errors": spelling_errors,
        "sentence_errors": sentence_errors,
        "spelling_count": total_spelling,
        "sentence_count": total_sentence
    }