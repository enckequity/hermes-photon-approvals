const {test} = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const {runInNewContext} = require('node:vm');
for (const first of ['approve', 'deny']) {
  test(first + ' is exclusive and has no network or command capability', () => {
    const nodes = Object.fromEntries(['approve', 'deny', 'status'].map(id => [id, {
      disabled: false, textContent: '', dataset: {}, addEventListener(event, callback) { this.click = callback; }
    }]));
    runInNewContext(readFileSync(__dirname + '/demo.js', 'utf8'), {
      document: {getElementById: id => nodes[id]}
    });
    nodes[first].click();
    const outcome = nodes.status.textContent;
    nodes[first === 'approve' ? 'deny' : 'approve'].click();
    assert.equal(nodes.status.textContent, outcome);
    assert.match(outcome, /No command ran/);
    assert.equal(nodes.status.dataset.choice, first);
    assert.equal(nodes.approve.disabled, true);
    assert.equal(nodes.deny.disabled, true);
  });
}
