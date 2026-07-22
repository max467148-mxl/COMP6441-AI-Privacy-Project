import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const ROOT = path.resolve("..");
const OUT = path.join(ROOT, "submission");
const QA = path.join(ROOT, "qa", "slides");
const W = 1280;
const H = 720;
const C = {
  ink: "#101418",
  muted: "#53606A",
  panel: "#EDEDED",
  rule: "#B8BCC4",
  blue: "#3D8DFF",
  cyan: "#6DCBF4",
  pale: "#D0EDFA",
  green: "#2A9D8F",
  red: "#D85B4A",
  white: "#FFFFFF",
};

function shape(slide, name, geometry, left, top, width, height, fill = "none", lineFill = "none", lineWidth = 0) {
  return slide.shapes.add({
    name,
    geometry,
    position: { left, top, width, height },
    fill,
    line: { style: "solid", fill: lineFill, width: lineWidth },
  });
}

function text(slide, name, value, left, top, width, height, fontSize, options = {}) {
  const box = shape(slide, name, "textbox", left, top, width, height);
  box.text = value;
  box.text.style = {
    fontSize,
    fontFamily: "Arial",
    color: options.color || C.ink,
    bold: options.bold || false,
    alignment: options.alignment || "left",
    verticalAlignment: options.verticalAlignment || "top",
  };
  return box;
}

function title(slide, value, number) {
  text(slide, `slide-${number}-title`, value, 48, 34, 1115, 80, 38, { bold: true });
  text(slide, `slide-${number}-number`, String(number).padStart(2, "0"), 1180, 45, 50, 30, 14, { color: C.muted, alignment: "right" });
  shape(slide, `slide-${number}-rule`, "rect", 48, 114, 1184, 2, C.ink);
}

function pill(slide, name, value, left, top, width, fill = C.pale) {
  shape(slide, `${name}-bg`, "rect", left, top, width, 34, fill);
  text(slide, name, value, left + 10, top + 7, width - 20, 22, 14, { bold: true });
}

function metric(slide, name, value, label, left, top, width, color) {
  shape(slide, `${name}-panel`, "rect", left, top, width, 175, C.panel);
  shape(slide, `${name}-accent`, "rect", left, top, width, 8, color);
  text(slide, `${name}-value`, value, left + 22, top + 32, width - 44, 62, 46, { bold: true });
  text(slide, `${name}-label`, label, left + 22, top + 110, width - 44, 42, 17, { color: C.muted });
}

async function imageBytes(file) {
  const bytes = await fs.readFile(file);
  return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
}

async function main() {
  await fs.mkdir(OUT, { recursive: true });
  await fs.mkdir(QA, { recursive: true });
  const deck = Presentation.create({ slideSize: { width: W, height: H } });

  // Slide 1: sparse title layout adapted from Codex Grid slide 01.
  {
    const s = deck.slides.add();
    s.background.fill = C.white;
    pill(s, "course-label", "COMP6441  |  CYBERSECURITY INDEPENDENT PROJECT", 48, 42, 390, C.pale);
    text(s, "cover-title", "When harmless fragments\nbecome sensitive", 48, 160, 880, 190, 58, { bold: true });
    text(s, "cover-subtitle", "Measuring privacy leakage through AI context aggregation", 52, 382, 740, 56, 24, { color: C.muted });
    const fragments = ["7:42 bus", "campus library", "shared rent", "evening class", "ocean pool", "retail shift"];
    fragments.forEach((f, i) => {
      const x = 820 + (i % 2) * 205;
      const y = 165 + Math.floor(i / 2) * 105;
      shape(s, `fragment-${i}-panel`, "rect", x, y, 180, 72, i === 5 ? C.cyan : C.panel);
      text(s, `fragment-${i}`, f, x + 14, y + 23, 152, 28, 17, { bold: i === 5 });
    });
    text(s, "cover-meta", "Xiaolong Ma  |  zXXXXXXX  |  90 controlled prompts", 52, 632, 720, 28, 16, { color: C.muted });
    text(s, "cover-takeaway", "The combination reveals more than any single item.", 820, 525, 385, 64, 24, { bold: true, color: C.blue });
  }

  // Slide 2: process layout adapted from Codex Grid slide 17.
  {
    const s = deck.slides.add();
    s.background.fill = C.white;
    title(s, "Aggregation creates a new disclosure surface", 2);
    const xs = [70, 350, 630, 910];
    for (let i = 0; i < 3; i++) {
      shape(s, `flow-arrow-${i}`, "rightArrow", xs[i] + 205, 293, 72, 42, C.cyan);
    }
    const items = [
      ["01", "Ordinary fragments", "Transport, study, shopping, work"],
      ["02", "Context policy", "Which memories cross the task boundary?"],
      ["03", "Model inference", "Correlates time, place and purpose"],
      ["04", "Sensitive profile", "Location, schedule, occupation, finance"],
    ];
    items.forEach(([n, h, b], i) => {
      shape(s, `flow-${i}-panel`, "rect", xs[i], 220, 205, 190, i === 3 ? C.pale : C.panel);
      text(s, `flow-${i}-number`, n, xs[i] + 18, 238, 48, 30, 16, { color: C.blue, bold: true });
      text(s, `flow-${i}-heading`, h, xs[i] + 18, 280, 168, 52, 21, { bold: true });
      text(s, `flow-${i}-body`, b, xs[i] + 18, 340, 168, 54, 16, { color: C.muted });
    });
    text(s, "linddun", "LINDDUN focus: linkability enables inference and disclosure", 70, 475, 900, 36, 22, { bold: true });
    text(s, "scope", "Synthetic profiles only. No real-person identification, secret extraction or cross-user data access.", 70, 535, 1070, 52, 18, { color: C.muted });
  }

  // Slide 3: method with evidence image, adapted from Codex Grid slide 08/19.
  {
    const s = deck.slides.add();
    s.background.fill = C.white;
    title(s, "Ninety isolated trials tested context and controls", 3);
    metric(s, "profiles", "3", "synthetic profiles", 48, 154, 205, C.blue);
    metric(s, "prompts", "90", "first responses preserved", 273, 154, 205, C.cyan);
    metric(s, "baseline", "60", "4 contexts x 5 questions", 48, 353, 205, C.green);
    metric(s, "mitigation", "30", "2 controls at full context", 273, 353, 205, C.red);
    const screenshot = await imageBytes(path.join(ROOT, "evidence", "screenshots", "formal_001_temporary_chat.png"));
    s.images.add({
      name: "temporary-chat-evidence",
      blob: screenshot,
      contentType: "image/png",
      alt: "ChatGPT Temporary Chat used for an isolated formal experiment prompt",
      fit: "contain",
      position: { left: 540, top: 154, width: 692, height: 388 },
      geometry: "rect",
      line: { style: "solid", fill: C.rule, width: 1 },
    });
    text(s, "method-caption", "Each prompt opened in a new Temporary Chat; all 90 outputs parsed as JSON.", 540, 564, 692, 42, 18, { bold: true });
    text(s, "method-model", "Interface label: ChatGPT Plus, High mode; exact model ID not exposed.", 540, 618, 692, 26, 14, { color: C.muted });
  }

  // Slide 4: chart-led evidence layout adapted from Codex Grid slide 20.
  {
    const s = deck.slides.add();
    s.background.fill = C.white;
    title(s, "More linked context drove leakage from 0.53 to 0.97", 4);
    s.charts.add("bar", {
      position: { left: 60, top: 160, width: 735, height: 430 },
      categories: ["No memory", "Limited", "Compartment", "Full aggregate"],
      series: [{ name: "Leakage score (%)", values: [53, 83, 93, 97], fill: C.blue }],
      hasLegend: false,
      dataLabels: { showValue: true, position: "outEnd" },
      yAxis: { min: 0, max: 100, majorUnit: 20, majorGridlines: { style: "solid", fill: "#E4E7EA", width: 1 } },
    });
    shape(s, "result-callout", "rect", 845, 170, 340, 175, C.panel);
    text(s, "result-value", "+0.44", 870, 200, 270, 60, 44, { bold: true, color: C.blue });
    text(s, "result-copy", "leakage increase from one fragment to all fifteen", 870, 275, 270, 54, 18, { color: C.muted });
    shape(s, "confidence-callout", "rect", 845, 375, 340, 175, C.pale);
    text(s, "confidence-value", "0.55 → 0.83", 870, 405, 285, 54, 35, { bold: true });
    text(s, "confidence-copy", "mean model-reported confidence also increased", 870, 475, 275, 54, 18, { color: C.muted });
    text(s, "result-footnote", "Baseline only; n = 15 responses per condition. Descriptive scores, not population estimates.", 60, 625, 1120, 28, 14, { color: C.muted });
  }

  // Slide 5: mitigation comparison adapted from Codex Grid slide 21.
  {
    const s = deck.slides.add();
    s.background.fill = C.white;
    title(s, "Simple mitigations barely changed disclosure", 5);
    s.charts.add("bar", {
      position: { left: 60, top: 165, width: 690, height: 420 },
      categories: ["No mitigation", "Generalise details", "Warning prompt"],
      series: [{ name: "Leakage score (%)", values: [97, 93, 97], fill: C.red }],
      hasLegend: false,
      dataLabels: { showValue: true, position: "outEnd" },
      yAxis: { min: 0, max: 100, majorUnit: 20, majorGridlines: { style: "solid", fill: "#E4E7EA", width: 1 } },
    });
    const findings = [
      ["Exact-detail redaction", "Only a 0.04 reduction; broader routines still linked."],
      ["Sensitive-inference warning", "No score reduction; confidence fell by about 0.03."],
      ["Weak compartments", "Five correlated fragments still leaked 0.93."],
    ];
    findings.forEach(([h, b], i) => {
      const y = 168 + i * 145;
      shape(s, `finding-${i}-panel`, "rect", 810, y, 390, 116, i === 1 ? C.pale : C.panel);
      text(s, `finding-${i}-title`, h, 832, y + 18, 345, 28, 19, { bold: true });
      text(s, `finding-${i}-body`, b, 832, y + 56, 345, 48, 16, { color: C.muted });
    });
    text(s, "mitigation-footnote", "Full aggregated context only; n = 15 per treatment.", 60, 625, 800, 28, 14, { color: C.muted });
  }

  // Slide 6: four-point close adapted from Codex Grid slide 13.
  {
    const s = deck.slides.add();
    s.background.fill = C.white;
    title(s, "Protect privacy before context reaches the model", 6);
    const recommendations = [
      ["01", "Minimise", "Retrieve only what the current task needs."],
      ["02", "Isolate by purpose", "Test whether each compartment still encodes sensitive attributes."],
      ["03", "Red-team combinations", "Evaluate linkability and attribute inference, not only direct secrets."],
      ["04", "Treat warnings as secondary", "Enforce boundaries in data flow, then add policy instructions."],
    ];
    recommendations.forEach(([n, h, b], i) => {
      const x = 55 + (i % 2) * 600;
      const y = 160 + Math.floor(i / 2) * 215;
      text(s, `rec-${i}-number`, n, x, y, 50, 30, 16, { color: C.blue, bold: true });
      text(s, `rec-${i}-title`, h, x + 65, y - 2, 485, 38, 24, { bold: true });
      shape(s, `rec-${i}-rule`, "rect", x + 65, y + 48, 485, 2, C.rule);
      text(s, `rec-${i}-body`, b, x + 65, y + 68, 485, 70, 18, { color: C.muted });
    });
    shape(s, "closing-band", "rect", 55, 590, 1165, 68, C.ink);
    text(s, "closing-message", "Privacy is a property of the combination, not just the individual fragment.", 80, 608, 1115, 34, 25, { bold: true, color: C.white, alignment: "center" });
  }

  for (const [index, slide] of deck.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    const png = await deck.export({ slide, format: "png", scale: 1 });
    await fs.writeFile(path.join(QA, `${stem}.png`), new Uint8Array(await png.arrayBuffer()));
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(path.join(QA, `${stem}.layout.json`), await layout.text());
  }
  const montage = await deck.export({ format: "webp", montage: true, scale: 1 });
  await fs.writeFile(path.join(QA, "deck-montage.webp"), new Uint8Array(await montage.arrayBuffer()));
  const snapshot = await deck.inspect({ kind: "slide,textbox,shape,image,chart", maxChars: 30000 });
  await fs.writeFile(path.join(QA, "deck-inspect.ndjson"), snapshot.ndjson, "utf8");
  const pptx = await PresentationFile.exportPptx(deck);
  await pptx.save(path.join(OUT, "Presentation-zXXXXXXX.pptx"));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
