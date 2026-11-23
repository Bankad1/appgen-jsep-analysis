# Analysis data and recompute script for "Service Acceptance and Reference-Model Conformance in Generated Low-Code Applications"

This archive lets a reader recompute the manuscript's reported counts from the decision records. It does
not include the generator or the generated applications themselves; replaying an application requires
those separately.

## Files
- `data/joined_runs.csv` - one row per generated project (108): the project identifier, its task, the
  configuration and repetition, the runtime service-check decision, the model-conformance score, and
  whether that score was full.
- `data/requirement_outcomes.csv` - one row per checked requirement instance (648): the project, task,
  requirement identifier, requirement family (entity, field, association, constraint), and pass/fail/
  unassessable status.
- `recompute.py` - reads the two files and prints the headline figures (the paired 2x2 of 108 projects,
  the 85 service passes and the 44 below-full among them, the 648 requirement split, the cumulative
  mismatch thresholds, and the per-family failed/assessed counts).

## Run
`python3 recompute.py`  (Python 3.9+, standard library only; no network, no dependencies.)

## License
Data under CC BY 4.0; `recompute.py` under the MIT License (see LICENSE).
