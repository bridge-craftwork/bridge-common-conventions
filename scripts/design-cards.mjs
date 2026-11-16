// Design a set of test cards from the pack: cards made to exercise the
// rules, not cards anybody plays.
//
//   node scripts/design-cards.mjs <convention-card checkout> <out dir> [--pack DIR]
//
// What a designed set promises, of the card settings the rule files read:
//   - every yes/no setting is on in at least one card and off in another;
//   - every option of every choice is chosen in at least one card;
//   - every number is at its default in one card, below it in another and
//     above it in a third.
// It does not try combinations: there is no end of them.
//
// What cannot be on together is taken from the pack, not guessed: the
// settings of one choice group, and the conventions that fill one function
// (two meanings of a 2♦ opening, two defences to 1NT). The first cards hold
// one member of each such group in turn. A member left out by that, because
// another group it belongs to had already spoken for the card, gets a card
// opened for it: that is the only way the set grows.
//
// Output: <out>/designed-NN.json, each a card in schema 3, and <out>.json
// beside the folder, which says what each card turns on and what the set
// covers. The convention-card checkout supplies the field list and writes
// the cards, as scripts/capture-cards.mjs uses it to read them.
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const args = process.argv.slice(2)
const packFlag = args.indexOf('--pack')
const packDir = packFlag >= 0 ? args.splice(packFlag, 2)[1] : path.join(path.dirname(fileURLToPath(import.meta.url)), '..')
const [ccArg, outDir] = args
if (!ccArg || !outDir) {
  console.error('usage: design-cards.mjs <convention-card checkout> <out dir> [--pack DIR]')
  process.exit(2)
}
const cc = path.resolve(ccArg)
const { FIELDS, field } = await import(path.join(cc, 'js/spec.js'))
const { writePath } = await import(path.join(cc, 'js/paths.js'))
const { toSchema3 } = await import(path.join(cc, 'js/schema3.js'))
const { checkCard } = await import(path.join(cc, 'js/checkCard.js'))
const PACK = JSON.parse(fs.readFileSync(path.join(cc, 'spec/pack.json'), 'utf8'))

// --- the settings the rules read ---------------------------------------
// A module reads a setting in a `param` or `card` line, and is switched on
// by the convention its `convention` line names.
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e =>
  e.isDirectory() ? walk(path.join(d, e.name)) : e.name.endsWith('.bid') ? [path.join(d, e.name)] : [])
const read = new Map() // path -> the rule files that read it
for (const file of [...walk(path.join(packDir, 'rules')), ...walk(path.join(packDir, 'conventions'))].sort()) {
  for (const m of fs.readFileSync(file, 'utf8').matchAll(/^\s+(?:param\s+\w+\s*=\s*|card\s+|convention\s+)(\S+)/gm)) {
    const p = field(m[1])?.path
    if (!p || !FIELDS[p]) continue
    read.set(p, [...(read.get(p) || []), path.relative(packDir, file)])
  }
}
const paths = [...read.keys()].sort()
const kind = p => FIELDS[p].kind
const item = (p, v) => `${p}=${v}`

// --- what cannot be on together ----------------------------------------
// A group is a list of items of which a card holds at most one.
const groups = new Map()
const group = (name, it) => { if (!groups.get(name)?.includes(it)) groups.set(name, [...(groups.get(name) || []), it]) }
for (const p of paths) {
  if (kind(p) === 'enum') for (const o of FIELDS[p].options) group(`choice ${p}`, item(p, o))
  if (kind(p) === 'bool' && FIELDS[p].choice) group(`group ${FIELDS[p].choice}`, item(p, true))
}
// Conventions that fill one function: the function's own setting, where it
// has one, already lists some as its options; the rest are switches.
const defs = { ...PACK.conventions, ...(PACK.skills || {}) }
const fills = new Map()
const fill = (fn, address) => fills.set(fn, [...(fills.get(fn) || []), address])
for (const [id, d] of Object.entries(defs)) {
  for (const fn of [d.implements ?? []].flat()) fill(fn, id)
  for (const [t, a] of Object.entries(d.treatments || {})) for (const fn of [a.implements ?? []].flat()) fill(fn, `${id}:${t}`)
}
for (const [fn, addresses] of fills) {
  const [whole, part] = fn.split('.')
  // What fills the whole function competes in each of its parts.
  const parts = part ? [fn] : [fn, ...(PACK.functions[whole]?.parts || []).map(x => `${whole}.${x}`)]
  for (const address of addresses) {
    const p = field(address)?.path
    if (!p || !read.has(p) || kind(p) !== 'bool') continue
    for (const name of parts) group(`function ${name}`, item(p, true))
  }
}
for (const [fn, f] of Object.entries(PACK.functions)) {
  const was = f.was || {}
  for (const [part, w] of Object.entries(was.setting ? { '': was } : was)) {
    const p = w.setting && field(w.setting)?.path
    if (!p || !read.has(p) || kind(p) !== 'enum') continue
    const name = `function ${part ? `${fn}.${part}` : fn}`
    // A deferring option ("conventional") leaves the call to a convention.
    for (const o of FIELDS[p].options) if (!(f.defers || []).includes(o)) group(name, item(p, o))
  }
}
const groupsOf = new Map()
for (const [name, members] of groups) for (const it of members) groupsOf.set(it, [...(groupsOf.get(it) || []), name])
const rivals = it => new Set((groupsOf.get(it) || []).flatMap(g => groups.get(g)).filter(x => x !== it))

// --- the cards ---------------------------------------------------------
const cards = [] // each: Map item -> true, plus the paths it has decided
const pathOf = it => it.slice(0, it.lastIndexOf('='))
const fits = (card, it) => !card.has(it) && !card.paths.has(pathOf(it)) && ![...rivals(it)].some(r => card.has(r))
const put = (card, it) => { card.set(it, true); card.paths.add(pathOf(it)) }
const fresh = () => { const c = new Map(); c.paths = new Set(); cards.push(c); return c }
const covered = it => cards.some(c => c.has(it))

// As many cards as the largest group has members, each group's members
// dealt round them in turn.
const grouped = [...groups.entries()].sort((a, b) => b[1].length - a[1].length || (a[0] < b[0] ? -1 : 1))
const first = Math.max(3, ...grouped.map(([, m]) => m.length))
for (let i = 0; i < first; i++) fresh()
grouped.forEach(([, members], g) => {
  cards.forEach((card, i) => {
    for (let k = 0; k < members.length; k++) {
      const it = members[(i + g + k) % members.length]
      if (card.has(it)) return
      if (fits(card, it)) return put(card, it)
    }
  })
})
// A member no card took gets a card of its own, shared with any other
// left-over that fits beside it.
const all = [...new Set(grouped.flatMap(([, m]) => m))]
const opened = []
for (const it of all) {
  if (covered(it)) continue
  const card = cards.slice(first).find(c => fits(c, it)) || (opened.push(it), fresh())
  put(card, it)
}
// Yes/no settings in no group: on in two cards of every three, so each is
// on somewhere and off somewhere, in a different pattern from its neighbour.
const free = paths.filter(p => kind(p) === 'bool' && !groupsOf.has(item(p, true)))
free.forEach((p, n) => cards.forEach((card, i) => { if ((i + n) % 3 !== 0) put(card, item(p, true)) }))
// A setting that needs another has it.
for (const card of cards) for (const it of [...card.keys()]) {
  const need = FIELDS[pathOf(it)].requires
  if (need && FIELDS[need]?.kind === 'bool' && !card.has(item(need, true)) && fits(card, item(need, true))) put(card, item(need, true))
}
// Numbers: the default, three below it and two above it, by card, the same
// shift for every number in a card so that a range keeps its order.
const SHIFT = [0, -3, 2]
const numbers = paths.filter(p => kind(p) === 'int' && FIELDS[p].default !== undefined)
const clip = (p, v) => Math.min(FIELDS[p].max ?? v, Math.max(FIELDS[p].min ?? v, v))

// --- written out -------------------------------------------------------
fs.mkdirSync(outDir, { recursive: true })
for (const f of fs.readdirSync(outDir)) if (/^designed-\d+\.json$/.test(f)) fs.rmSync(path.join(outDir, f))
const design = { cards: {}, settings: paths.length, opened_for: opened }
const problems = []
cards.forEach((card, i) => {
  const name = `designed-${String(i + 1).padStart(2, '0')}`
  const data = { schema_version: '2.0', metadata: { name, partner_names: 'A designed test card' } }
  const on = []
  for (const it of [...card.keys()].sort()) {
    const p = pathOf(it), v = it.slice(p.length + 1)
    writePath(data, p, kind(p) === 'bool' ? true : v)
    on.push(kind(p) === 'bool' ? p : it)
  }
  // Off is said, not left unset, so a default cannot turn it on.
  for (const p of paths) if (kind(p) === 'bool' && !card.has(item(p, true))) writePath(data, p, false)
  const shift = SHIFT[i % SHIFT.length]
  for (const p of numbers) writePath(data, p, clip(p, FIELDS[p].default + shift))
  const saved = toSchema3(data)
  const { diagnostics = [] } = checkCard(saved)
  for (const d of diagnostics.filter(d => d.severity === 'error')) problems.push(`${name}: ${d.message}`)
  fs.writeFileSync(path.join(outDir, `${name}.json`), JSON.stringify({ name, card_data: saved }, null, 1) + '\n')
  design.cards[name] = { on, numbers: shift === 0 ? 'default' : `${shift > 0 ? '+' : ''}${shift}` }
})
// What the set covers, checked from the cards as designed.
const onSomewhere = p => cards.some(c => c.has(item(p, true))), offSomewhere = p => cards.some(c => !c.has(item(p, true)))
const bools = paths.filter(p => kind(p) === 'bool'), choices = paths.filter(p => kind(p) === 'enum')
const options = choices.flatMap(p => FIELDS[p].options.map(o => item(p, o)))
design.covers = {
  yes_no: bools.length, on_somewhere: bools.filter(onSomewhere).length, off_somewhere: bools.filter(offSomewhere).length,
  choices: choices.length, options: options.length, options_chosen: options.filter(covered).length,
  numbers: numbers.length, not_varied: paths.filter(p => !['bool', 'enum'].includes(kind(p)) && !numbers.includes(p)),
}
design.not_covered = [...bools.filter(p => !onSomewhere(p)).map(p => `${p} is never on`), ...bools.filter(p => !offSomewhere(p)).map(p => `${p} is never off`), ...options.filter(o => !covered(o)).map(o => `${o} is never chosen`)]
design.groups = Object.fromEntries([...groups].filter(([, m]) => m.length > 1).map(([n, m]) => [n, m]))
fs.writeFileSync(`${path.resolve(outDir)}.json`, JSON.stringify(design, null, 1) + '\n')
const c = design.covers
console.log(`${cards.length} cards (${first} dealt, ${cards.length - first} opened for a left-over) from ${paths.length} settings the rules read`)
console.log(`yes/no: ${c.on_somewhere} of ${c.yes_no} on somewhere, ${c.off_somewhere} off somewhere; options: ${c.options_chosen} of ${c.options} chosen; numbers varied: ${c.numbers}; not varied: ${c.not_varied.length}`)
for (const line of [...design.not_covered, ...problems]) console.log('  ' + line)
if (design.not_covered.length || problems.length) process.exitCode = 1
