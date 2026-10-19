# Image-generation prompts for the LOINC-Ontology-2.82 / MTB coordination story

Three prompts at different fidelity levels — pick by your target tool. All written for a 16:9 hero image (slide deck, IG cover, blog post).

---

## Prompt 1 — Diagrammatic (Midjourney v6 / DALL·E 3 / SDXL)

> A clean, modern technical infographic on a dark navy background, illustrating the coordination between three medical terminology authorities — HL7, SNOMED International, and LOINC/Regenstrief — converging on a single shared release artifact labeled "LOINC Ontology 2.82, March 2026". Three glowing hexagonal nodes at the top in violet, sky-blue, and amber, connected by luminous data-flow lines pointing down to a central panel labeled with a release identifier. Below it, a grid of small biomarker cards (HER2, ER, PR, Ki-67, BRAF V600E, ALK, MMR panel, p53) arranged like a molecular tumor board worklist. Subtle DNA helix and IHC microscope-slide motifs in the background, very faint. Typography: thin geometric sans-serif. Color palette: deep slate, electric cyan, warm amber, soft magenta. High detail, editorial quality, no people, no text artifacts. Aspect ratio 16:9. Style: a cross between a Bloomberg terminal dashboard and a scientific journal cover.
>
> `--ar 16:9 --style raw --v 6`

---

## Prompt 2 — Editorial / metaphorical (Midjourney, Ideogram)

> Three open hands reaching toward a single softly glowing crystal at the center of the frame, viewed from above. Each hand wears a thin band of light in a different color — violet, sky-blue, amber — representing three institutions. The crystal contains tiny floating glyphs: protein structures, microscope-slide squares, and barcode-like terminology codes. A faint molecular DNA double helix curves through the background. Soft, cinematic, high-contrast lighting. Editorial photography style, shallow depth of field, dark navy and graphite background, no text or letters. Visualizes scientific consortia building shared infrastructure for cancer diagnostics. 16:9.
>
> `--ar 16:9 --style raw --v 6`

---

## Prompt 3 — Abstract / cover-art (DALL·E 3, SDXL, Ideogram)

> An abstract data visualization rendered as flowing ribbons of light, three streams in violet, sky-blue, and amber, braiding together along the horizontal centerline and merging into a single bright gold strand on the right. Faint contour lines of histology and IHC-stained tissue mottle the lower background like a topographic map of breast cancer pathology. Particle constellations along the streams resemble SNOMED concept identifiers and barcodes. Mood: scientific, calm, optimistic. Color palette: midnight navy base, neon violet, sky cyan, hospital amber, warm parchment highlights. No people, no readable text. 16:9, editorial cover-art quality, suitable for a medical informatics journal.
>
> `--ar 16:9 --style raw --v 6`

---

## Notes on usage

- **Prompt 1** is the most informative — it will reproduce something close to the SVG diagram with imagery flourishes. Use when the audience needs to recognize the three-org structure.
- **Prompt 2** works as a slide opener or section divider. The hands metaphor reads instantly as "collaboration" without needing a viewer to parse a diagram.
- **Prompt 3** is the safe abstract — works on any deck, never looks wrong, but conveys less narrative.

If the model refuses or fights the prompt (DALL·E sometimes balks at "biomarker" or "tumor" language), substitute *"laboratory analytes"* for *"biomarkers"* and *"oncology diagnostics"* for *"tumor board"*. The visual concept survives the rewording.

If you want a tighter brand match to the existing dashboard, the color triple is:
- HL7 violet      `#b48ff5`
- SNOMED blue     `#5fb1ee`
- LOINC amber     `#f8c155`
- Background      `#0f1216`

Add `"in the style of #b48ff5 violet, #5fb1ee sky-blue, #f8c155 amber on a #0f1216 charcoal background"` to any of the three prompts to lock the palette.
