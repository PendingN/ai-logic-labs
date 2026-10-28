# AI Logic Labs

Completed lecture 9 and 10 homework notebooks for Introduction to Artificial Intelligence (503043).

| Notebook | Contents |
| --- | --- |
| [Lecture 9](52400066-lec09-PropositionalLogic-HW.ipynb) | Graphviz knowledge-base diagram, Forward Chaining, and the inference trace for query `Q` |
| [Lecture 10](52400066-lec10-FirstOrderLogic-HW.ipynb) | Six English translations and six First-Order Logic translations, with explicit quantifier scope |

The notebooks retain the assignment prompts, cell metadata, and prescribed function signature. Original prompts and reference images belong to their respective authors. No license is asserted over those materials.

## Run

Python 3.10+ and the [Graphviz system executable](https://graphviz.org/download/) are required. Install Graphviz and make sure `dot -V` works before running lecture 9; the Python package alone does not install it.

```sh
python -m pip install -r requirements.txt
python -m ipykernel install --user --name python3
python -c "from nbclient.cli import main; main()" 52400066-lec09-PropositionalLogic-HW.ipynb --timeout=60
python test_logic_labs.py
```

You can also open the notebooks in VS Code or Jupyter and run all cells. Lecture 10 contains Markdown answers and requires no execution.

## Results and conventions

Lecture 9 represents each clause as `(premises, conclusion)` and each fact with an empty premise tuple. The diagram uses an AND node for each rule with multiple premises. Forward Chaining uses a FIFO agenda, processes each proposition once, prints it on its own line, and stops when it reaches the query.

For the provided knowledge base, the trace is shown compactly below (the notebook prints one proposition per line):

```text
A B D C G E F H I J K L M N O P Q
Entails Q: True
```

Lecture 10 explains the scope of "some student", both a time-abstracted and an explicit temporal reading of "eventually", the direction of trust, the company constant, and distinct reviewers in "at least two other scientists".

## Validation

`python test_logic_labs.py` checks the 17 clauses, the exact inference trace, query stopping, missing premises, repeated facts/premises, alternative rules, cycles, and seeded random knowledge bases against an independent closure calculation. It also checks notebook validity, stored execution outputs, and completed answer cells. If the original templates are present in the parent folder, it additionally verifies that only designated answer cells changed.

Lecture 9 includes the rendered graph and actual kernel outputs. Lecture 10 was manually checked for quantifier scope and implication direction; the local tests do not prove its natural-language translations. The teacher's grading system was not available.
