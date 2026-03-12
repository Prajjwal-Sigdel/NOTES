#!/usr/bin/env python3
"""
Reformat aianswers.txt for a 46-character-wide display.

Handles:
  - Prose paragraphs → word-wrap to 46 chars
  - Box-drawn tables → compact box table if it fits, else labeled list
  - Single-cell boxes → extract text and wrap
  - Architecture diagrams → strip indent or convert to labeled text
  - SQL code blocks → keep with 2-space indent, smart wrap if >46
  - Relational algebra → same treatment as code
  - Query trees (| / \\ based) -> preserve structure, strip indent
  - Dividers → shorten to 46
  - SET headers → shorten to 46
  - List items → wrap with hanging indent
  - Notation guide → one symbol per line
"""

import textwrap, re, copy

W = 46
SRC = "aianswers.txt"
DST = "aianswers_mobile.txt"

BOX = set("┌┐└┘├┤┬┴┼─│╔╗╚╝╠╣╦╩╬═║")

# ════════════════════════════════════════
# DETECTION HELPERS
# ════════════════════════════════════════

def has_border(line):
    """Has structural box-drawing chars (not just │)."""
    return any(c in line for c in '┌┐└┘├┤┬┴┼─╔╗╚╝╠╣╦╩╬═║')

def has_any_box(line):
    """Has any box-drawing character including │."""
    return any(c in BOX for c in line)

def is_divider(s):
    s = s.strip()
    return (len(s) >= 15 and
            all(c in '═─= ' for c in s) and
            sum(1 for c in s if c in '═─=') > len(s) * 0.7)

def is_set_header(s):
    return bool(re.match(r'^SET\s+\d+\s*─', s.strip()))

def is_q_start(s):
    return bool(re.match(r'^Q\.\s*\d+', s.strip()))

SQL_KWS = [
    'SELECT ', 'INSERT ', 'UPDATE ', 'DELETE ',
    'CREATE ', 'ALTER ', 'DROP ', 'GRANT ', 'REVOKE ',
    'TRUNCATE ', 'COMMIT', 'ROLLBACK', 'EXPLAIN ',
    'SET TRANSACTION',
    'CREATE TABLE', 'CREATE VIEW', 'CREATE INDEX',
    'CREATE OR REPLACE', 'CREATE TYPE',
    'WITH GRANT', 'LANGUAGE ', 'AS $$',
    'PRIMARY KEY', 'FOREIGN KEY',
]

def is_code(s):
    """Heuristic: is this line SQL, RA, or schema code?"""
    s = s.strip()
    if not s:
        return False
    su = s.upper()
    for k in SQL_KWS:
        if su.startswith(k):
            return True
    if s.startswith('--'):
        return True
    if any(s.startswith(p) for p in ['σ_', 'π_', 'ρ_', '⋈', '𝒢']):
        return True
    if re.match(r'^[a-z_]\w*\s*←', s):
        return True
    return False

def is_code_cont(s, indent):
    """Is this an indented continuation of a code block?"""
    s = s.strip()
    if not s:
        return False
    if indent < 2:
        return False
    # Continuation patterns
    if s[0] in ');,(':
        return True
    cont_kws = ['AND ', 'OR ', 'ON ', 'FROM ', 'WHERE ', 'JOIN ',
                'LEFT JOIN', 'RIGHT JOIN', 'SET ', 'INTO ',
                'VALUES', 'HAVING ', 'GROUP BY', 'ORDER BY',
                'LIMIT ', 'REFERENCES', 'NOT NULL', 'CHECK ',
                'UNIQUE', 'DEFAULT', 'IN ', 'OUT ', 'AS ',
                'PRIMARY KEY', 'FOREIGN KEY', 'BETWEEN',
                'LIKE ', 'IS NULL', 'IS NOT NULL']
    su = s.upper()
    for k in cont_kws:
        if su.startswith(k):
            return True
    # Also continuation if line starts lowercase or with special chars
    if s[0] in "'\"" or s.startswith('$$'):
        return True
    return False

def is_section_header(s):
    """ALL-CAPS section header like 'ANSWER:', 'KEY DDL COMMANDS:'"""
    s = s.strip()
    if not s:
        return False
    if s == 'ANSWER:':
        return True
    # Check for numbered section headers like "1. DATA DEFINITION LANGUAGE (DDL)"
    m = re.match(r'^\d+\.\s+[A-Z]', s)
    if m and all(c.isupper() or c in ' _-()/:0123456789.' for c in s):
        return True
    # Plain ALL-CAPS header with colon
    if (s.endswith(':') and len(s) < 55 and
        any(c.isalpha() for c in s) and
        all(c.isupper() or c in ' _-()/:,0123456789.⁺' for c in s[:-1])):
        return True
    return False


# ════════════════════════════════════════
# WRAPPING HELPERS
# ════════════════════════════════════════

def wrap(text, width=W, indent=''):
    r = textwrap.wrap(text, width=width,
                      initial_indent='',
                      subsequent_indent=indent,
                      break_long_words=False,
                      break_on_hyphens=False)
    return r if r else ['']

def wrap_code_line(code, width=W):
    """Format a code line with 2-space indent, smart-wrap if too long."""
    s = code.strip()
    line = '  ' + s

    if len(line) <= width:
        return [line]

    # If 1-space indent fits, use that
    if len(' ' + s) <= width:
        return [' ' + s]

    # If raw expression fits exactly, use no indent
    if len(s) <= width:
        return [s]

    # Don't wrap tree-structure lines
    if set(s) <= set('│/\\ ─'):
        return [line[:width]]

    # For timeline/diagram lines with ─ and |, truncate
    if re.match(r'^[\s─|←→↑↓]*$', s):
        return [line[:width]]

    # Try wrapping at logical break points
    cont = '  '

    # Simple word-wrap with continuation indent
    words = s.split()
    lines = []
    current = '  '
    for word in words:
        if current.strip() == '':
            current += word
        elif len(current) + 1 + len(word) <= width:
            current += ' ' + word
        else:
            lines.append(current)
            current = cont + word
    if current.strip():
        lines.append(current)

    return lines if lines else [line[:width]]


# ════════════════════════════════════════
# TABLE PARSING AND RENDERING
# ════════════════════════════════════════

def find_col_pos(border):
    return [i for i, c in enumerate(border) if c in '┬┼┴']

def parse_table(block):
    """Parse box-drawn table into list of rows (each row = list of cell strings)."""
    splits = []
    left = 0
    for line in block:
        if '┬' in line or '┼' in line:
            splits = find_col_pos(line)
            for i, c in enumerate(line):
                if c in '│┌├└':
                    left = i
                    break
            break
    if not splits:
        return None

    bounds = [left] + splits
    ncols = len(bounds)
    rows = []
    cur = None

    for line in block:
        s = line.rstrip()
        stripped = s.strip()
        if stripped and all(c in BOX | {' '} for c in stripped):
            if cur is not None:
                rows.append(cur)
                cur = None
            continue
        if '│' in s:
            cells = []
            for ci in range(ncols):
                start = bounds[ci] + 1
                end = bounds[ci + 1] if ci + 1 < ncols else len(s)
                cell = s[start:end].strip().strip('│').strip() if start < len(s) else ''
                cells.append(cell)
            if cur is not None and cells[0] == '' and any(c for c in cells):
                for ci in range(ncols):
                    if cells[ci]:
                        cur[ci] = (cur[ci] + ' ' + cells[ci]).strip()
            else:
                if cur is not None:
                    rows.append(cur)
                cur = cells[:]
        else:
            if cur is not None:
                rows.append(cur)
                cur = None
    if cur is not None:
        rows.append(cur)
    return rows

def max_word_len(text):
    """Return the length of the longest word in text."""
    words = text.split()
    return max((len(w) for w in words), default=0)

def try_box_table(rows_orig, max_w=W):
    """Try to render a proper box table with cell wrapping.
    Never breaks words. Returns lines or None."""
    rows = copy.deepcopy(rows_orig)
    if not rows or len(rows) < 2:
        return None
    ncols = max(len(r) for r in rows)
    for r in rows:
        while len(r) < ncols:
            r.append('')

    # overhead: (ncols+1) border chars + 2*ncols padding spaces
    overhead = (ncols + 1) + (2 * ncols)
    avail = max_w - overhead
    if avail < ncols * 3:
        return None

    # Max content width (single line) per column
    max_lens = [0] * ncols
    # Minimum column width = longest single word in that column
    min_word_lens = [0] * ncols
    for r in rows:
        for ci in range(ncols):
            max_lens[ci] = max(max_lens[ci], len(r[ci]))
            min_word_lens[ci] = max(min_word_lens[ci], max_word_len(r[ci]))

    # Minimum col width must fit longest word (no word breaking)
    min_ws = [max(3, min_word_lens[ci]) for ci in range(ncols)]
    if sum(min_ws) > avail:
        return None  # Can't fit without breaking words

    if sum(max_lens) <= avail:
        # Fits without wrapping — use natural widths
        cw = max_lens[:]
    else:
        # Start from min_ws, distribute remaining space proportionally
        cw = min_ws[:]
        remaining = avail - sum(cw)
        # Give extra space to columns that need it most
        need = [max(0, max_lens[ci] - cw[ci]) for ci in range(ncols)]
        total_need = sum(need) or 1
        for ci in range(ncols):
            extra = round(remaining * need[ci] / total_need)
            cw[ci] += extra
        # Adjust to exactly fill available
        while sum(cw) > avail:
            # Shrink the widest column (that's above its minimum)
            idx = max(range(ncols), key=lambda i: cw[i] - min_ws[i])
            if cw[idx] <= min_ws[idx]:
                return None
            cw[idx] -= 1
        while sum(cw) < avail:
            idx = max(range(ncols), key=lambda i: max_lens[i] - cw[i])
            cw[idx] += 1

    if any(w < 3 for w in cw):
        return None

    def hline(l, m, r, f='─'):
        return l + m.join(f * (w + 2) for w in cw) + r

    def data_lines(cells):
        wr = []
        for ci in range(ncols):
            txt = cells[ci] if ci < len(cells) else ''
            wl = textwrap.wrap(txt, cw[ci],
                               break_long_words=False,
                               break_on_hyphens=False) or ['']
            wr.append(wl)
        mh = max(len(w) for w in wr)
        out = []
        for li in range(mh):
            parts = []
            for ci in range(ncols):
                t = wr[ci][li] if li < len(wr[ci]) else ''
                parts.append(f' {t:<{cw[ci]}} ')
            out.append('│' + '│'.join(parts) + '│')
        return out

    result = [hline('┌', '┬', '┐')]
    result.extend(data_lines(rows[0]))
    result.append(hline('├', '┼', '┤'))
    for ri in range(1, len(rows)):
        result.extend(data_lines(rows[ri]))
    result.append(hline('└', '┴', '┘'))

    # Final check: all lines must be <= max_w
    if any(len(l) > max_w for l in result):
        return None
    return result

def labeled_table(rows_orig, max_w=W):
    """Render table as labeled entries (fallback for wide tables)."""
    rows = copy.deepcopy(rows_orig)
    if not rows or len(rows) < 2:
        return []
    hdrs = rows[0]
    nc = len(hdrs)
    out = []

    for ri in range(1, len(rows)):
        row = rows[ri]
        while len(row) < nc:
            row.append('')

        if nc == 2:
            label, value = row[0], row[1]
            t = f"▸ {label}: {value}" if value else f"▸ {label}"
            out.extend(wrap(t, max_w, '    '))
        elif nc >= 3:
            out.append(f"▸ {row[0]}:")
            for ci in range(1, nc):
                h = hdrs[ci] if ci < len(hdrs) else ''
                v = row[ci]
                if v:
                    pref = f"  {h}: "
                    hlen = min(len(pref), 18)
                    hang = ' ' * hlen
                    out.extend(wrap(pref + v, max_w, hang))
        out.append('')
    return out

def format_table_block(block):
    """Format a table block — try box table, fall back to labeled."""
    rows = parse_table(block)
    if not rows:
        return None
    box = try_box_table(rows)
    if box:
        return box
    return labeled_table(rows)


# ════════════════════════════════════════
# SINGLE-CELL BOX & DIAGRAM HANDLING
# ════════════════════════════════════════

def extract_box_text(block):
    """Extract text lines from a single-cell box (no column separators)."""
    parts = []
    for line in block:
        s = line.strip()
        if all(c in BOX | {' '} for c in s):
            continue
        clean = s.strip('│').strip('║').strip()
        if clean:
            parts.append(clean)
    return parts

def is_real_timeline(lines):
    """Detect actual schedule timelines (T1/T2 schedules, transaction timelines).
    Not architecture diagrams that happen to have ── and → chars."""
    text = ' '.join(lines)
    # True timelines have transaction labels like T1:, T2:, or
    # operations like read(, write(, lock(, commit, abort
    timeline_markers = ['T1:', 'T2:', 'T3:', 'read(', 'write(', 'lock(',
                        'unlock(', 'commit', 'abort', 'checkpoint',
                        'Time →', 'Time→', 'time →']
    marker_count = sum(1 for m in timeline_markers if m.lower() in text.lower())
    return marker_count >= 1

def format_er_relationship(block):
    """Detect and format ER relationship diagrams (3 boxes in a row like:
    ┌──────────┐  1     ┌──────────┐  1     ┌──────────┐
    │ Employee │────────│  heads   │────────│Department│
    └──────────┘        └──────────┘        └──────────┘
    Convert to compact text representation."""
    # Collect all text content from box lines
    texts = []
    card_labels = []  # cardinality labels between boxes
    for line in block:
        s = line.strip()
        # Find text inside │...│ segments
        segs = re.findall(r'│\s*([^│]+?)\s*│', s)
        for seg in segs:
            seg = seg.strip()
            if seg and not all(c in BOX | {' ', '─'} for c in seg):
                texts.append(seg)
        # Find cardinality labels (like "1", "N", "M") between boxes
        # These appear as isolated chars/numbers between ┘ and ┌ or between boxes
        cards = re.findall(r'[┘└]\s+([1NM])\s+', s)
        card_labels.extend(cards)
        # Also check for "1" "N" "M" in the top line between ┐ and ┌
        cards2 = re.findall(r'┐\s+([1NM])\s+', s)
        card_labels.extend(cards2)

    if len(texts) < 3:
        return None  # Not a 3-box ER diagram

    # Deduplicate while preserving order
    seen = set()
    unique_texts = []
    for t in texts:
        tl = t.lower()
        if tl not in seen:
            seen.add(tl)
            unique_texts.append(t)

    if len(unique_texts) == 3:
        entity1, rel, entity2 = unique_texts
        # Build compact representation
        if len(card_labels) >= 2:
            c1, c2 = card_labels[0], card_labels[1]
            line = f"[{entity1}] ─({c1})── {rel} ──({c2})─ [{entity2}]"
        else:
            line = f"[{entity1}] ─── {rel} ─── [{entity2}]"

        if len(line) <= W:
            return ['', '  ' + line, '']
        # If still too wide, try wrapping
        return ['', f'  [{entity1}]', f'    ─── {rel} ───',
                f'  [{entity2}]', '']

    return None

def format_side_by_side_boxes(block):
    """Handle wide diagrams with multiple boxes side by side.
    Split into individual box regions and render them stacked."""
    # Find the first line that has ┌ to determine box positions
    first_border = ''
    for bl in block:
        if '┌' in bl:
            first_border = bl
            break

    # Find top-level box starts on the first border line
    # For nested boxes (┌...┌...┐...┐), only count top-level ┌'s
    box_starts = [m.start() for m in re.finditer('┌', first_border)]
    if len(box_starts) < 2:
        return None

    # Match each ┌ with its corresponding ┐ on the same line
    # to find the true column extents
    box_extents = []  # (start, end) for each top-level box
    for bl in block:
        if '└' in bl:
            # Use the └ line to find box boundaries (more reliable)
            starts = [m.start() for m in re.finditer('└', bl)]
            ends = [m.start() for m in re.finditer('┘', bl)]
            if len(starts) >= 2 and len(ends) >= 2:
                # We have at least 2 boxes
                box_extents = list(zip(starts, ends))
                break

    if not box_extents:
        # Fall back to using ┌ and ┐ from first border line
        starts = [m.start() for m in re.finditer('┌', first_border)]
        ends = [m.start() for m in re.finditer('┐', first_border)]
        if len(starts) >= 2 and len(ends) >= 2:
            # Match them: for side-by-side, each ┐ closes the nearest ┌
            # Simple heuristic: pair them left to right
            # But nested boxes make this tricky — use └/┘ instead
            # For now, use first and last pairs
            box_extents = list(zip(starts, ends))

    if len(box_extents) < 2:
        return None

    # Filter to get only the top-level (outermost) boxes
    # Remove boxes that are nested inside others
    top_level = []
    for s, e in box_extents:
        nested = False
        for s2, e2 in box_extents:
            if s2 < s and e < e2:  # This box is inside another
                nested = True
                break
        if not nested:
            top_level.append((s, e))
    box_extents = top_level

    if len(box_extents) < 2:
        return None

    max_line_len = max(len(l) for l in block)

    # Extract content from each box region
    box_data = []
    for (col_start, col_end) in box_extents:
        texts = []
        for line in block:
            if col_start >= len(line):
                continue
            seg = line[col_start:min(col_end + 1, len(line))].rstrip()
            # Remove outer box characters
            clean = seg
            for c in '┌┐└┘├┤─':
                clean = clean.replace(c, ' ')
            # Keep inner box chars (│) as separators to extract sub-sections
            # But remove outer │ (first and last)
            clean = clean.strip()
            if clean.startswith('│'):
                clean = clean[1:]
            if clean.endswith('│'):
                clean = clean[:-1]
            # Now split by │ for inner boxes
            parts = clean.split('│')
            for part in parts:
                part = part.strip()
                if part and not all(c in ' ─→←↑↓▼▲' for c in part):
                    texts.append(part)

        # Deduplicate
        seen = set()
        unique = []
        for t in texts:
            key = t.lower().strip()
            if key not in seen and key:
                seen.add(key)
                unique.append(t)
        box_data.append(unique)

    # Extract inter-box connector text
    inter_text = []
    for bi in range(len(box_extents) - 1):
        gap_start = box_extents[bi][1] + 1
        gap_end = box_extents[bi + 1][0]
        gap_texts = []
        for line in block:
            if gap_start >= len(line):
                continue
            seg = line[gap_start:min(gap_end, len(line))].strip()
            clean = seg
            for c in BOX | {'─', '→', '←', '↑', '↓', '▼', '▲', '|'}:
                clean = clean.replace(c, ' ')
            clean = ' '.join(clean.split()).strip()
            if clean and len(clean) >= 2:
                gap_texts.append(clean)
        # Deduplicate
        seen = set()
        unique_gap = []
        for t in gap_texts:
            if t.lower() not in seen:
                seen.add(t.lower())
                unique_gap.append(t)
        inter_text.append(unique_gap)

    # Build output: stack boxes vertically with connectors
    out = []
    for bi, texts in enumerate(box_data):
        if not texts:
            continue

        # Try to render as a box
        max_text_w = max((len(t) for t in texts), default=0)
        box_inner = min(max_text_w, W - 4)
        if box_inner >= 3 and box_inner + 4 <= W:
            bw = box_inner + 2
            out.append('┌' + '─' * bw + '┐')
            for t in texts:
                if len(t) <= box_inner:
                    out.append(f'│ {t:<{box_inner}} │')
                else:
                    wrapped = textwrap.wrap(t, box_inner,
                                          break_long_words=False,
                                          break_on_hyphens=False)
                    for wl in wrapped:
                        out.append(f'│ {wl:<{box_inner}} │')
            out.append('└' + '─' * bw + '┘')
        else:
            for t in texts:
                out.extend(wrap('  ' + t, W, '    '))

        if bi < len(box_data) - 1:
            # Add inter-box connector text
            if bi < len(inter_text) and inter_text[bi]:
                for ct in inter_text[bi]:
                    out.extend(wrap(f'    {ct}', W, '      '))
            out.append('         ↕')

    return out if out else None

def format_diagram(block):
    """Try to fit diagram by stripping leading whitespace.
    Also tries progressively removing indent."""
    min_ind = 999
    for line in block:
        if line.strip():
            min_ind = min(min_ind, len(line) - len(line.lstrip()))
    if min_ind >= 999:
        min_ind = 0

    stripped = [line[min_ind:].rstrip() for line in block]
    mw = max((len(l) for l in stripped), default=0)

    if mw <= W:
        return stripped

    # Check if this is a real timeline diagram (T1/T2 schedules)
    if is_real_timeline(stripped):
        result = compress_timeline(stripped)
        if result is not None:
            mw2 = max((len(l) for l in result), default=0)
            if mw2 <= W:
                return result

    # Check if this is an ER relationship diagram (3 boxes in a row)
    er = format_er_relationship(block)
    if er is not None:
        return er

    # Try removing additional leading spaces from all lines
    current = stripped[:]
    for _ in range(10):
        attempt = []
        can_strip = all(l == '' or l.startswith(' ') for l in current)
        if not can_strip:
            break
        for s in current:
            if s.startswith(' '):
                attempt.append(s[1:])
            else:
                attempt.append(s)
        if max((len(l) for l in attempt), default=0) <= W:
            return attempt
        current = attempt

    # Try formatting as stacked side-by-side boxes
    stacked = format_side_by_side_boxes(block)
    if stacked is not None:
        # Verify all lines fit
        if all(len(l) <= W for l in stacked):
            return stacked

    return None

def compress_timeline(lines):
    """Compress a wide timeline to fit W chars.
    Shortens runs of ─ and spaces proportionally.
    Returns compressed lines, or None if can't fit without truncation."""
    result = []
    mw = max((len(l) for l in lines), default=0)
    if mw <= W:
        return lines

    all_fit = True
    for line in lines:
        if not line.strip():
            result.append('')
            continue

        # Keep shrinking ─ runs until it fits
        shortened = line
        for ratio in [0.6, 0.5, 0.4, 0.3, 0.2]:
            def shorten_runs(m, r=ratio):
                run = m.group(0)
                new_len = max(2, int(len(run) * r))
                return run[0] * new_len
            shortened = re.sub(r'─{3,}', shorten_runs, line)

            # Compress runs of spaces (4+)
            def shorten_spaces(m, r=ratio):
                run = m.group(0)
                new_len = max(1, int(len(run) * r))
                return ' ' * new_len
            shortened = re.sub(r' {4,}', shorten_spaces, shortened)

            if len(shortened) <= W:
                break

        if len(shortened) > W:
            all_fit = False
            # Don't hard-truncate — keep the shortened version
            # but flag that we couldn't fully fit

        result.append(shortened)

    if not all_fit:
        return None
    return result

def diagram_to_text(block):
    """Convert wide diagram to labeled text.
    Extracts meaningful text from box-drawn diagrams."""
    out = []
    seen = set()

    # First, try to identify distinct boxes and their contents
    # by looking for │ delimited text segments
    box_contents = []
    current_box = []
    for line in block:
        s = line.strip()
        if '┌' in s and current_box:
            # New box starting, save previous
            if current_box:
                box_contents.append(current_box[:])
            current_box = []
        if '│' in s:
            # Extract text between │ markers
            clean = s
            for c in BOX | {'▼', '▲', '◄', '►', '←', '→', '↑', '↓'}:
                clean = clean.replace(c, ' ')
            segs = [seg.strip() for seg in clean.split('  ') if seg.strip()]
            for seg in segs:
                if seg and len(seg) >= 2:
                    current_box.append(seg)
        elif '└' in s and current_box:
            box_contents.append(current_box[:])
            current_box = []
    if current_box:
        box_contents.append(current_box[:])

    # Also extract connecting text (arrows, labels between boxes)
    connectors = []
    for line in block:
        s = line.strip()
        clean = s
        for c in BOX | {'▼', '▲', '◄', '►'}:
            clean = clean.replace(c, ' ')
        # Keep arrows as they're meaningful
        clean = clean.replace('──→', ' → ').replace('←──', ' ← ')
        clean = clean.replace('→', ' → ').replace('←', ' ← ')
        segs = re.findall(r'\S+', clean)
        for seg in segs:
            seg = seg.strip()
            if (seg and len(seg) >= 2 and
                not all(c in '─│┌┐└┘├┤┬┴┼ |/\\' for c in seg)):
                connectors.append(seg)

    if box_contents:
        for bi, box in enumerate(box_contents):
            # Deduplicate content within this box
            seen_in_box = set()
            unique = []
            for item in box:
                key = item.lower()
                if key not in seen_in_box:
                    seen_in_box.add(key)
                    unique.append(item)
            if not unique:
                continue

            # Check if first item looks like a header (ALL CAPS or short)
            hdr = unique[0]
            body = unique[1:]
            words = hdr.split()
            is_hdr = (all(w.isupper() or not w.isalpha() for w in words) and
                      any(w.isalpha() and w.isupper() for w in words) and
                      len(words) <= 8)
            if is_hdr:
                out.extend(wrap(f"▶ {hdr}", W, '  '))
                for item in body:
                    out.extend(wrap(f"  • {item}", W, '    '))
            else:
                for item in unique:
                    out.extend(wrap(f"  • {item}", W, '    '))

            if bi < len(box_contents) - 1:
                # Add separator/connector
                out.append('')
        return out

    # Fallback: simple text extraction
    for line in block:
        clean = line
        for c in BOX | {'▼', '▲', '◄', '►', '←', '→', '↑', '↓'}:
            clean = clean.replace(c, ' ')
        segs = re.findall(r'\S+', clean)
        if not segs:
            continue
        text = ' '.join(segs)
        text = re.sub(r'\s{2,}', ' ', text).strip()
        if not text or len(text) < 2:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        out.extend(wrap(f"  • {text}", W, '    '))
    return out


# ════════════════════════════════════════
# NOTATION GUIDE
# ════════════════════════════════════════

def reformat_notation(lines):
    out = []
    for line in lines:
        s = line.strip()
        if not s:
            out.append('')
            continue
        entries = re.findall(r'(\S+)\s+—\s+(.+?)(?=\s{3,}\S+\s+—|$)', s)
        if entries:
            for sym, desc in entries:
                out.append(f"  {sym}  — {desc.strip()}")
        else:
            out.extend(wrap(s, W, '    '))
    return out


# ════════════════════════════════════════
# MAIN PROCESSING
# ════════════════════════════════════════

def process():
    with open(SRC, 'r', encoding='utf-8') as f:
        lines = [l.rstrip('\n') for l in f]
    n = len(lines)
    out = []
    i = 0

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # ── Notation section ──
        if stripped == 'NOTE ON NOTATION':
            out.append('NOTE ON NOTATION')
            out.append('─' * W)
            i += 1
            if i < n and is_divider(lines[i]):
                i += 1
            buf = []
            while i < n:
                if is_divider(lines[i]) and '═' in lines[i]:
                    break
                buf.append(lines[i])
                i += 1
            out.extend(reformat_notation(buf))
            out.append('')
            continue

        # ── Dividers ═══ or ─── or === ──
        if is_divider(stripped):
            if '═' in stripped or '=' in stripped:
                ch = '═'
            else:
                ch = '─'
            out.append(ch * W)
            i += 1
            continue

        # ── SET headers ──
        if is_set_header(stripped):
            m = re.match(r'(SET\s+\d+)\s*─+', stripped)
            if m:
                tag = m.group(1)
                out.append(f"{tag} {'─' * (W - len(tag) - 1)}")
            i += 1
            continue

        # ── Centered titles (ALL CAPS, centered in original) ──
        if ((stripped.isupper() or
             re.match(r'^[A-Z\s\(\)—×\d,]+$', stripped)) and
            len(line) - len(line.lstrip()) > 10 and
            len(stripped) > 5 and
            not is_q_start(stripped)):
            out.extend(wrap(stripped, W))
            i += 1
            continue

        # ── Box blocks: tables + diagrams ──
        if has_border(line) and not is_divider(stripped) and not is_set_header(stripped):
            block = []
            while i < n:
                cl = lines[i]
                cs = cl.strip()
                if has_border(cl) and not is_divider(cs) and not is_set_header(cs):
                    block.append(cl)
                    i += 1
                elif cl.strip() == '':
                    # blank — include if box continues after
                    j = i + 1
                    while j < n and lines[j].strip() == '':
                        j += 1
                    if j < n and has_border(lines[j]):
                        block.append(cl)
                        i += 1
                    else:
                        break
                elif '│' in cl or '▼' in cl or '▲' in cl:
                    block.append(cl)
                    i += 1
                elif '←' in cl or '→' in cl or '↑' in cl or '↓' in cl:
                    block.append(cl)
                    i += 1
                elif '|' in cl and any(has_border(lines[k]) for k in range(max(0, i-3), i)):
                    # Regular pipe char in context of a timeline diagram
                    block.append(cl)
                    i += 1
                else:
                    # text sandwiched between box lines?
                    j = i + 1
                    while j < n and not has_border(lines[j]) and lines[j].strip():
                        j += 1
                    if j < n and has_border(lines[j]) and j - i <= 4:
                        for k in range(i, j):
                            block.append(lines[k])
                        i = j
                    else:
                        break

            if not block:
                continue

            # Determine type from first full border line
            first_border = ''
            for bl in block:
                bs = bl.strip()
                if bs and all(c in BOX | {' '} for c in bs) and len(bs) > 5:
                    first_border = bs
                    break

            is_table = '┬' in first_border or '┼' in first_border

            if is_table:
                result = format_table_block(block)
                if result:
                    out.append('')
                    out.extend(result)
                    out.append('')
                else:
                    # Fallback: extract text
                    out.append('')
                    for tl in extract_box_text(block):
                        out.extend(wrap('  ' + tl, W, '    '))
                    out.append('')
            else:
                # Check if this is a timeline-style diagram (has ─ runs and |)
                is_tl = any('──' in bl and ('|' in bl or '→' in bl) for bl in block)
                # Check if it's a simple single-cell box
                # Count TOTAL ┌ chars across all lines (not just lines with ┌)
                total_box_corners = sum(bl.count('┌') for bl in block)
                is_simple_box = (total_box_corners <= 1 and len(block) <= 8 and
                                 not is_tl and
                                 any('┌' in bl for bl in block))

                if is_simple_box:
                    # Simple single-cell box — extract text
                    out.append('')
                    for tl in extract_box_text(block):
                        out.extend(wrap('  ' + tl, W, '    '))
                    out.append('')
                else:
                    # Complex diagram or timeline — try to fit
                    formatted = format_diagram(block)
                    if formatted:
                        out.append('')
                        out.extend(formatted)
                        out.append('')
                    else:
                        out.append('')
                        out.extend(diagram_to_text(block))
                        out.append('')
            continue

        # ── Question lines ──
        if is_q_start(stripped):
            q = stripped
            i += 1
            while i < n:
                nxt = lines[i]
                ns = nxt.strip()
                if (ns and not is_divider(ns) and
                    not is_set_header(ns) and
                    not ns.startswith('ANSWER') and
                    (len(nxt) - len(nxt.lstrip()) >= 5 or
                     (ns and ns[0].islower()))):
                    q += ' ' + ns
                    i += 1
                else:
                    break
            out.extend(wrap(q, W, '   '))
            continue

        # ── Blank lines ──
        if not stripped:
            out.append('')
            i += 1
            continue

        # ── Code blocks (indented SQL / RA / schema) ──
        indent_len = len(line) - len(line.lstrip())
        if indent_len >= 2 and (is_code(stripped) or stripped.startswith('--')):
            code = []
            in_code = True
            while i < n:
                cl = lines[i]
                cs = cl.strip()
                ci_len = len(cl) - len(cl.lstrip())
                if cs == '' and code:
                    # blank — peek ahead
                    j = i + 1
                    if (j < n and len(lines[j]) - len(lines[j].lstrip()) >= 2
                        and not is_divider(lines[j].strip())
                        and not is_set_header(lines[j].strip())):
                        code.append('')
                        i += 1
                    else:
                        break
                elif (ci_len >= 2 and cs and
                      not is_divider(cs) and not is_set_header(cs) and
                      not has_border(cl)):
                    code.extend(wrap_code_line(cs, W))
                    i += 1
                else:
                    break
            out.extend(code)
            continue

        # ── Relational algebra assignments and expressions ──
        if indent_len >= 2 and any(c in stripped for c in 'σπ⋈ρ𝒢←'):
            code = []
            while i < n:
                cl = lines[i]
                cs = cl.strip()
                ci_len = len(cl) - len(cl.lstrip())
                if cs == '' and code:
                    j = i + 1
                    if j < n and len(lines[j]) - len(lines[j].lstrip()) >= 2:
                        code.append('')
                        i += 1
                    else:
                        break
                elif (ci_len >= 2 and cs and
                      not is_divider(cs) and not is_set_header(cs) and
                      not has_border(cl)):
                    code.extend(wrap_code_line(cs, W))
                    i += 1
                else:
                    break
            out.extend(code)
            continue

        # ── Query tree blocks (indented with │ / \ and operators) ──
        if (indent_len >= 4 and
            ('│' in stripped or
             ('/' in stripped and '\\' in stripped) or
             stripped in ('│', '/ \\'))):
            tree = []
            while i < n:
                cl = lines[i]
                cs = cl.strip()
                ci_len = len(cl) - len(cl.lstrip())
                if cs == '' and tree:
                    j = i + 1
                    if j < n and len(lines[j]) - len(lines[j].lstrip()) >= 4:
                        tree.append(cl)
                        i += 1
                    else:
                        break
                elif ci_len >= 2 and cs:
                    tree.append(cl)
                    i += 1
                else:
                    break
            # Strip indent
            if tree:
                mi = min(len(l) - len(l.lstrip()) for l in tree if l.strip())
                for tl in tree:
                    s = tl[mi:].rstrip()
                    out.append(s[:W] if len(s) > W else s)
            continue

        # ── List items (•, ▸, -, numbered) ──
        lm = re.match(r'^(\s*)(•|▸|\-|\d+[\.\)])\s+(.*)', line)
        if lm:
            bullet = lm.group(2)
            text = lm.group(3)
            i += 1
            while i < n:
                nxt = lines[i]
                ns = nxt.strip()
                nind = len(nxt) - len(nxt.lstrip())
                if (ns and nind >= 4 and
                    not re.match(r'^(•|▸|\-|\d+[\.\)])\s', ns) and
                    not is_divider(ns) and not is_set_header(ns) and
                    not is_q_start(ns) and not has_border(nxt)):
                    text += ' ' + ns
                    i += 1
                else:
                    break
            pref = f"  {bullet} "
            hang = ' ' * len(pref)
            out.extend(wrap(pref + text, W, hang))
            continue

        # ── Section headers (ANSWER:, numbered ALL-CAPS headers, etc.) ──
        if is_section_header(stripped):
            out.extend(wrap(stripped, W, '  '))
            i += 1
            continue

        # ── ALL-CAPS label lines (like "SCHEMA (does not change frequently):") ──
        if (stripped.endswith(':') and len(stripped) < 60 and
            re.match(r'^[A-Z]', stripped)):
            # Check if it's a sub-header
            words = stripped[:-1].split()
            if len(words) <= 10 and any(w.isupper() for w in words):
                out.extend(wrap(stripped, W, '  '))
                i += 1
                continue

        # ── Prose paragraphs ──
        para = stripped
        i += 1
        while i < n:
            nxt = lines[i]
            ns = nxt.strip()
            nind = len(nxt) - len(nxt.lstrip())
            if (ns and
                not is_divider(ns) and
                not is_set_header(ns) and
                not is_q_start(ns) and
                not has_border(nxt) and
                not re.match(r'^(•|▸|\-|\d+[\.\)])\s', ns) and
                not ns == 'ANSWER:' and
                not is_section_header(ns) and
                not (nind >= 2 and (is_code(ns) or any(c in ns for c in 'σπ⋈ρ𝒢←'))) and
                not ('│' in ns and nind >= 4)):
                para += ' ' + ns
                i += 1
            else:
                break
        out.extend(wrap(para, W))
        continue

    # ── Post-process: limit consecutive blanks to 2 ──
    final = []
    bc = 0
    for line in out:
        if not line.strip():
            bc += 1
            if bc <= 2:
                final.append('')
        else:
            bc = 0
            final.append(line)

    # Write output
    with open(DST, 'w', encoding='utf-8') as f:
        for line in final:
            f.write(line + '\n')

    # Stats
    total = len(final)
    over_w = sum(1 for l in final if len(l) > W)
    max_len = max((len(l) for l in final), default=0)
    leaked_box = sum(1 for l in final if any(c in BOX for c in l))
    print(f"Lines: {total}")
    print(f"Max width: {max_len}")
    print(f"Lines > {W} chars: {over_w}")
    if over_w:
        print("Overwidth lines:")
        for li, l in enumerate(final, 1):
            if len(l) > W:
                print(f"  L{li} ({len(l)}): {l[:80]}...")
    print(f"Lines with box chars: {leaked_box}")


if __name__ == '__main__':
    process()
