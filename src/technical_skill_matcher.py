import spacy
from spacy.matcher import PhraseMatcher


# Each standard name maps to spellings or aliases found in job postings
SKILL_PATTERNS = {
    "python": ["python", "python 3", "python 3.x"],
    "javascript": ["javascript"],
    "sql": ["sql"],
    "mysql": ["mysql"],
    "java": ["java"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "natural language processing": ["natural language processing", "nlp"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "power bi": ["power bi"],
    "tableau": ["tableau"],
    "excel": ["excel", "ms excel"],
    "html": ["html"],
    "css": ["css"],
    "react": ["react", "react.js"],
    "node.js": ["node.js", "nodejs"],
    "c++": ["c++"],
    "c#": ["c#"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes"],
    "git": ["git"],
    "linux": ["linux"],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization"],
}


# Create an English tokenizer without downloading a large language model
_nlp = spacy.blank("en")

# Match phrases without treating uppercase and lowercase as different
_matcher = PhraseMatcher(_nlp.vocab, attr="LOWER")

for standard_name, variants in SKILL_PATTERNS.items():
    patterns = [_nlp.make_doc(variant) for variant in variants]
    _matcher.add(standard_name, patterns)


def extract_technical_skills(value):
    """Find known technical skills in pipe-separated entries."""
    if value is None:
        return []

    found_skills = []

    # Match each source entry separately so phrases cannot cross a | boundary
    for item in str(value).split("|"):
        item = item.strip()
                # Treat JS as JavaScript only when it is a whole skill entry
        if item.casefold() == "js":
            if "javascript" not in found_skills:
                found_skills.append("javascript")
            continue

        if not item:
            continue

        document = _nlp.make_doc(item)
        matches = sorted(_matcher(document), key=lambda match: match[1])

        for match_id, start, end in matches:
            standard_name = _nlp.vocab.strings[match_id]

            if standard_name not in found_skills:
                found_skills.append(standard_name)

    return found_skills

