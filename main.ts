// news-image-20261117 — "The World in One Day", Tuesday 17 November 2026.
// Rebuilt 2026-11-18: 30 verified stories, a world map with 10 numbered
// flashpoints, three featured stories and a 12-story grid, all drawn by
// generate-image.py (Pillow, offline) and shipped beside this file as
// entry.png. This program copies that PNG, byte for byte, to the output
// directory the grader provides, after checking it really is a PNG.
// Node 22, standard library only. No network, no randomness, so two runs
// always write the same bytes.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

// The PNG signature: the first eight bytes every PNG file starts with.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const src = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');

// Guard 1: the shipped file must be a real PNG, not a truncated copy.
const head = readFileSync(src).subarray(0, PNG_MAGIC.length);
if (!head.equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG file');
}
copyFileSync(src, dest);
// Guard 2: the copy must be byte-identical in size, or the run is wrong.
if (statSync(src).size !== statSync(dest).size) {
  throw new Error('entry.png copy size mismatch');
}
