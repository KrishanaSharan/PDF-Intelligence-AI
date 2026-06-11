import re
from collections import Counter

STOP_WORDS = {
    "the", "is", "are", "a", "an", "and", "or", "to", "of", "in", "on",
    "for", "with", "as", "by", "this", "that", "from", "it", "be", "was",
    "were", "has", "have", "had", "at", "not", "can", "will", "their",
    "they", "them", "these", "those", "into", "also", "which"
}

def get_document_stats(text, pages):
    words = text.split()
    sentences = re.split(r"[.!?]", text)

    word_count = len(words)
    char_count = len(text)
    sentence_count = len([s for s in sentences if s.strip()])
    read_time = max(1, round(word_count / 200))

    return {
        "pages": pages,
        "words": word_count,
        "characters": char_count,
        "sentences": sentence_count,
        "read_time": read_time
    }

def get_top_keywords(text, limit=10):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    filtered = [w for w in words if w not in STOP_WORDS]
    counter = Counter(filtered)
    return counter.most_common(limit)

def get_complexity_score(text):
    words = text.split()
    sentences = re.split(r"[.!?]", text)
    sentences = [s for s in sentences if s.strip()]

    if not words or not sentences:
        return {
            "avg_sentence_length": 0,
            "avg_word_length": 0,
            "level": "Unknown"
        }

    avg_sentence_length = round(len(words) / len(sentences), 2)
    avg_word_length = round(sum(len(w) for w in words) / len(words), 2)

    if avg_sentence_length < 12:
        level = "Easy"
    elif avg_sentence_length < 20:
        level = "Medium"
    else:
        level = "Advanced"

    return {
        "avg_sentence_length": avg_sentence_length,
        "avg_word_length": avg_word_length,
        "level": level
    }