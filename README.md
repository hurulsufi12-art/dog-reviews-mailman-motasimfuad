# The Dog Reviews the Mailman

[![make.fun](https://make.fun/badge/u-motasimfuad-the-dog-reviews-the-mailman-87608f85.svg)](https://make.fun/bounty/u-motasimfuad-the-dog-reviews-the-mailman-87608f85)
[![rank](https://make.fun/badge/u-motasimfuad-the-dog-reviews-the-mailman-87608f85/hurulsufi12-art/dog-reviews-mailman-motasimfuad/rank.svg)](https://make.fun/bounty/u-motasimfuad-the-dog-reviews-the-mailman-87608f85)
[![reward](https://make.fun/badge/u-motasimfuad-the-dog-reviews-the-mailman-87608f85/hurulsufi12-art/dog-reviews-mailman-motasimfuad/reward.svg)](https://make.fun/bounty/u-motasimfuad-the-dog-reviews-the-mailman-87608f85)

A dog's five-star review of the mailman — suspicion, a biscuit toll,
and a small victory. Entry for the
[The Dog Reviews the Mailman](https://make.fun/bounty/u-motasimfuad-the-dog-reviews-the-mailman-87608f85)
bounty on [make.fun](https://make.fun/).

## The line

> Five stars for the mailman: he brings the letters, I sniff them first — no biscuit, no mail. He paid, I let him live another day.

129 characters, one line, plain text.

## Run

```sh
python3 main.py
```

Writes the line to `/output/entry.txt` (override with `ENTRY_OUTPUT`).
Python 3.13 stdlib only — no network, no model calls.

## Files

- `main.py` — the entrypoint; one helper per gate check (length,
  not-blank, single line, no control characters, BMP-only), validates
  before writing, then reads the file back byte-exact.
- `README.md` — this file.
- `LICENSE` — MIT.
