"""
Playlist Vibe Builder — CISC 121 Project
Sorting Algorithm: Quick Sort
Problem: Sort a playlist by energy score or duration.
Author: Landon Fraser
"""

import gradio as gr
import random
import time

# ─────────────────────────────────────────
# DATA
# ─────────────────────────────────────────

# Default sample playlist (title, artist, energy 0-100, duration in seconds)
DEFAULT_SONGS = [
    ("Blinding Lights",    "The Weeknd",       87, 200),
    ("Levitating",         "Dua Lipa",         72, 203),
    ("As It Was",          "Harry Styles",     55, 167),
    ("Bad Guy",            "Billie Eilish",    40, 194),
    ("Montero",            "Lil Nas X",        93, 137),
    ("Watermelon Sugar",   "Harry Styles",     60, 174),
    ("Good 4 U",           "Olivia Rodrigo",   81, 178),
    ("Stay",               "Kid LAROI",        68, 141),
    ("Peaches",            "Justin Bieber",    45, 198),
    ("drivers license",    "Olivia Rodrigo",   28, 242),
]


def generate_random_playlist(n: int = 8) -> list[tuple]:
    """Generate a random playlist of n songs with random energy/duration."""
    titles = [
        "Midnight Run", "Solar Flare", "Chill Pulse", "Storm Chaser",
        "Neon Dream", "Quiet Storm", "Electric Feel", "Deep Blue",
        "Golden Hour", "Dark Matter", "Velvet Rush", "Cloud Nine",
        "Thunder Road", "Soft Reset", "Fever Pitch", "Slow Burn",
    ]
    artists = [
        "Luna Echo", "Solar Boys", "The Drift", "Cascade",
        "Nightwave", "Static Bloom", "Ember & Ash", "The Tides",
    ]
    songs = []
    used_titles = random.sample(titles, min(n, len(titles)))
    for i in range(n):
        title = used_titles[i] if i < len(used_titles) else f"Track {i+1}"
        artist = random.choice(artists)
        energy = random.randint(10, 99)
        duration = random.randint(120, 280)
        songs.append((title, artist, energy, duration))
    return songs


# QUICK SORT
# Records each comparison/swap as a "step"

def quick_sort_steps(arr: list, key_index: int) -> list[dict]:
    """
    Perform Quick Sort on arr (list of tuples), sorting by arr[i][key_index].
    Returns a list of step snapshots for animation.
    Each step: { 'array': [...], 'pivot_idx': int, 'comparing': [i,j], 'action': str }
    """
    steps = []
    working = list(arr)  # work on a copy

    def record(pivot_idx, comparing, action, left=None, right=None):
        steps.append({
            "array": list(working),
            "pivot_idx": pivot_idx,
            "comparing": comparing,
            "action": action,
            "left": left,
            "right": right,
        })

    def partition(low: int, high: int) -> int:
        """
        Choose the rightmost element as pivot.
        Move all elements smaller than pivot to its left.
        Return the final index of the pivot.
        """
        pivot_val = working[high][key_index]
        i = low - 1  # index of smaller element

        record(high, [], f"Pivot chosen: '{working[high][0]}' (value={pivot_val})", low, high)

        for j in range(low, high):
            # Compare current element with pivot
            record(high, [j], f"Comparing '{working[j][0]}' ({working[j][key_index]}) vs pivot ({pivot_val})", low, high)

            if working[j][key_index] <= pivot_val:
                # Current element belongs on the left side
                i += 1
                if i != j:
                    working[i], working[j] = working[j], working[i]
                    record(high if high != i else j, [i, j],
                           f"Swap '{working[i][0]}' ↔ '{working[j][0]}'", low, high)

        # Place pivot in its correct sorted position
        working[i + 1], working[high] = working[high], working[i + 1]
        pivot_final = i + 1
        record(pivot_final, [pivot_final],
               f"Pivot '{working[pivot_final][0]}' placed at position {pivot_final}", low, high)
        return pivot_final

    def quick_sort(low: int, high: int):
        """Recursively sort sub-arrays around the partition index."""
        if low < high:
            pi = partition(low, high)   # pi = pivot's sorted index
            quick_sort(low, pi - 1)     # sort left sub-array
            quick_sort(pi + 1, high)    # sort right sub-array

    quick_sort(0, len(working) - 1)

    # Final sorted state
    record(-1, [], "✅ Sorting complete!", 0, len(working) - 1)
    return steps


# FORMATTING HELPERS

def fmt_duration(seconds: int) -> str:
    """Convert seconds to m:ss format."""
    return f"{seconds // 60}:{seconds % 60:02d}"


def songs_to_table_html(songs: list, highlight_indices: list = None,
                         pivot_idx: int = -1, left: int = None, right: int = None) -> str:
    """Render songs as a styled HTML table with optional highlights."""
    if highlight_indices is None:
        highlight_indices = []

    rows = ""
    for i, (title, artist, energy, duration) in enumerate(songs):
        # Determine row styling
        if i == pivot_idx:
            bg = "#ff6b35"   # orange = pivot
            fw = "bold"
            label = " 🎯 pivot"
        elif i in highlight_indices:
            bg = "#4ecdc4"   # teal = being compared
            fw = "bold"
            label = " 👀 comparing"
        elif left is not None and right is not None and left <= i <= right:
            bg = "#2a2a3e"   # dark blue = active sub-array
            fw = "normal"
            label = ""
        else:
            bg = "#1a1a2e"
            fw = "normal"
            label = ""

        # Energy bar (visual)
        bar_width = energy
        energy_bar = (
            f'<div style="background:#0f3460;border-radius:4px;height:10px;width:100px;display:inline-block;vertical-align:middle">'
            f'<div style="background:#e94560;border-radius:4px;height:10px;width:{bar_width}px"></div></div>'
        )

        rows += (
            f'<tr style="background:{bg};font-weight:{fw};transition:background 0.3s">'
            f'<td style="padding:8px 12px;color:#ccc">{i + 1}</td>'
            f'<td style="padding:8px 12px;color:#fff">{title}{label}</td>'
            f'<td style="padding:8px 12px;color:#aaa">{artist}</td>'
            f'<td style="padding:8px 12px;color:#fff">{energy_bar} {energy}</td>'
            f'<td style="padding:8px 12px;color:#aaa">{fmt_duration(duration)}</td>'
            f'</tr>'
        )

    return (
        '<table style="width:100%;border-collapse:collapse;font-family:monospace;font-size:13px">'
        '<thead><tr style="background:#0f3460;color:#e94560">'
        '<th style="padding:8px 12px">#</th>'
        '<th style="padding:8px 12px">Title</th>'
        '<th style="padding:8px 12px">Artist</th>'
        '<th style="padding:8px 12px">Energy</th>'
        '<th style="padding:8px 12px">Duration</th>'
        '</tr></thead>'
        f'<tbody>{rows}</tbody></table>'
    )


def parse_custom_songs(text: str) -> list[tuple] | str:
    """
    Parse user-entered songs from text.
    Expected format per line: Title, Artist, Energy(0-100), Duration(seconds)
    Returns list of tuples or an error string.
    """
    songs = []
    for line_num, line in enumerate(text.strip().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 4:
            return f"❌ Line {line_num}: expected 4 fields (Title, Artist, Energy, Duration), got {len(parts)}."
        title, artist = parts[0], parts[1]
        try:
            energy = int(parts[2])
            if not (0 <= energy <= 100):
                return f"❌ Line {line_num}: Energy must be between 0 and 100."
        except ValueError:
            return f"❌ Line {line_num}: Energy '{parts[2]}' is not a valid integer."
        try:
            duration = int(parts[3])
            if duration <= 0:
                return f"❌ Line {line_num}: Duration must be a positive integer (seconds)."
        except ValueError:
            return f"❌ Line {line_num}: Duration '{parts[3]}' is not a valid integer."
        songs.append((title, artist, energy, duration))

    if len(songs) < 2:
        return "❌ Please enter at least 2 songs."
    if len(songs) > 20:
        return "❌ Please enter at most 20 songs (keep it manageable!)."
    return songs


# GRADIO HANDLERS

def load_default_playlist():
    """Load the built-in sample playlist into the text box."""
    lines = "\n".join(
        f"{t}, {a}, {e}, {d}" for t, a, e, d in DEFAULT_SONGS
    )
    return lines


def randomize_playlist():
    """Generate a fresh random playlist."""
    songs = generate_random_playlist(random.randint(6, 10))
    lines = "\n".join(
        f"{t}, {a}, {e}, {d}" for t, a, e, d in songs
    )
    return lines


def run_sort(playlist_text: str, sort_key: str, show_steps: bool):
    """
    Parse the playlist, run Quick Sort, and return:
    - step-by-step HTML animation frames (as a single HTML string with all steps)
    - summary text
    """
    # Validate / parse input
    result = parse_custom_songs(playlist_text)
    if isinstance(result, str):  # error message
        return result, ""

    songs = result
    key_index = 2 if sort_key == "Energy Score" else 3  # tuple index
    key_label = sort_key

    # Run Quick Sort and collect steps
    steps = quick_sort_steps(songs, key_index)

    total_steps = len(steps)
    comparisons = sum(1 for s in steps if s["action"].startswith("Comparing"))
    swaps = sum(1 for s in steps if s["action"].startswith("Swap"))

    # Build the output
    if show_steps:
        # Show every step as an HTML block
        html_parts = [
            f'<div style="font-family:monospace;background:#0d0d1a;padding:16px;border-radius:10px;color:#eee">'
            f'<h3 style="color:#e94560;margin-top:0">🎵 Quick Sort — Sorting by {key_label}</h3>'
            f'<p style="color:#aaa">Songs: {len(songs)} | Steps: {total_steps} | '
            f'Comparisons: {comparisons} | Swaps: {swaps}</p>'
            f'<hr style="border-color:#333">'
        ]

        for idx, step in enumerate(steps):
            html_parts.append(
                f'<details {"open" if idx == 0 or idx == total_steps - 1 else ""}>'
                f'<summary style="cursor:pointer;padding:6px;color:#4ecdc4;font-weight:bold">'
                f'Step {idx + 1}/{total_steps}: {step["action"]}</summary>'
                f'<div style="padding:8px 0">'
                + songs_to_table_html(
                    step["array"],
                    highlight_indices=step["comparing"],
                    pivot_idx=step["pivot_idx"],
                    left=step["left"],
                    right=step["right"],
                )
                + f'</div></details>'
            )
        html_parts.append('</div>')
        steps_html = "\n".join(html_parts)
    else:
        # Just show original → sorted
        final = steps[-1]["array"]
        steps_html = (
            f'<div style="font-family:monospace;background:#0d0d1a;padding:16px;border-radius:10px;color:#eee">'
            f'<h3 style="color:#e94560;margin-top:0">🎵 Sorted by {key_label} (Quick Sort)</h3>'
            f'<p style="color:#aaa">Comparisons: {comparisons} | Swaps: {swaps}</p>'
            + songs_to_table_html(final)
            + '</div>'
        )

    # Summary text
    final_sorted = steps[-1]["array"]
    summary_lines = [f"Sorted playlist by {key_label} (ascending):"]
    for rank, (title, artist, energy, duration) in enumerate(final_sorted, 1):
        val = energy if key_index == 2 else fmt_duration(duration)
        summary_lines.append(f"  {rank}. {title} — {artist}  [{key_label}: {val}]")
    summary_lines.append(f"\nTotal steps: {total_steps}  |  Comparisons: {comparisons}  |  Swaps: {swaps}")

    return steps_html, "\n".join(summary_lines)


# GRADIO UI

CSS = """
body, .gradio-container, footer { background: #0d0d1a !important; }
.prose h1, .prose h2, .prose h3, label span { color: #e94560 !important; }
button.primary { background: #e94560 !important; border: none !important; }
textarea, .block { background: #1a1a2e !important; color: #eee !important; }
"""

with gr.Blocks(title="🎵 Playlist Vibe Builder") as demo:

    gr.Markdown("""
# 🎵 Playlist Vibe Builder
### Quick Sort Algorithm Visualizer — CISC 121
Sort your playlist by **Energy Score** or **Duration** using a step-by-step Quick Sort simulation.

**Legend:** 🎯 Orange = Pivot &nbsp;|&nbsp; 👀 Teal = Being Compared &nbsp;|&nbsp; 🟦 Dark Blue = Active Sub-array
""")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📋 Your Playlist")
            gr.Markdown("One song per line: `Title, Artist, Energy(0–100), Duration(seconds)`")

            playlist_input = gr.Textbox(
                label="Playlist (editable)",
                lines=12,
                placeholder="Blinding Lights, The Weeknd, 87, 200\nBad Guy, Billie Eilish, 40, 194\n...",
                value="\n".join(f"{t}, {a}, {e}, {d}" for t, a, e, d in DEFAULT_SONGS),
            )

            with gr.Row():
                btn_default = gr.Button("🎵 Load Sample", variant="secondary")
                btn_random = gr.Button("🎲 Randomize", variant="secondary")

            sort_key = gr.Radio(
                choices=["Energy Score", "Duration"],
                value="Energy Score",
                label="Sort by",
            )
            show_steps = gr.Checkbox(
                label="Show step-by-step simulation",
                value=True,
            )
            btn_sort = gr.Button("▶ Run Quick Sort", variant="primary", size="lg")

        with gr.Column(scale=2):
            gr.Markdown("### 🔍 Simulation Output")
            output_html = gr.HTML()
            output_text = gr.Textbox(label="Sorted Result (plain text)", lines=14, interactive=False)

    # Wire up buttons
    btn_default.click(fn=load_default_playlist, outputs=playlist_input)
    btn_random.click(fn=randomize_playlist, outputs=playlist_input)
    btn_sort.click(fn=run_sort, inputs=[playlist_input, sort_key, show_steps],
                   outputs=[output_html, output_text])

    gr.Markdown("""
---
**How Quick Sort works here:**
1. Pick the **last song** in the current sub-array as the **pivot**.
2. Scan left-to-right; songs with a lower value than the pivot move left.
3. Place the pivot in its correct sorted position.
4. Recursively repeat on the left and right sub-arrays.

*Algorithm implemented from scratch — no `sorted()` or `list.sort()` used.*
""")

if __name__ == "__main__":
    demo.launch(css=CSS, theme=gr.themes.Base())
