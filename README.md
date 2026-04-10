# Playlist Vibe Builder

A Python app that uses **Quick Sort** to sort a music playlist by energy score or duration, with a step-by-step visual simulation built in **Gradio**.

---

## Chosen Problem

This app enables the user to load or enter a playlist of songs (title, artist, energy score 0–100, duration in seconds) and sort it by either energy or duration.

---

## Chosen Algorithm — Quick Sort

**Why Quick Sort fits this problem:**

Quick Sort is an excellent choice for playlist data because:
- The dataset is **unsorted and random** by default — Quick Sort's average O(n log n) performance handles this well.
- Energy scores are **distinct-enough integers** (0–100), making pivot selection meaningful and partition imbalance unlikely.
- The **in-place partitioning** is easy to visualize step-by-step.
- No precondition requires the data to be pre-sorted.
**Assumptions:**
- Energy scores are integers in the range 0–100.
- Duration is a positive integer (seconds).
- The dataset is between 2 and 20 songs.
- Duplicate energy values are handled correctly (≤ comparison places duplicates on the left).


---

## Demo

![Demo GIF](demo.gif)

---

## Problem Breakdown & Computational Thinking

### Decomposition
1. Parse and validate the user's playlist input.
2. Select a sort key (energy or duration).
3. Choose a pivot.
4. Partition: scan, compare each element to pivot, swap if needed.
5. Recursively apply to left and right sub-arrays.
6. Record every comparison and swap as a "step snapshot."
7. Render each snapshot as an HTML table row with colour highlights.
8. Display all steps sequentially in the Gradio UI.

### Pattern Recognition
- The **partition loop** repeats for every element in the sub-array: compare, swap if smaller, advance pointer.
- The **recursion** repeats the same process on smaller and smaller sub-arrays until each sub-array has 0 or 1 element.

### Abstraction
| Shown to user                         | Hidden from user                    |
|---------------------------------------|-------------------------------------|
| Pivot            | Call stack / recursion depth        |
| Which songs are being compared | Memory addresses / index arithmetic |
| Which sub-array is active | The `i` and `j` pointer internals   |
| Action label per step | Low-level swap mechanics            |

The user sees a music-themed story ("Pivot chosen: 'Blinding Lights'") rather than raw array indices.

### Algorithm Design

```
INPUT:
- List of songs formatted as: title, artist, energy, duration
- Choose between sorting by energy or duration
- Toggle showing steps ON/OFF

OUTPUT: HTML simulation in Gradio + plain-text ranked list

Constraints:
- Energy must be below 0-100
- Must input between 2-20 songs
- Duration must be in seconds
```

### Flowchart

```
┌─────────────────────────────────┐
│              START              │
└────────────────┬────────────────┘
                 ▼
     ┌───────────────────────┐
     │  User enters playlist │
     │  + chooses sort key   │
     │  run_sort()           │
     └───────────┬───────────┘
                 ▼
     ┌───────────────────────┐
     │  parse_custom_songs() │◄──── Error? Show message, STOP
     └───────────┬───────────┘
                 ▼
     ┌───────────────────────┐
     │  quick_sort_steps()   │
     │  low=0, high=n-1      │
     └───────────┬───────────┘
                 ▼
     ┌───────────────────────┐
     │  low < high?          │
     ├── NO → record "done"  │
     └───────────┬───────────┘
                 │ YES
                 ▼
     ┌───────────────────────┐
     │  partition(low, high) │
     │  pivot = arr[high]    │
     │  i = low - 1          │
     └───────────┬───────────┘
                 ▼
     ┌───────────────────────┐
     │  for j = low..high-1  │◄─────────────────────┐
     │  record COMPARE step  │                      │
     │  arr[j] <= pivot?     │                      │
     ├── YES: i++            │                      │
     │        swap arr[i],   │                      │
     │             arr[j]    │                      │
     │        record SWAP    │                      │
     └───────────┬───────────┘                      │
                 │                                  │
                 └──────────── j++ ─────────────────┘
                 ▼
     ┌───────────────────────┐
     │  swap pivot into      │
     │  position i+1         │
     │  record PIVOT PLACED  │
     └───────────┬───────────┘
                 ▼
     ┌───────────────────────┐
     │  quick_sort(low, pi-1)│  ← left sub-array
     │  quick_sort(pi+1,high)│  ← right sub-array
     └───────────┬───────────┘
                 ▼
     ┌───────────────────────┐
     │  Render all steps as  │
     │  HTML + plain text    │
     └───────────┬───────────┘
                 ▼
               DONE
```

---

## Steps to Run (Local)

**Requirements:** Python 3.10+

# 1. Clone the repo
git clone https://github.com/landonfraser17-wq/playlist-vibe-builder.git
cd playlist-vibe-builder

# 2. Install dependencies
`pip install -r requirements.txt`

# 3. Run the app
`python app.py`

Then open `http://localhost:7860` in your browser.

---

## Hugging Face Link

https://huggingface.co/spaces/landonfraser17/playlist-vibe-builder

---

## Testing

### Test Cases

| Test | Input | Expected | Actual | Pass? |
|------|-------|----------|--------|-------|
| Default playlist, sort by energy | 10-song sample | Ascending energy order | ✅  | ✅ |
| Default playlist, sort by duration | 10-song sample | Ascending duration order | ✅  | ✅ |
| Reverse sorted input | Songs entered high→low energy | Correctly sorted ascending | ✅  | ✅ |
| Duplicate energy values | Two songs both energy=50 | Both appear, order stable for equal values | ✅  | ✅ |
| Single song | 1 song entered | Error: "at least 2 songs" | ✅  | ✅ |
| Too many songs | 21 songs entered | Error: "at most 20 songs" | ✅  | ✅ |
| Bad energy value | Energy = "abc" | Error: "not a valid integer" | ✅  | ✅ |
| Energy out of range | Energy = 150 | Error: "must be between 0 and 100" | ✅  | ✅ |
| Missing fields | "Song, Artist, 80" (3 fields) | Error: "expected 4 fields" | ✅  | ✅ |
| Empty input | (blank text box) | Error: "at least 2 songs" | ✅  | ✅ |

### Validation of Sorting Correctness
The output was independently verified using Python's built-in `sorted()` on the same input (for testing only — `sorted()` is not used in the algorithm itself):

```python
# Verification snippet (not in production code)
result = [s[2] for s in final_sorted_output]
expected = sorted([s[2] for s in original], reverse=False)
assert result == expected  # ✅ passes for all test cases
```

---

## Author & Acknowledgments

**Author:** Landon Fraser — Student ID: 20551268 — CISC 121, Queen's University

**Sources:**
- Quick Sort algorithm concept: CISC 121 lecture notes
- Gradio documentation: [gradio.app/docs](https://gradio.app/docs)

**AI Use (Level 4):**
This project was completed with AI assistance (Claude). AI was used to:
- Help structure the Gradio UI layout
- Suggest HTML styling for the step-by-step table
- Review edge case handling in `parse_custom_songs()`

The Quick Sort algorithm logic and overall app architecture were designed and implemented by the author.

