# Blockmode — Block Sprite Editor

A tiny, dependency-free editor for block-ASCII sprites — the kind used in
terminal / PETSCII / C64-style games. Draw with block and box-drawing glyphs in
four colors over an optional background, animate them frame by frame, and
export to JSON, SVG, PNG or MP4.

**Live:** https://unowness.github.io/block-sprite-editor/

It is one self-contained HTML file with no build step and no backend — copy
`index.html` anywhere and open it in a browser.

## Drawing

- Pick a **glyph** from the palette and a **paint** (Main, Accent, Detail, Extra),
  then draw on the grid. **Right-click** erases.
- **Custom panel** — 16 slots for glyphs you use often. Select a glyph in the
  palette, then click an empty slot to store it there. Click a filled slot to
  draw with it; **Backspace** clears it. Pasting or typing into a slot also works.
- **Mirror** keeps the left and right halves symmetric as you paint.
- **Eraser** and **Select** (drag a rectangle, then move it or press Delete).
- **Undo/redo** per sprite: buttons or Ctrl/Cmd+Z.
- **Background** toggles the backdrop color; **Grid** toggles the cell overlay.
  Both are included in an export if they are active at export time.

## Canvas and animation

- Size from 3×3 to 128×128 — type into **W/H**, or drag any of the four edge
  handles to resize from that side.
- **Zoom** presets: 1×, 4×, 8×, 16×.
- **Frames** — add and delete frames, set **FPS** (1–60), and play the loop.
- **Fullscreen** renders the sprite 1:1 with the paint and custom panels docked
  at the bottom.

## Interface

- **Tabs** — several sprites open at once, each with its own undo history.
- **Theme** — Light and Dark, remembered between visits.
- **Autosave** — every open tab is written to `localStorage` and restored on the
  next visit. Nothing is sent anywhere; there is no backend.
- Works with touch: drag to paint, and the resize handles stay visible on
  coarse-pointer devices.

## Export

| Format | What you get |
| --- | --- |
| **JSON** | The full sprite, all frames — download or copy. Load it back to keep editing. |
| **SVG** | Current frame, vector. |
| **PNG** | Current frame, upscaled by the current zoom. |
| **MP4** | The animation loop (~2s), encoded with WebCodecs (H.264). |

MP4 needs WebCodecs — available in Chromium browsers and Safari 16.4+. Where it
is missing (Firefox today), the editor falls back to a WebM recording.

## Sprite JSON format

```json
{
  "version": 3,
  "id": "sprite",
  "width": 8,
  "height": 6,
  "body_color": "#6f74c0",
  "accent_color": "#b9a5f0",
  "decoration_color": "#f0a5c0",
  "extra_color": "#5CE422",
  "background_color": "#101018",
  "fps": 8,
  "active": 0,
  "custom_glyphs": ["▀", "▄"],
  "frames": [
    {
      "glyphs": ["row strings, one character per cell"],
      "colors": ["same dimensions; b/a/d/e per cell, space where empty"],
      "accent_mask": ["same dimensions; 'X' where the cell uses the accent color"]
    }
  ],
  "glyphs": ["..."],
  "colors": ["..."],
  "accent_mask": ["..."]
}
```

- `colors` encodes which paint each cell uses: `b` Main, `a` Accent,
  `d` Detail, `e` Extra, space for an empty cell.
- `background_color` is `null` when the background is switched off.
- `custom_glyphs` holds the custom panel, preserving slot positions
  (internal gaps stay as `""`, trailing empties are trimmed).
- The top-level `glyphs` / `colors` / `accent_mask` repeat the **active frame**
  so single-frame consumers can read a sprite without understanding `frames`.
- `accent_mask` is likewise kept for readers that predate the 4-color model;
  `colors` is the authoritative field.

Every glyph is a single-cell character — ASCII, Unicode Block Elements
(U+2580–U+259F) or Box Drawing (U+2500–U+257F) — so sprites render at a fixed
width in any terminal.

## License

MIT — see [LICENSE](LICENSE).
