# Block Sprite Editor

A tiny, dependency-free editor for block-ASCII sprites — the kind used in
terminal / PETSCII / C64-style games. Draw with block and box-drawing glyphs in
two colors (body + accent), keep it symmetric with mirror painting, and
export/import JSON to drop sprites into any project.

**Live:** https://unowness.github.io/block-sprite-editor/

It is one self-contained HTML file with no dependencies — copy `index.html`
anywhere and open it in a browser.

## Use

- Pick a glyph from the palette, choose **body** or **accent** color, draw on the grid.
- **Right-click** erases. **Mirror** keeps the left/right halves symmetric.
- **Grid** toggles the gray cell overlay; turn it off to see the clean result.
- **Undo**: button or Ctrl/Cmd+Z. **Zoom** and **W/H** resize the canvas.
- **Export JSON** writes the sprite; paste a sprite's JSON and click **Load JSON** to edit it.

## Sprite JSON format

```json
{
  "id": "name",
  "width": 8,
  "height": 6,
  "body_color": "#6f74c0",
  "accent_color": "#b9a5f0",
  "glyphs": ["row strings, one character per cell"],
  "accent_mask": ["same dimensions; 'X' where the cell uses the accent color, space otherwise"]
}
```

Every glyph is a single-cell character — ASCII, Unicode Block Elements
(U+2580–U+259F) or Box Drawing (U+2500–U+257F) — so sprites render at a fixed
width in any terminal.

## License

MIT — see [LICENSE](LICENSE).
