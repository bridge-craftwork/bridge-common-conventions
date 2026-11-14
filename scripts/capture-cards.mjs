// Capture what convention-card makes of each card: the card as loaded, every
// export, the values written into both ACBL PDFs, and the rows the editor
// shows. Called by scripts/capture.py; not meant to be run by hand.
//
//   node scripts/capture-cards.mjs <convention-card checkout> <cards dir> <out dir>
//
// <cards dir> holds card files (.bbsa or .json; a file may hold several
// cards). Output goes to <out dir>/<card name>/, and each card's name and
// the file it came from are printed. Everything written is sorted and free of dates, so
// two runs on the same inputs give the same bytes.
import fs from 'node:fs'
import path from 'node:path'
import { pathToFileURL } from 'node:url'
import { createRequire } from 'node:module'

const [ccArg, cardsDir, outDir] = process.argv.slice(2)
const ccDir = path.resolve(ccArg || '.')
if (!outDir) {
  console.error('usage: capture-cards.mjs <convention-card> <cards dir> <out dir>')
  process.exit(2)
}
const load = rel => import(pathToFileURL(path.join(ccDir, rel)).href)
const lib = await load('js/index.js')
const assets = await load('js/assets.js')
const catalog = await load('web/src/editor/conventionCatalog.js')
const summary = await load('web/src/editor/cardSummary.js')
const { PDFDocument, PDFTextField, PDFCheckBox, PDFRadioGroup, PDFDropdown } =
  createRequire(path.join(ccDir, 'package.json'))('pdf-lib')

assets.setAssetLoader({
  template: name => fs.readFileSync(path.join(ccDir, 'assets/templates', assets.TEMPLATE_FILES[name])),
  font: () => fs.readFileSync(path.join(ccDir, 'assets/fonts', assets.FONT_FILE)),
})

// JSON with sorted keys, so a change in key order is not a difference.
const sorted = v =>
  Array.isArray(v) ? v.map(sorted)
  : v && typeof v === 'object' ? Object.fromEntries(Object.keys(v).sort().map(k => [k, sorted(v[k])]))
  : v
const writeJson = (file, v) => fs.writeFileSync(file, JSON.stringify(sorted(v), null, 1) + '\n')
const attempt = async (what, fn) => {
  try { return await fn() } catch (err) { return { capture_error: `${what}: ${err.message}` } }
}

async function pdfValues(card, template) {
  const bytes = await lib.renderAcblPdfBytes(card, template)
  const pdf = await PDFDocument.load(bytes)
  const out = {}
  for (const f of pdf.getForm().getFields()) {
    let v
    if (f instanceof PDFTextField) v = f.getText() ?? ''
    else if (f instanceof PDFCheckBox) v = f.isChecked()
    else if (f instanceof PDFRadioGroup) v = f.getSelected() ?? ''
    else if (f instanceof PDFDropdown) v = f.getSelected()
    else continue
    if (v !== '' && v !== false && !(Array.isArray(v) && !v.length)) out[f.getName()] = v
  }
  return out
}

// The editor's rows: each catalogue entry and whether it shows as ticked,
// and each structured field with the value it shows.
function editorRows(data) {
  const entries = {}
  for (const e of catalog.CONVENTION_CATALOG) {
    entries[`${e.section}/${e.id}`] = catalog.isEntryChecked(e, data)
  }
  const values = {}
  const walk = node => {
    if (typeof node === 'string') {
      if (lib.field(node)) {
        const v = lib.readPath(data, node)
        if (v !== undefined && v !== null && v !== '' && v !== false) values[node] = v
      }
    } else if (Array.isArray(node)) node.forEach(walk)
    else if (node && typeof node === 'object') Object.values(node).forEach(walk)
  }
  walk(catalog.STRUCTURED_FIELDS)
  return {
    ticked: Object.keys(entries).filter(k => entries[k]).sort(),
    entries: Object.keys(entries).length,
    values,
    level: await_free(() => summary.cardLevel(data)),
    system: await_free(() => summary.systemOf(data)),
  }
}
const await_free = fn => { try { return fn() } catch (err) { return { capture_error: err.message } } }

const files = fs.readdirSync(cardsDir).filter(f => /\.(bbsa|json)$/.test(f)).sort()
const safe = s => String(s || 'card').trim().replace(/[^A-Za-z0-9._-]+/g, '_')
for (const file of files) {
  const base = file.replace(/\.(bbsa|json)$/, '')
  const text = fs.readFileSync(path.join(cardsDir, file), 'utf8')
  // A file may hold several cards (a BBO export, a bundle): one capture each.
  const from = file.endsWith('.bbsa') ? 'bbsa' : null
  let reads
  try {
    reads = from ? [await lib.importCard(text, { name: base, from })]
      : await lib.importCards(text, { name: base })
    if (!Array.isArray(reads)) reads = reads.cards ?? [reads]
  } catch (err) {
    reads = [await lib.importCard(text, { name: base, from })]
  }
  for (const [i, read] of reads.entries()) {
    const name = reads.length === 1 ? base : `${base}--${String(i + 1).padStart(2, '0')}-${safe(read.name)}`
    const dir = path.join(outDir, name)
    fs.mkdirSync(dir, { recursive: true })
    const data = read.card_data
    const card = { name, card_data: data }

    writeJson(path.join(dir, 'card.json'), data)
    writeJson(path.join(dir, 'import.json'), {
      format: read.format,
      implied: read.implied ?? null,
      recognised: read.recognised ?? null,
      report: read.report ?? null,
      check: await attempt('check', () => lib.checkCard(data)),
    })
    const bbsa = await attempt('bbsa', () => lib.exportBbsa(data))
    if (typeof bbsa === 'string') fs.writeFileSync(path.join(dir, 'export.bbsa'), bbsa)
    else writeJson(path.join(dir, 'export.bbsa.json'), bbsa)
    writeJson(path.join(dir, 'bbo.json'), await attempt('bbo', () => lib.exportBboCard(data, { name })))
    writeJson(path.join(dir, 'bridgodex.json'), await attempt('bridgodex', () => lib.exportBridgodexJson(data)))
    writeJson(path.join(dir, 'acbl-classic.json'), await attempt('acbl classic', () => pdfValues(card, 'classic')))
    writeJson(path.join(dir, 'acbl-new.json'), await attempt('acbl new', () => pdfValues(card, 'new')))
    writeJson(path.join(dir, 'editor.json'), await attempt('editor', () => editorRows(data)))
    console.log(`${name}\t${file}`)
  }
}
