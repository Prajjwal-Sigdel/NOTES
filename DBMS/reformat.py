#!/usr/bin/env python3
"""
Reformat aianswers.txt for iPhone 13 Notes app.
Target: ~40 monospaced characters per line in portrait mode.

Strategy:
  - Prose paragraphs → re-wrap to W chars
  - Data tables (borders contain ┬) → labelled list format
  - Diagrams (box art without ┬) → strip box chars, extract text
  - Code/SQL/RA → keep as-is with 2-space indent (may exceed W, ok)
  - Notation guide → one symbol per line
  - Dividers → shorten to W
  - SET headers → shorten to W
  - List items → re-wrap with hanging indent
  - Q. lines → collect and re-wrap
"""

import textwrap, re, sys

W = 40  # target width
SRC = "aianswers.txt"
DST = "aianswers_mobile.txt"

BOX = set("┌┐└┘├┤┬┴┼─│╔╗╚╝╠╣╦╩╬═║▼▲◄►")
ARROWS = set("←→↑↓────────►◄◀▶▸")

# ── helpers ──────────────────────────────────────────────────────

def has_box(line, threshold=1):
    """True if line has box-drawing characters."""
    return sum(1 for c in line if c in BOX) >= threshold

def is_box_line(line):
    """True if this line is part of a diagram or table (has any box char)."""
    return has_box(line, 1)

def is_table_border(line):
    """A table (not just diagram) has ┬ or ┴ or ┼ in its top/bottom border."""
    return bool(re.search(r'[┬┴┼]', line))

def is_full_divider(line):
    """═══… or ───… lines spanning most of the line."""
    s = line.strip()
    return (len(s) >= 20 and
            all(c in '═─ ' for c in s) and
            sum(1 for c in s if c in '═─') > len(s) * 0.7)

def is_set_header(line):
    """SET N ────…"""
    return bool(re.match(r'^SET\s+\d+\s*─', line.strip()))

def is_question_start(line):
    """Q. N (x) …"""
    return bool(re.match(r'^Q\.\s*\d+', line.strip()))

def looks_like_code(line):
    """Heuristic: SQL or RA code lines."""
    s = line.strip()
    kws = ('SELECT ', 'INSERT ', 'UPDATE ', 'DELETE ', 'CREATE ',
           'ALTER ', 'DROP ', 'GRANT ', 'REVOKE ', 'BEGIN ',
           'COMMIT', 'ROLLBACK', 'SET TRANSACTION',
           'σ', 'π', '⋈', 'ρ', '𝒢', 'GROUP BY', 'ORDER BY',
           'HAVING ', 'WHERE ', 'FROM ', 'JOIN ', 'ON ', 'INTO ',
           'VALUES', 'PRIMARY KEY', 'FOREIGN KEY', 'REFERENCES',
           'NOT NULL', 'CHECK (', 'UNIQUE',
           'CREATE TABLE', 'CREATE VIEW', 'CREATE INDEX',
           'EXPLAIN', 'WITH ')
    return any(s.upper().startswith(k.upper()) or
               s.startswith(k) for k in kws)

def wrap_text(text, width=W, indent=''):
    """Wrap a paragraph to width with optional indent on continuation."""
    lines = textwrap.wrap(text, width=width,
                          initial_indent='',
                          subsequent_indent=indent,
                          break_long_words=False,
                          break_on_hyphens=False)
    return lines if lines else ['']

def strip_box_chars(text):
    """Replace all box-drawing characters with spaces."""
    return ''.join(' ' if c in BOX else c for c in text)


# ── table parser ─────────────────────────────────────────────────

def find_columns(border_line):
    """Find column split positions from a border line with ┬ or ┼."""
    cols = []
    for i, c in enumerate(border_line):
        if c in '┬┼┤┴':
            cols.append(i)
    return cols

def parse_table(lines):
    """
    Parse a box-drawn table into rows of cells.
    Returns list of rows; each row is list of cell strings.
    """
    # Find the first border with ┬ to get column positions
    splits = []
    for line in lines:
        if '┬' in line or '┼' in line:
            splits = find_columns(line)
            # also need left edge
            left = line.find('│')
            if left < 0:
                left = line.find('┌')
            break

    if not splits:
        return None

    # boundaries: left edge, each split, right edge
    bounds = [left] + splits
    ncols = len(bounds)

    rows = []
    current_row = None

    for line in lines:
        s = line.rstrip()
        # skip border lines (contain ┌┐├┤└┘┬┴┼─)
        stripped = s.strip()
        if all(c in BOX | {' '} for c in stripped) and len(stripped) > 2:
            if current_row is not None:
                rows.append(current_row)
                current_row = None
            continue

        # data line (contains │)
        if '│' in s:
            # extract cell contents between boundaries
            cells = []
            for ci in range(ncols):
                start = bounds[ci] + 1  # skip the │
                end = bounds[ci + 1] if ci + 1 < ncols else len(s)
                cell = s[start:end].strip().strip('│').strip()
                cells.append(cell)

            # if first cell is empty, it's a continuation of previous row
            if current_row is not None and cells[0] == '' and any(c for c in cells):
                for ci in range(ncols):
                    if cells[ci]:
                        current_row[ci] += ' ' + cells[ci]
            else:
                if current_row is not None:
                    rows.append(current_row)
                current_row = cells[:]
        else:
            if current_row is not None:
                rows.append(current_row)
                current_row = None

    if current_row is not None:
        rows.append(current_row)

    return rows

def table_to_text(rows):
    """Convert parsed table rows to mobile-friendly text."""
    if not rows or len(rows) < 2:
        return []

    out = []
    headers = rows[0]
    ncols = len(headers)

    for ri, row in enumerate(rows[1:], 1):
        # pad row to ncols
        while len(row) < ncols:
            row.append('')

        if ncols == 2:
            label = row[0]
            val = row[1]
            wrapped = wrap_text(f"▸ {label}: {val}", W)
            out.extend(wrapped)
        elif ncols >= 3:
            # first cell is the label
            label = row[0]
            out.append(f"▸ {label}:")
            for ci in range(1, ncols):
                hdr = headers[ci] if ci < len(headers) else f"Col{ci}"
                val = row[ci]
                prefix = f"  {hdr}: "
                rest_indent = '  ' + ' ' * len(f"{hdr}: ")
                wrapped = wrap_text(f"{prefix}{val}", W, rest_indent)
                out.extend(wrapped)
        out.append('')

    return out


# ── diagram handler ──────────────────────────────────────────────

def diagram_to_text(lines):
    """
    Convert an ASCII diagram block to mobile-friendly text.
    Strategy: strip box chars, extract meaningful text segments,
    output as hierarchical list.
    """
    out = []
    seen = set()  # avoid duplicate text

    for line in lines:
        # strip box-drawing characters → spaces
        clean = strip_box_chars(line)
        # also strip arrow characters
        clean = clean.replace('▼', ' ').replace('▲', ' ')
        clean = clean.replace('◄', ' ').replace('►', ' ')
        clean = clean.replace('←', ' ').replace('→', ' ')
        clean = clean.replace('↑', ' ').replace('↓', ' ')

        # find text segments (runs of non-space chars)
        segments = re.findall(r'\S(?:.*?\S)?', clean)
        # merge very short fragments that are close together
        # (like "a" "b" should become "a b")

        if not segments:
            continue

        # join all text on this line
        text = ' '.join(segments)
        # collapse multiple spaces
        text = re.sub(r'\s{2,}', '  ', text).strip()

        if not text or len(text) < 2:
            continue

        # skip lines that are just arrows or connectors
        if all(c in '─│┌┐└┘├┤┬┴┼ ▼▲◄►←→↑↓|/\\' for c in text):
            continue

        # skip duplicate lines (diagrams often repeat labels)
        key = text.lower().strip()
        if key in seen:
            continue
        seen.add(key)

        # determine indent level based on leading spaces in original
        leading = len(line) - len(line.lstrip())
        if leading < 4:
            indent = ''
        elif leading < 10:
            indent = '  '
        else:
            indent = '    '

        # Check if it's a major header (ALL CAPS, like "QUERY PROCESSOR")
        words = text.split()
        is_header = (len(words) >= 1 and
                     all(w.isupper() or w in '():/,.-—' or
                         not w.isalpha() for w in words) and
                     any(w.isalpha() and w.isupper() for w in words))

        if is_header:
            wrapped = wrap_text(f"▶ {text}", W, '  ')
        else:
            wrapped = wrap_text(f"{indent}• {text}", W,
                                indent + '  ')

        out.extend(wrapped)

    return out


# ── notation guide handler ───────────────────────────────────────

def reformat_notation(lines):
    """
    Reformat the two-column notation guide into single-column.
    Lines like: σ  — Select (sigma)          π  — Project (pi)
    """
    out = []
    for line in lines:
        s = line.strip()
        if not s:
            out.append('')
            continue

        # Try to split two entries on one line
        # Pattern: "sym — desc     sym — desc"
        # Find all "sym — desc" patterns
        entries = re.findall(r'(\S+)\s+—\s+(.+?)(?=\s{3,}\S+\s+—|$)', s)
        if entries:
            for sym, desc in entries:
                desc = desc.strip()
                out.append(f"  {sym}  — {desc}")
        else:
            # keep as-is, wrapped
            wrapped = wrap_text(s, W, '    ')
            out.extend(wrapped)

    return out


# ── main processing ──────────────────────────────────────────────

def process():
    with open(SRC, 'r', encoding='utf-8') as f:
        raw = f.readlines()

    lines = [l.rstrip('\n') for l in raw]
    n = len(lines)
    out = []
    i = 0

    # track if we're in the notation section
    in_notation = False
    notation_buf = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # ── notation section ──
        if stripped == 'NOTE ON NOTATION':
            out.append('NOTE ON NOTATION')
            out.append('─' * W)
            i += 1
            # skip the ─── underline
            if i < n and is_full_divider(lines[i]):
                i += 1
            # collect notation lines until blank line followed by ═══
            notation_buf = []
            while i < n:
                if is_full_divider(lines[i]) and '═' in lines[i]:
                    break
                notation_buf.append(lines[i])
                i += 1
            # process notation
            formatted = reformat_notation(notation_buf)
            out.extend(formatted)
            out.append('')
            continue

        # ── full dividers ════ or ────  ──
        if is_full_divider(stripped):
            if '═' in stripped:
                out.append('═' * W)
            else:
                out.append('─' * W)
            i += 1
            continue

        # ── SET headers ──
        if is_set_header(stripped):
            m = re.match(r'(SET\s+\d+)\s*─+', stripped)
            if m:
                out.append(f"{m.group(1)} {'─' * (W - len(m.group(1)) - 1)}")
            else:
                out.append(stripped[:W])
            i += 1
            continue

        # ── centered title lines (all caps, centered) ──
        if (stripped.isupper() or
            re.match(r'^[A-Z\s\(\)—×\d]+$', stripped)) and \
           len(line) - len(line.lstrip()) > 10 and \
           len(stripped) > 5 and not is_question_start(stripped):
            # center within W
            wrapped = wrap_text(stripped, W)
            for wl in wrapped:
                out.append(wl.center(W).rstrip())
            i += 1
            continue

        # ── table or diagram block ──
        if is_box_line(line):
            # collect all consecutive box-containing lines
            # (and lines in between that are part of the same block)
            block_start = i
            block = []
            while i < n:
                cl = lines[i]
                if is_box_line(cl):
                    block.append(cl)
                    i += 1
                elif cl.strip() == '':
                    # blank line — might separate sections of diagram
                    # peek ahead: if next non-blank has box chars, include
                    j = i + 1
                    while j < n and lines[j].strip() == '':
                        j += 1
                    if j < n and is_box_line(lines[j]):
                        block.append(cl)
                        i += 1
                    else:
                        break
                elif ('│' in cl or '▼' in cl or '▲' in cl or
                      '←' in cl or '→' in cl or
                      cl.strip().startswith('│') or
                      cl.strip().endswith('│')):
                    # connector line between box sections
                    block.append(cl)
                    i += 1
                else:
                    # text line between box lines — check if box lines follow
                    j = i + 1
                    while j < n and not is_box_line(lines[j]) and lines[j].strip():
                        j += 1
                    if j < n and is_box_line(lines[j]):
                        # text is sandwiched between box lines → include
                        for k in range(i, j):
                            block.append(lines[k])
                        i = j
                    else:
                        break

            if not block:
                continue

            # determine if this is a DATA TABLE or a DIAGRAM
            # A data table's FIRST border line has ┬ (column separators)
            # Diagrams may have ┬ inside (tree connectors) but NOT on
            # the very first border line
            first_border = ''
            for bl in block:
                bs = bl.strip()
                if bs and all(c in BOX | {' '} for c in bs) and len(bs) > 5:
                    first_border = bs
                    break
            is_table = '┬' in first_border

            if is_table:
                rows = parse_table(block)
                if rows:
                    out.append('')
                    out.extend(table_to_text(rows))
                else:
                    # fallback: strip box chars
                    out.append('')
                    out.extend(diagram_to_text(block))
                    out.append('')
            else:
                out.append('')
                out.append('· · · · · · · · · ·')
                out.extend(diagram_to_text(block))
                out.append('· · · · · · · · · ·')
                out.append('')

            continue

        # ── question lines ──
        if is_question_start(stripped):
            # collect the full question (may span multiple lines)
            q_text = stripped
            i += 1
            while i < n:
                nxt = lines[i]
                ns = nxt.strip()
                # continuation: indented text that's not a divider/header/blank
                if (ns and
                    not is_full_divider(ns) and
                    not is_set_header(ns) and
                    not ns.startswith('ANSWER') and
                    (len(nxt) - len(nxt.lstrip()) >= 5 or
                     ns[0].islower())):
                    q_text += ' ' + ns
                    i += 1
                else:
                    break
            wrapped = wrap_text(q_text, W, '   ')
            out.extend(wrapped)
            continue

        # ── blank lines ──
        if not stripped:
            out.append('')
            i += 1
            continue

        # ── code / SQL / RA lines ──
        # detect code blocks: lines starting with significant indent
        # that look like code
        indent_len = len(line) - len(line.lstrip())
        if indent_len >= 2 and looks_like_code(stripped):
            # collect code block
            code_block = []
            while i < n:
                cl = lines[i]
                cs = cl.strip()
                cind = len(cl) - len(cl.lstrip())
                if cs == '' and code_block:
                    # blank line — check if code continues after
                    j = i + 1
                    if j < n and len(lines[j]) - len(lines[j].lstrip()) >= 2 and looks_like_code(lines[j].strip()):
                        code_block.append('')
                        i += 1
                    else:
                        break
                elif cind >= 2 and cs and not is_full_divider(cs) and not is_set_header(cs):
                    code_block.append('  ' + cs)
                    i += 1
                else:
                    break
            out.extend(code_block)
            continue

        # ── list items (•, -, digit.) ──
        list_match = re.match(r'^(\s*)(•|\-|\d+[\.\)])\s+(.*)', line)
        if list_match:
            indent_str = '  '
            bullet = list_match.group(2)
            text = list_match.group(3)

            # collect continuation lines
            i += 1
            while i < n:
                nxt = lines[i]
                ns = nxt.strip()
                nind = len(nxt) - len(nxt.lstrip())
                if (ns and
                    nind >= 4 and
                    not re.match(r'^(•|\-|\d+[\.\)])\s', ns) and
                    not is_full_divider(ns) and
                    not is_set_header(ns) and
                    not is_question_start(ns) and
                    not is_box_line(nxt)):
                    text += ' ' + ns
                    i += 1
                else:
                    break

            prefix = f"{indent_str}{bullet} "
            hang = ' ' * len(prefix)
            wrapped = wrap_text(f"{prefix}{text}", W, hang)
            out.extend(wrapped)
            continue

        # ── headers (ANSWER:, ALL CAPS short lines) ──
        if stripped == 'ANSWER:' or (
            stripped.endswith(':') and stripped[:-1].isupper() and
            len(stripped) < 50):
            out.append(stripped)
            i += 1
            continue

        # ── prose paragraphs ──
        # collect consecutive non-empty, non-special lines
        para = stripped
        i += 1
        while i < n:
            nxt = lines[i]
            ns = nxt.strip()
            if (ns and
                not is_full_divider(ns) and
                not is_set_header(ns) and
                not is_question_start(ns) and
                not is_box_line(nxt) and
                not re.match(r'^(•|\-|\d+[\.\)])\s', ns) and
                not ns == 'ANSWER:' and
                not (ns.endswith(':') and ns[:-1].isupper() and len(ns) < 50) and
                not looks_like_code(ns)):
                para += ' ' + ns
                i += 1
            else:
                break

        wrapped = wrap_text(para, W)
        out.extend(wrapped)
        continue

    # ── post-process: limit consecutive blank lines to 2 ──
    final = []
    blank_count = 0
    for line in out:
        if line.strip() == '':
            blank_count += 1
            if blank_count <= 2:
                final.append('')
        else:
            blank_count = 0
            final.append(line)

    # write output
    with open(DST, 'w', encoding='utf-8') as f:
        for line in final:
            f.write(line + '\n')

    # stats
    total = len(final)
    over_w = sum(1 for l in final if len(l) > W)
    over_55 = sum(1 for l in final if len(l) > 55)
    max_len = max(len(l) for l in final) if final else 0
    leaked_box = sum(1 for l in final if any(c in BOX for c in l))

    print(f"Lines: {total}")
    print(f"Max width: {max_len}")
    print(f"Lines > {W} chars: {over_w}")
    print(f"Lines > 55 chars: {over_55}")
    print(f"Leaked box chars: {leaked_box}")

if __name__ == '__main__':
    process()
