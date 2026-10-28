"""Run with python test_logic_labs.py; requires the notebook dependencies."""
import contextlib
import copy
import io
import json
import random
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parent
NAMES = ['lec09-PropositionalLogic-HW', 'lec10-FirstOrderLogic-HW']
notebooks = []
for name, changed in zip(NAMES, [{5, 8, 11}, {4, 7}]):
    path = ROOT / f'52400066-{name}.ipynb'
    notebook = json.loads(path.read_text(encoding='utf-8'))
    nbformat.validate(nbformat.read(path, as_version=4))
    notebooks.append(notebook)
    original_path = ROOT.parent / f'{name}.ipynb'
    if original_path.exists():
        original = json.loads(original_path.read_text(encoding='utf-8'))
        assert notebook['metadata'] == original['metadata']
        assert len(notebook['cells']) == len(original['cells'])
        for i, (before, after) in enumerate(zip(original['cells'], notebook['cells'])):
            assert before['metadata'] == after['metadata'], i
            assert before['cell_type'] == after['cell_type'], i
            if i not in changed:
                assert before == after, i
    for i in changed:
        source = ''.join(notebook['cells'][i]['source'])
        assert source.strip() and 'YOUR CODE HERE' not in source
        assert 'YOUR ANSWER HERE' not in source and 'YOUR ANDSWER HERE' not in source

namespace = {}
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    for i in [5, 8, 11]:
        exec(''.join(notebooks[0]['cells'][i]['source']), namespace)

expected_kb = [
    (('A', 'B'), 'C'), (('A',), 'D'), (('C', 'D'), 'E'),
    (('E',), 'F'), (('B',), 'G'), (('F', 'G'), 'H'),
    (('H',), 'I'), (('I', 'D'), 'J'), (('J',), 'K'),
    (('K', 'A'), 'L'), (('L',), 'M'), (('M', 'G'), 'N'),
    (('N',), 'O'), (('O', 'C'), 'P'), (('P',), 'Q'),
    ((), 'A'), ((), 'B'),
]
assert namespace['KB'] == expected_kb
assert namespace['entails_q'] is True
graph = namespace['graph'].source
assert graph.count('shape=diamond') == 7
for number, (premises, conclusion) in enumerate(expected_kb, 1):
    if len(premises) > 1:
        for premise in premises:
            assert f'{premise} -> rule_{number}' in graph
        assert f'rule_{number} -> {conclusion}' in graph
    elif premises:
        assert f'{premises[0]} -> {conclusion}' in graph

def run(kb, query='Q'):
    before = copy.deepcopy(kb)
    with contextlib.redirect_stdout(io.StringIO()) as output:
        result = namespace['PL_FC_ENTAILS'](kb, query)
    assert kb == before, 'Input knowledge base was mutated'
    trace = output.getvalue().splitlines()
    assert len(trace) == len(set(trace)), trace
    return result, trace


expected_trace = 'A B D C G E F H I J K L M N O P Q'.split()
assert run(expected_kb) == (True, expected_trace)
assert run(expected_kb, 'A') == (True, ['A'])
assert run(expected_kb, 'Z') == (False, expected_trace)
assert run([], 'A') == (False, [])
assert run([(('A', 'B'), 'Q'), ((), 'A')]) == (False, ['A'])
assert run([(('A', 'A'), 'Q'), ((), 'A'), ((), 'A')]) == (True, ['A', 'Q'])
assert run([(('A',), 'B'), (('B',), 'A')], 'B') == (False, [])
assert run([(('A',), 'B'), (('B',), 'A'), ((), 'A')], 'Z') == (False, ['A', 'B'])
assert run([(('A',), 'Q'), (('B',), 'Q'), ((), 'B')]) == (True, ['B', 'Q'])

# Fixed-point closure is an independent oracle; it has no agenda or counters.
rng = random.Random(9)
symbols = list('ABCDEF')
for _ in range(200):
    kb = [(tuple(rng.choices(symbols, k=rng.randrange(4))), rng.choice(symbols))
          for _ in range(rng.randrange(20))]
    closure = {head for premises, head in kb if not premises}
    while True:
        expanded = closure | {head for premises, head in kb if set(premises) <= closure}
        if expanded == closure:
            break
        closure = expanded
    for query in symbols + ['Z']:
        result, trace = run(kb, query)
        assert result == (query in closure), (kb, query)
        assert set(trace) <= closure
        if result:
            assert trace[-1] == query
        else:
            assert set(trace) == closure

cells = notebooks[0]['cells']
assert any('image/png' in output.get('data', {}) for output in cells[5]['outputs'])
assert ''.join(output.get('text', '') if isinstance(output.get('text', ''), str)
               else ''.join(output['text']) for output in cells[11]['outputs']) == (
                   '\n'.join(expected_trace) + '\nEntails Q: True\n')
for i in [5, 8, 11]:
    assert cells[i]['execution_count'] is not None
    assert not any(output['output_type'] == 'error' for output in cells[i]['outputs'])
for i in [4, 7]:
    source = ''.join(notebooks[1]['cells'][i]['source'])
    assert all(f'{number}. ' in source for number in range(1, 7))

print('PASS: notebook structure, Graphviz graph, exact Q trace, edge cases, and 1,400 random entailment checks.')
print('PASS: all 12 First-Order Logic answer items are present; semantic review is manual.')
