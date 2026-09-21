#!/usr/bin/env python3
"""
Typeset Favour Tumba's resume as a one-page, ATS-friendly PDF.

Why a script instead of a word-processor export:
  * fonts are embedded (subset) so the PDF renders identically everywhere
  * email, phone, portfolio, LinkedIn and GitHub are real clickable links
  * spacing is driven by a single scale factor that auto-fits to one page
  * the text layer stays a plain single-column flow, which is what ATS parsers read

Usage:  python resume/build_resume.py [output.pdf ...]
"""

from __future__ import annotations

import io
import os
import re
import sys

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# --------------------------------------------------------------------------
# fonts
# --------------------------------------------------------------------------

FONT_DIR = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")

# Segoe UI has a large x-height for its width, so it holds a readable apparent
# size in the space available. Semibold carries the name and section rules;
# bold is reserved for employer/project titles.
_FACES = [
    ("Body", "segoeui.ttf"),
    ("Body-B", "segoeuib.ttf"),
    ("Body-I", "segoeuii.ttf"),
    ("Body-BI", "segoeuiz.ttf"),
    ("Body-SB", "seguisb.ttf"),
    ("Display", "seguisb.ttf"),
]


def register_fonts() -> None:
    missing = []
    for name, filename in _FACES:
        path = os.path.join(FONT_DIR, filename)
        if not os.path.exists(path):
            missing.append(filename)
            continue
        pdfmetrics.registerFont(TTFont(name, path))
    if missing:
        raise SystemExit("Missing system fonts: " + ", ".join(missing))
    pdfmetrics.registerFontFamily(
        "Body", normal="Body", bold="Body-B", italic="Body-I", boldItalic="Body-BI"
    )


# --------------------------------------------------------------------------
# palette + page geometry
# --------------------------------------------------------------------------

INK = HexColor("#14181F")    # body text - reads as black in print
ACCENT = HexColor("#1F3D63")  # deep slate blue - name, headings, links
MUTED = HexColor("#535D6B")   # dates, locations, secondary text
RULE = HexColor("#AEB8C4")    # hairlines

PAGE_W, PAGE_H = LETTER
MARGIN_X = 40.0
MARGIN_TOP = 38.0
MARGIN_BOTTOM = 32.0
LEFT = MARGIN_X
RIGHT = PAGE_W - MARGIN_X
COL_W = RIGHT - LEFT


# --------------------------------------------------------------------------
# content
# --------------------------------------------------------------------------

NAME = "FAVOUR TUMBA"
TAGLINE = "Software Engineer  \u00b7  AI, Backend & Full-Stack Systems"

CONTACT_ROWS = [
    [
        ("tumbafavour1@gmail.com", "mailto:tumbafavour1@gmail.com"),
        ("+234 704 297 3276", "tel:+2347042973276"),
        ("Abuja, Nigeria", None),
    ],
    [
        ("tumbafavour.github.io", "https://tumbafavour.github.io"),
        ("linkedin.com/in/favour-tumba", "https://linkedin.com/in/favour-tumba"),
        ("github.com/tumbafavour", "https://github.com/tumbafavour"),
    ],
]

SUMMARY = (
    "Software engineer building AI, backend, and full-stack systems in Python and TypeScript. "
    "First Class Computer Science graduate (GPA 4.57/5.00) who has designed and shipped end-to-end "
    "applications including an LLM observability platform and a retrieval-augmented document "
    "question-answering API, combining FastAPI services, PostgreSQL persistence, and LLM integrations."
)

SKILLS = [
    ("Languages", "Python, TypeScript, JavaScript, SQL, Bash"),
    ("AI / ML", "Claude API, OpenAI, LiteLLM, RAG, pgvector, LLM Evaluation & Observability, "
                "scikit-learn, pandas"),
    ("Backend & Data", "FastAPI, Node.js, RESTful APIs, SQLAlchemy, PostgreSQL (Neon), Redis, Celery"),
    ("Frontend", "React, Next.js, TanStack, HTML5, CSS3"),
    ("DevOps & Tools", "Docker, GitHub Actions, CI/CD, Git, Linux, pytest, Streamlit"),
]

EXPERIENCE = [
    {
        "org": "AfterQuery",
        "role": "Software Engineer",
        "note": "promoted from Mid-Level Full-Stack Engineer",
        "where": "Remote",
        "dates": "Aug 2026 \u2013 Present",
        "bullets": [
            "Build and ship full-stack product features across React and TypeScript interfaces and Python "
            "backend services, working from API design through to deployment.",
            "Contribute to code review, automated testing, and iterative delivery within a distributed "
            "engineering team.",
        ],
    },
    {
        "org": "Anazemma Global Enterprises Nigeria Limited",
        "role": "Software Engineer",
        "note": None,
        "where": "Abuja, Nigeria",
        "dates": "Apr 2026 \u2013 Present",
        "bullets": [
            "Maintain the company's office server, website, and broader IT infrastructure, and support data "
            "collection, cleaning, and analysis workflows for the business.",
        ],
    },
    {
        "org": "National Information Technology Development Agency (NITDA)",
        "role": "IT Intern",
        "note": None,
        "where": "Abuja, Nigeria",
        "dates": "Mar 2024 \u2013 Sep 2024",
        "bullets": [
            "Wrote Python scripts to organize, sort, and filter operational data, increasing data management "
            "efficiency by 25% and team data accessibility by 30%.",
            "Collaborated with the IT team to streamline workflows and reduce redundant data handling by 20%, "
            "alongside public digital literacy initiatives.",
        ],
    },
]

PROJECTS = [
    {
        "name": "LLM Evaluation & Observability Platform",
        "sub": "Python, FastAPI, PostgreSQL (Neon), SQLAlchemy, Streamlit",
        "dates": "Jul 2026 \u2013 Present",
        "bullets": [
            "Built an observability service that traces every LLM call, covering prompt, response, tokens, "
            "latency, and cost, through a FastAPI ingestion API backed by PostgreSQL.",
            "Created a Python SDK that wraps LLM calls to report traces automatically, plus a Streamlit "
            "dashboard charting cost, latency, and error trends over time.",
        ],
    },
    {
        "name": "Document Intelligence API",
        "sub": "Python, FastAPI, PostgreSQL, pgvector, Docker, Claude API, OpenAI Embeddings",
        "dates": "Jul 2026 \u2013 Present",
        "bullets": [
            "Built a document question-answering REST API with FastAPI that ingests PDFs, chunks and embeds "
            "them, and answers questions with structured citations from the Claude API.",
            "Implemented hybrid retrieval fusing PostgreSQL full-text search with pgvector embeddings via "
            "Reciprocal Rank Fusion, with cost and latency telemetry on every query.",
        ],
    },
    {
        "name": "Heart Disease Risk Prediction",
        "sub": "Python, scikit-learn, pandas, Streamlit",
        "dates": "Final Year Project  \u00b7  2024 \u2013 2025",
        "bullets": [
            "Trained and compared machine-learning models on the Framingham Heart Study dataset "
            "(4,240 patients) to predict 10-year coronary heart disease risk, handling class imbalance with "
            "SMOTE and evaluating with ROC-AUC.",
            "Built a leakage-free scikit-learn pipeline and a Streamlit web app that turns a patient's health "
            "details into a risk percentage.",
        ],
    },
    {
        "name": "Additional Projects",
        "sub": None,
        "dates": "Jul 2026 \u2013 Present",
        "bullets": [
            "Transformer From Scratch (PyTorch) \u2014 GPT-style language model with causal self-attention.  "
            "RelayQ (Python, Redis) \u2014 Celery-like task queue with retries, backoff, priorities, and "
            "dead-letter queues.",
        ],
    },
]

EDUCATION = {
    "school": "B.Sc. Computer Science \u2014 Landmark University, Nigeria",
    "dates": "Graduated August 2025",
    "lines": [
        [("First Class Honours", True),
         ("  |  GPA: 4.57/5.00  |  Concentrations: Artificial Intelligence, Python Programming", False)],
        [("Relevant Coursework: ", True),
         ("Data Structures & Algorithms, Database Design & Management, Machine Learning, Artificial "
          "Intelligence, Object-Oriented Programming", False)],
    ],
}

CERTIFICATIONS = [
    ("Supervised Machine Learning: Regression and Classification",
     "DeepLearning.AI & Stanford (Coursera, Jan 2026)",
     "https://coursera.org/share/099f01dc41be76a3d7e82526a4e3f9a6"),
    ("Python for Data Science, AI & Development",
     "IBM (Coursera, Jun 2026)",
     "https://coursera.org/share/2d457c8efbf5b3a6ec965783407b37ee"),
]


# --------------------------------------------------------------------------
# tiny rich-text layout engine
# --------------------------------------------------------------------------

def run(text, font="Body", size=9.5, color=INK, url=None, track=0.0):
    return {"t": text, "f": font, "s": size, "c": color, "url": url, "track": track}


def _tokenize(runs):
    toks = []
    for r in runs:
        for part in re.split(r"(\s+)", r["t"]):
            if not part:
                continue
            tok = dict(r)
            tok["t"] = part
            tok["sp"] = part.isspace()
            toks.append(tok)
    return toks


def _tok_w(tok):
    return pdfmetrics.stringWidth(tok["t"], tok["f"], tok["s"]) + tok["track"] * len(tok["t"])


def _wrap(toks, width, hang=0.0):
    lines, cur, cur_w, avail = [], [], 0.0, width
    for tok in toks:
        tw = _tok_w(tok)
        if tok["sp"]:
            if cur:
                cur.append(tok)
                cur_w += tw
            continue
        if cur and cur_w + tw > avail + 0.01:
            while cur and cur[-1]["sp"]:
                cur.pop()
            lines.append(cur)
            cur, cur_w, avail = [tok], tw, width - hang
        else:
            cur.append(tok)
            cur_w += tw
    if cur:
        while cur and cur[-1]["sp"]:
            cur.pop()
        lines.append(cur)
    return lines


def _line_w(line):
    return sum(_tok_w(t) for t in line)


def put(c, x, y, s, font, size, color, track=0.0):
    """Draw a single string.

    Character tracking lives on the text object, not the canvas. Tc is part of
    the PDF text state and persists across text objects, so it must be set on
    every call - otherwise tracking set once for the name leaks into the whole
    document and every string renders wider than stringWidth() measured it.
    """
    t = c.beginText(x, y)
    t.setFont(font, size)
    t.setFillColor(color)
    t.setCharSpace(track)
    t.textOut(s)
    c.drawText(t)


def _draw_line(c, line, x, y):
    link = None  # (url, x0, x1, size) for the run of tokens currently sharing a URL

    def flush():
        if link:
            url, x0, x1, size = link
            c.linkURL(url, (x0, y - 2.0, x1, y + size * 0.78), relative=0)

    for tok in line:
        put(c, x, y, tok["t"], tok["f"], tok["s"], tok["c"], tok["track"])
        w = _tok_w(tok)
        if tok["url"]:
            if link and link[0] == tok["url"]:
                link = (link[0], link[1], x + w, max(link[3], tok["s"]))
            else:
                flush()
                link = (tok["url"], x, x + w, tok["s"])
        else:
            flush()
            link = None
        x += w
    flush()


def draw_runs(c, runs, x, y, width, leading, hang=0.0, align="left"):
    """Draw wrapped rich text with its first baseline at `y`. Returns the next baseline."""
    lines = _wrap(_tokenize(runs), width, hang)
    for i, line in enumerate(lines):
        lx = x + (0.0 if i == 0 else hang)
        if align == "center":
            lx = x + (width - _line_w(line)) / 2.0
        _draw_line(c, line, lx, y)
        y -= leading
    return y


# --------------------------------------------------------------------------
# document
# --------------------------------------------------------------------------

def build_page(c: canvas.Canvas, k: float) -> float:
    """Render the resume at scale `k` (type sizes and rhythm together).

    Returns the final baseline y, which the caller compares against the bottom
    margin to decide whether the page fits.
    """

    name_s = 21.0 * k
    tag_s = 8.2 * k
    contact_s = 8.6 * k
    sec_s = 8.9 * k
    title_s = 10.0 * k
    sub_s = 9.0 * k
    date_s = 8.6 * k
    body = 9.3 * k
    lead = body * 1.235

    gap_sec = 11.0 * k     # space above a section rule
    gap_entry = 5.6 * k    # space between entries
    gap_small = 2.0 * k

    def section(y, title, bookmark):
        y -= gap_sec
        track = 1.45 * k
        put(c, LEFT, y, title, "Body-B", sec_s, ACCENT, track)
        w = pdfmetrics.stringWidth(title, "Body-B", sec_s) + track * len(title)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.7)
        c.line(LEFT + w + 9, y + 2.8, RIGHT, y + 2.8)
        c.bookmarkHorizontalAbsolute(bookmark, y + 18)
        c.addOutlineEntry(title.title(), bookmark, level=0)
        return y - (11.6 * k)

    def entry_head(y, left_runs, right_text):
        rw = 0.0
        if right_text:
            rw = pdfmetrics.stringWidth(right_text, "Body", date_s)
            put(c, RIGHT - rw, y, right_text, "Body", date_s, MUTED)
        return draw_runs(c, left_runs, LEFT, y, COL_W - rw - 14, lead)

    def bullet(y, text):
        ind = 10.0 * k
        put(c, LEFT + 1.5, y, "\u2022", "Body", body, MUTED)
        return draw_runs(c, [run(text, size=body)], LEFT + ind, y, COL_W - ind, lead)

    # ---- header ----------------------------------------------------------
    y = PAGE_H - MARGIN_TOP - name_s * 0.74

    n_track = 1.8 * k
    nw = pdfmetrics.stringWidth(NAME, "Display", name_s) + n_track * len(NAME)
    put(c, LEFT + (COL_W - nw) / 2.0, y, NAME, "Display", name_s, ACCENT, n_track)
    y -= 12.6 * k

    tag = TAGLINE.upper()
    t_track = 1.2 * k
    tw = pdfmetrics.stringWidth(tag, "Body", tag_s) + t_track * len(tag)
    put(c, LEFT + (COL_W - tw) / 2.0, y, tag, "Body", tag_s, MUTED, t_track)
    y -= 12.6 * k

    for row in CONTACT_ROWS:
        runs = []
        for i, (label, url) in enumerate(row):
            if i:
                runs.append(run("   \u00b7   ", size=contact_s, color=RULE))
            runs.append(run(label, size=contact_s, color=ACCENT if url else MUTED, url=url))
        y = draw_runs(c, runs, LEFT, y, COL_W, 10.8 * k, align="center")

    y += 1.0 * k
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.1)
    c.line(LEFT, y, RIGHT, y)
    y -= 3.0 * k

    # ---- summary ---------------------------------------------------------
    y = section(y, "PROFESSIONAL SUMMARY", "summary")
    y = draw_runs(c, [run(SUMMARY, size=body)], LEFT, y, COL_W, lead)

    # ---- skills ----------------------------------------------------------
    y = section(y, "TECHNICAL SKILLS", "skills")
    label_w = max(pdfmetrics.stringWidth(lbl + ":", "Body-B", body) for lbl, _ in SKILLS) + 7
    for lbl, items in SKILLS:
        put(c, LEFT, y, lbl + ":", "Body-B", body, ACCENT)
        y = draw_runs(c, [run(items, size=body)], LEFT + label_w, y, COL_W - label_w, lead)

    # ---- experience ------------------------------------------------------
    y = section(y, "EXPERIENCE", "experience")
    for i, job in enumerate(EXPERIENCE):
        if i:
            y -= gap_entry
        left = [run(job["org"], "Body-B", title_s, INK),
                run("  —  ", "Body", sub_s, RULE),
                run(job["role"], "Body-I", sub_s, ACCENT)]
        if job["note"]:
            left.append(run("  (" + job["note"] + ")", "Body-I", sub_s * 0.95, MUTED))
        y = entry_head(y, left, job["where"] + "  ·  " + job["dates"])
        y -= gap_small
        for b in job["bullets"]:
            y = bullet(y, b)

    # ---- projects --------------------------------------------------------
    y = section(y, "PROJECTS", "projects")
    for i, proj in enumerate(PROJECTS):
        if i:
            y -= gap_entry
        left = [run(proj["name"], "Body-B", title_s, INK)]
        if proj["sub"]:
            left.append(run("  —  ", "Body", sub_s, RULE))
            left.append(run(proj["sub"], "Body-I", sub_s, MUTED))
        y = entry_head(y, left, proj["dates"])
        y -= gap_small
        for b in proj["bullets"]:
            y = bullet(y, b)

    # ---- education -------------------------------------------------------
    y = section(y, "EDUCATION & CERTIFICATIONS", "education")
    y = entry_head(y, [run(EDUCATION["school"], "Body-B", title_s, INK)], EDUCATION["dates"])
    for parts in EDUCATION["lines"]:
        runs = [run(t, "Body-B" if bold else "Body", sub_s, INK if bold else MUTED)
                for t, bold in parts]
        y = draw_runs(c, runs, LEFT, y, COL_W, lead)

    y -= gap_small
    for name, issuer, url in CERTIFICATIONS:
        runs = [run("\u2022  ", size=sub_s, color=MUTED),
                run(name, "Body", sub_s, ACCENT, url=url),
                run(" \u2014 " + issuer, "Body", sub_s, MUTED)]
        y = draw_runs(c, runs, LEFT, y, COL_W, lead, hang=10.0 * k)

    return y


def render(scale: float, stream):
    c = canvas.Canvas(stream, pagesize=LETTER, pageCompression=1)
    c.setTitle("Favour Tumba \u2014 Software Engineer Resume")
    c.setAuthor("Favour Tumba")
    c.setSubject("Resume \u2014 Software Engineer (AI, Backend & Full-Stack)")
    c.setCreator("build_resume.py (reportlab)")
    c.setKeywords(
        "Favour Tumba, Software Engineer, Python, TypeScript, FastAPI, React, Next.js, "
        "PostgreSQL, pgvector, RAG, LLM, Claude API, Docker, Machine Learning, Backend, Full-Stack"
    )
    y = build_page(c, scale)
    return c, y


def main(outputs) -> None:
    register_fonts()

    # auto-fit: shrink the vertical rhythm until the content clears the bottom margin
    scale = 1.04
    while True:
        buf = io.BytesIO()
        c, y = render(scale, buf)
        if y >= MARGIN_BOTTOM:
            break
        scale -= 0.01
        if scale < 0.90:
            raise SystemExit("Content does not fit on one page even at minimum scale.")

    c.showPage()
    c.save()
    data = buf.getvalue()

    # tag the document language - screen readers and some ATS parsers look for it
    try:
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import NameObject, TextStringObject

        reader = PdfReader(io.BytesIO(data))
        writer = PdfWriter(clone_from=reader)
        writer._root_object[NameObject("/Lang")] = TextStringObject("en-US")
        out = io.BytesIO()
        writer.write(out)
        data = out.getvalue()
    except Exception as exc:  # cosmetic only - never block the build
        print("note: skipped /Lang tagging (" + str(exc) + ")")

    for path in outputs:
        parent = os.path.dirname(os.path.abspath(path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(data)
        print("wrote %s  (%.1f KB, scale %.2f, bottom y %.1f)" % (path, len(data) / 1024, scale, y))


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        here = os.path.dirname(os.path.abspath(__file__))
        args = [os.path.join(os.path.dirname(here), "Favour_Tumba_Resume.pdf")]
    main(args)
