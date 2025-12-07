import os
import re
import json
import math
import traceback
from collections import Counter, defaultdict
from difflib import SequenceMatcher

# -----------------------------
# CONFIG
# -----------------------------
ROOT_DIR = "C:\qmm-igsoa\Organized_Papers"
OUTPUT_DIR = "./reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TERMS = [
    "substrate", "relation", "relational", "identity", "kernel",
    "instance", "agency", "cohesion", "msc", "msp", "mbc",
    "igsoa", "dfvm", "satp", "process", "attractor",
    "time", "field", "semantic"
]

VOLUME_HINTS = ["volume1", "volume2", "volume3"]

CONFIDENCE_WEIGHTS = {
    "definition_density": 0.35,
    "term_consistency": 0.35,
    "length_balance": 0.30
}

# Pairs we already treat as simple text-level contradictions
CONTRADICTION_TRIGGERS = [
    ("identity is", "identity is not"),
    ("substrate is", "substrate is not"),
    ("time is", "time is not"),
    ("kernel is", "kernel is not"),
    ("agency is intrinsic", "agency is emergent"),
    ("emergent", "fundamental"),
]

# Core subjects we care most about in definition collisions
CORE_DEFINITION_SUBJECTS = [
    "identity",
    "identity kernel",
    "kernel",
    "substrate",
    "agency",
    "time"
]

# Identity/Kernel misuse triggers (patterns to flag)
IK_MISUSE_PATTERNS = [
    # kernel treated as soul/persistent entity
    r"identity kernel\s+is\s+the\s+soul",
    r"identity\s+kernel\s+is\s+my\s+.*",
    r"kernel\s+is\s+my\s+.*",
    r"kernel\s+survives\s+death",
    r"kernel\s+persists\s+after\s+death",
    r"identity\s+kernel\s+persists\s+after",
    # kernel or substrate with agency
    r"identity\s+kernel\s+chooses",
    r"identity\s+kernel\s+decides",
    r"identity\s+kernel\s+wants",
    r"substrate\s+wants",
    r"substrate\s+decides",
    r"substrate\s+chooses",
    # identity as stored entity
    r"identity\s+is\s+stored\s+in",
    r"the\s+self\s+is\s+stored\s+as",
]

# -----------------------------
# SAFE UTILITIES
# -----------------------------
def safe_read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read(), None
    except Exception as e:
        return None, str(e)

def safe_extract_sections(text):
    try:
        sections = re.split(r"\n#+\s+", text)
        return [s.strip() for s in sections if len(s.strip()) > 300], None
    except Exception as e:
        return [], str(e)

def safe_similarity(a, b):
    try:
        return SequenceMatcher(None, a, b).ratio()
    except Exception:
        return 0.0

def safe_split_sentences(text):
    try:
        # Simple sentence split: good enough for our purposes
        return re.split(r"(?<=[.!?])\s+", text)
    except Exception:
        return [text]

def extract_definitions_from_text(text, path):
    """
    Extract candidate definition statements of the form:
    <subject> is (not)? <predicate>.
    Returns a list of dict entries for a global definition map.
    """
    results = []
    try:
        sentences = safe_split_sentences(text)
        pattern = re.compile(r"\b([a-z][a-z0-9\s\-]{1,40}?)\s+is\s+(not\s+)?([a-z][a-z0-9\s\-]{1,80})", re.IGNORECASE)

        for sent in sentences:
            sent_l = sent.strip()
            if len(sent_l) < 15:
                continue
            m = pattern.search(sent_l)
            if not m:
                continue
            subject = m.group(1).strip().lower()
            neg = True if m.group(2) else False
            predicate = m.group(3).strip().lower()
            results.append({
                "subject": subject,
                "negated": neg,
                "predicate": predicate,
                "sentence": sent_l,
                "file": path
            })
    except Exception:
        # Fail-soft: return what we have so far
        return results
    return results

def normalized_subject_key(subject):
    """
    Normalize definition subject to help align variants like:
    'the identity', 'identity', 'human identity'
    """
    s = subject.strip().lower()
    s = re.sub(r"^(the|a|an)\s+", "", s)
    # keep core words only, truncate trailing phrases
    tokens = s.split()
    if len(tokens) > 3:
        tokens = tokens[:3]
    return " ".join(tokens)

# -----------------------------
# GLOBAL ACCUMULATORS
# -----------------------------
global_term_counter = Counter()
volume_term_map = defaultdict(Counter)
file_reports = {}
redundancy_pairs = []
contradictions = []
logic_contradictions = []
definition_collisions = []
ik_misuse = []
error_log = []
all_sections = []

# subject -> list of definition entries
definition_map = defaultdict(list)

# -----------------------------
# MAIN SCAN (FAIL-SAFE)
# -----------------------------
for root, _, files in os.walk(ROOT_DIR):
    for f in files:
        if not f.lower().endswith(".md"):
            continue

        path = os.path.join(root, f)
        raw, err = safe_read_file(path)

        if err:
            error_log.append({"file": path, "stage": "read", "error": err})
            continue

        try:
            txt = raw
            lower_txt = txt.lower()
            words = re.findall(r"[a-zA-Z\-]{3,}", lower_txt)
            counts = Counter(words)

            term_hits = {t: counts.get(t, 0) for t in TERMS}

            sections, sec_err = safe_extract_sections(lower_txt)
            if sec_err:
                error_log.append({"file": path, "stage": "section_split", "error": sec_err})

            for s in sections:
                all_sections.append((path, s))

            # Volume tagging
            vol = "unassigned"
            for v in VOLUME_HINTS:
                if v in path.lower():
                    vol = v
                    break

            volume_term_map[vol].update(term_hits)

            # -------- CONFIDENCE SCORE ----------
            length_words = len(words)
            definition_density = sum(1 for w in words if w in ["is", "are", "defined"]) / max(length_words, 1)

            term_consistency = sum(term_hits.values()) / max(len(TERMS), 1)
            length_balance = 1.0 - abs(length_words - 2500) / 4000
            length_balance = max(0.0, min(length_balance, 1.0))

            confidence_score = (
                CONFIDENCE_WEIGHTS["definition_density"] * definition_density +
                CONFIDENCE_WEIGHTS["term_consistency"] * term_consistency +
                CONFIDENCE_WEIGHTS["length_balance"] * length_balance
            )

            # -------- TERMINOLOGY VOLATILITY ----------
            volatility = math.sqrt(sum((counts[t] - global_term_counter.get(t, 0)) ** 2 for t in TERMS))

            file_reports[path] = {
                "length_words": length_words,
                "term_density": term_hits,
                "confidence_score": round(confidence_score, 3),
                "terminology_volatility": round(volatility, 3),
                "volume": vol
            }

            global_term_counter.update(term_hits)

            # -------- DEFINITION EXTRACTION ----------
            defs = extract_definitions_from_text(lower_txt, path)
            for d in defs:
                subj_key = normalized_subject_key(d["subject"])
                definition_map[subj_key].append(d)

            # -------- IDENTITY/KERNEL MISUSE DETECTION ----------
            for pattern in IK_MISUSE_PATTERNS:
                try:
                    if re.search(pattern, lower_txt):
                        ik_misuse.append({
                            "file": path,
                            "pattern": pattern
                        })
                except Exception as e:
                    error_log.append({
                        "file": path,
                        "stage": "ik_misuse_pattern",
                        "pattern": pattern,
                        "error": str(e)
                    })
                    continue

        except Exception as e:
            error_log.append({
                "file": path,
                "stage": "analysis",
                "error": str(e),
                "trace": traceback.format_exc()
            })
            continue

# -----------------------------
# REDUNDANCY SCAN
# -----------------------------
for i in range(len(all_sections)):
    a_path, a_txt = all_sections[i]
    for j in range(i + 1, len(all_sections)):
        b_path, b_txt = all_sections[j]
        if a_path == b_path:
            continue

        sim = safe_similarity(a_txt, b_txt)
        if sim > 0.88:
            redundancy_pairs.append({
                "file_a": a_path,
                "file_b": b_path,
                "similarity": round(sim, 3)
            })

# -----------------------------
# SIMPLE TEXT CONTRADICTION DETECTION
# -----------------------------
for path, info in file_reports.items():
    text, _ = safe_read_file(path)
    if not text:
        continue
    t = text.lower()

    for a, b in CONTRADICTION_TRIGGERS:
        if a in t and b in t:
            contradictions.append({
                "file": path,
                "pattern": f"{a} <-> {b}"
            })

# -----------------------------
# LOGIC-GRAPH CONTRADICTION DETECTION
# -----------------------------
# We treat each subject as a node and each definition as:
#   subject --(is / is-not)--> predicate
# We flag:
#   1) Same subject with both negated and non-negated predicates
#   2) Same subject with significantly different predicates across files
logic_contradictions = []
definition_collisions = []

for subj, defs in definition_map.items():
    if len(defs) < 2:
        continue

    # A) Negation conflicts
    neg_states = set(d["negated"] for d in defs)
    if len(neg_states) > 1:
        logic_contradictions.append({
            "subject": subj,
            "type": "negation_conflict",
            "definitions": defs
        })

    # B) Predicate collisions (dissimilar predicates)
    # Focus more strongly on core subjects
    is_core = any(subj.startswith(core) for core in CORE_DEFINITION_SUBJECTS)
    pred_pairs = []
    for i in range(len(defs)):
        for j in range(i + 1, len(defs)):
            p1 = defs[i]["predicate"]
            p2 = defs[j]["predicate"]
            sim = safe_similarity(p1, p2)
            pred_pairs.append((sim, i, j))

    # Flag worst pairs if similarity too low
    for sim, i, j in pred_pairs:
        if sim < 0.5:  # threshold: obviously incompatible statements
            definition_collisions.append({
                "subject": subj,
                "predicate_a": defs[i]["predicate"],
                "predicate_b": defs[j]["predicate"],
                "similarity": round(sim, 3),
                "file_a": defs[i]["file"],
                "file_b": defs[j]["file"],
                "core_subject": is_core
            })

# -----------------------------
# CROSS-VOLUME DRIFT DETECTION
# -----------------------------
cross_volume_drift = {}
volumes = list(volume_term_map.keys())

for i in range(len(volumes)):
    for j in range(i + 1, len(volumes)):
        v1, v2 = volumes[i], volumes[j]
        dist = math.sqrt(sum(
            (volume_term_map[v1][t] - volume_term_map[v2][t]) ** 2
            for t in TERMS
        ))
        cross_volume_drift[f"{v1} ↔ {v2}"] = round(dist, 3)

# -----------------------------
# OUTPUT (ALWAYS WRITES)
# -----------------------------
with open(os.path.join(OUTPUT_DIR, "file_micro_reports.json"), "w") as f:
    json.dump(file_reports, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "global_term_density.json"), "w") as f:
    json.dump(global_term_counter, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "redundancy_risks.json"), "w") as f:
    json.dump(redundancy_pairs, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "terminology_volatility.json"), "w") as f:
    json.dump({k: v["terminology_volatility"] for k, v in file_reports.items()}, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "confidence_scores.json"), "w") as f:
    json.dump({k: v["confidence_score"] for k, v in file_reports.items()}, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "cross_volume_drift.json"), "w") as f:
    json.dump(cross_volume_drift, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "contradictions_simple.json"), "w") as f:
    json.dump(contradictions, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "logic_contradictions.json"), "w") as f:
    json.dump(logic_contradictions, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "definition_collisions.json"), "w") as f:
    json.dump(definition_collisions, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "ik_misuse.json"), "w") as f:
    json.dump(ik_misuse, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "processing_errors.json"), "w") as f:
    json.dump(error_log, f, indent=2)

print("✅ FULL BOOK AUDIT COMPLETE (FAIL-SAFE MODE).")
print("Generated:")
print("- file_micro_reports.json")
print("- global_term_density.json")
print("- redundancy_risks.json")
print("- terminology_volatility.json")
print("- confidence_scores.json")
print("- cross_volume_drift.json")
print("- contradictions_simple.json")
print("- logic_contradictions.json")
print("- definition_collisions.json")
print("- ik_misuse.json")
print("- processing_errors.json")
print(f"⚠️ Files with errors: {len(error_log)}")
