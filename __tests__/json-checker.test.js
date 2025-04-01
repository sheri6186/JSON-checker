const { checkJson } = require('../json-checker');

test('valid JSON', () => {
    expect(checkJson('{"key": "value"}')).toBe(true);
});

test('invalid JSON', () => {
    expect(checkJson('{"key": "value"')).toBe(false);
});

test('empty string', () => {
    expect(checkJson('')).toBe(false);
});