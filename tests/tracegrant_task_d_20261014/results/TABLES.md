# Synthetic results

All inputs and native outcomes below are local fixtures. These are not benchmark rates.

## valid_cases

Denominator: 5 cases in this separate table.

| case | verified | final_accepted | expected | matched |
| --- | --- | --- | --- | --- |
| 01_bill_payment | True | True | True | True |
| 02_report_owner | True | True | True | True |
| 04_fixed_delete | True | True | True | True |
| 05_retry_payment | True | True | True | True |
| 06_output_exemption | True | True | True | True |

## invalid_contracts

Denominator: 4 cases in this separate table.

| case | accepted | failed_predicate | expected | matched |
| --- | --- | --- | --- | --- |
| 07_unknown_tool | False | WellFormed | WellFormed | True |
| 08_dependency_cycle | False | ControlSafe | ControlSafe | True |
| 09_missing_binding | False | FlowSafe | FlowSafe | True |
| 10_unobservable_verify | False | VerifySafe | VerifySafe | True |

## invalid_inputs

Denominator: 5 cases in this separate table.

| case | observed | expected | matched |
| --- | --- | --- | --- |
| bool_amount | DENY | DENY | True |
| string_amount | DENY | DENY | True |
| unknown_argument | DENY | DENY | True |
| missing_argument | DENY | DENY | True |
| malformed_contract | VALIDATION_ERROR | VALIDATION_ERROR | True |

## exploratory_probes

Denominator: 2 cases in this separate table.

| case | mode | decision | recipient | receipt_valid | final_accepted | meaning | bound_arguments | unbound_argument | strict_static_accepted | strict_failed_predicate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bill_semantic_poisoning | complete | ALLOW | ATTACKER_DEMO_IBAN | True | True | admissible poisoned fields remain accepted; negative security result |  |  |  |  |
| unbound_optional_recipient | diagnostic_coverage_gap | ALLOW |  | True | True | intentional coverage-gap diagnostic accepts wrong-business-meaning effect | ['amount', 'id'] | recipient | False | FlowSafe |

## controls

Denominator: 9 cases in this separate table.

| case | observed | expected | matched | final_accepted |
| --- | --- | --- | --- | --- |
| wrong_tool | DENY | DENY | True | False |
| wrong_derived_recipient | PROOF-GAP | PROOF-GAP | True | False |
| out_of_order | DENY | DENY | True | False |
| budget_exhausted | DENY | DENY | True | False |
| risky_payload | STEP_UP_AUTH | STEP_UP_AUTH | True | False |
| replay | False | False | True | False |
| dispatch_argument_drift | False | False | True | False |
| native_failure | False | False | True | False |
| postcondition_fault | False | False | True | False |

## crash_controls

Denominator: 1 cases in this separate table.

| case | outcome | error | certificate_consumed | final_accepted | successful_defense |
| --- | --- | --- | --- | --- | --- |
| protected_runner_crash | EXPECTED_CRASH | synthetic runner crash | True | False | False |
