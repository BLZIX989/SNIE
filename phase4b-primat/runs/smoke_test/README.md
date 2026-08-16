# Smoke Test (Environment Capability Check)

This file preserves the output of the pre-Phase-4B environment capability
check (PRIMAT 0.3.1 installability/executability verification), run before
any scientific protocol began. It used PRIMATConfig defaults with only
`--output_final_result --output_final_file` enabled, no other flags set,
and is **not** part of the Phase 4B scientific baseline.

Command:
```
primat --output_final_result --output_final_file capability_test_output.json --no-show_progress
```

This run is kept separate from `runs/deterministic/baseline/` per the
Phase 4B protocol's instruction not to overwrite or conflate it with the
scientific baseline.
