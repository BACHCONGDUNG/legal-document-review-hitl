// Controller regression tests; the real browser/HTTP smoke check is recorded
// separately. DOM and transport doubles never replace backend acceptance data.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

class Element {
  constructor() {this.handlers = {}; this.hidden = true; this.children = [];}
  addEventListener(name, callback) {this.handlers[name] = callback;}
  querySelectorAll() {return [];}
  setAttribute() {}
  append(...children) {this.children.push(...children);}
  replaceChildren(...children) {this.children = children;}
  scrollIntoView() {}
}

async function boot(response) {
  const elements = new Map();
  const element = id => {
    if (!elements.has(id)) elements.set(id, new Element());
    return elements.get(id);
  };
  const document = {querySelector: element, querySelectorAll: () => [],
    getElementById: id => element('#' + id), createElement: () => new Element()};
  const context = {document, console, AbortController, setTimeout, clearTimeout,
    FormData: class {append() {}},
    fetch: async url => url === '/api/demo/config' ? {
      ok: true, json: async () => ({samples: [], max_file_bytes: 1000,
        max_total_bytes: 2000, max_reference_files: 5, deadline_seconds: 1})
    } : response()};
  const source = fs.readFileSync(path.join(__dirname, '../../frontend/src/pages/demo.js'), 'utf8');
  const state = await vm.runInNewContext('(async () => {' + source + '\nreturn state;})()', context);
  state.v1 = [{name: 'v1.docx', size: 1}];
  state.s = [{name: 's.docx', size: 1}];
  const previous = {comparison_id: 'previous-report', status: 'PARTIAL', results: []};
  state.report = previous;
  element('#results').hidden = false;
  return {state, previous, element,
    submit: () => element('#compare-form').handlers.submit({preventDefault() {}})};
}

for (const [label, response] of [
  ['HTTP 200 with FAILED report', async () => ({ok: true, json: async () => ({
    comparison_id: 'new-failed', status: 'FAILED', results: [], errors: [], warnings: []})})],
  ['HTTP 500 with FAILED report', async () => ({ok: false, json: async () => ({
    comparison_id: 'new-error', status: 'FAILED', results: [], errors: [{message: 'Server error'}]})})],
  ['network error', async () => {throw new TypeError('Failed to fetch');}],
  ['invalid response body', async () => ({ok: false, json: async () => {throw new SyntaxError('Invalid JSON');}})],
]) {
  test('keeps previous report after ' + label, async () => {
    const page = await boot(response);
    await page.submit();
    assert.equal(page.state.report, page.previous);
    assert.equal(page.element('#results').hidden, false);
    assert.equal(page.state.busy, false);
    assert.equal(page.element('#form-message').hidden, false);
  });
}
