# Meal Management: Project Specification (Draft 0.1)

Status: draft for review. Technology-neutral. Based on the 15 monthly workbooks (Sept 2025 to Nov 2026). Items marked **Confirmed** are read directly from the workbook; items marked **Open** need the owner's decision before they become requirements.

## 1. Problem statement

A shared mess manages daily meals, market purchases, bills, guest meals and monthly settlement in an Excel workbook, one file per month, with nine interconnected sheets. The balance from one month is linked into the next through an external file reference. This is fragile: files can drift in layout, links can break, and past results can change silently. The goal is an online system that keeps the familiar workbook structure and calculations, while making results stable, shareable and auditable.

## 2. Goals and non-goals

**Goals**

- Reproduce the workbook's nine-sheet workflow online, one workbook per month.
- Reproduce the workbook's calculations exactly, validated against all 15 existing months.
- Preserve historical settlements so later setting changes never alter them.
- Support Active and Archive month areas, with admin-controlled reopening.
- Import historical workbooks through a reviewable process and export months back to Excel.

**Non-goals (initial)**

- Generic expense tracking, dashboards or analytics unrelated to the workbook.
- Changing or "improving" accounting rules without explicit approval.
- Features beyond the nine sheets until the core is validated.

## 3. User roles

| Role | Capabilities | Status |
| --- | --- | --- |
| Administrator | Manage members, months and assignments; configure formulas and parameters; close and reopen months | Stated by owner |
| Monthly manager | Edit the sheets of assigned open months | Stated by owner |
| Member | Read-only access to relevant information | Stated by owner |

Open: who holds each role in practice, whether every member has a login, and whether the manager rotates monthly.

## 4. Functional requirements by sheet

| Sheet | Purpose (Confirmed) | Inputs | Outputs |
| --- | --- | --- | --- |
| Notes | Reference data: contact numbers, rent table, cylinder cost | Typed | None |
| Meals | Daily meal chart: dates down, members across, Breakfast/Lunch/Dinner per member, Guest and Extra columns, row totals, separate Khala block | Member meals (decimal), Extra | Daily totals, Khala block, guest columns pulled from Guest Chart |
| Total Meal | Per-member and overall meal totals | None | Totals derived from Meals |
| Market Costings | Date-grouped ledger of purchases (description, amount as free text, cost, cost per kg, place) | Typed | Total market cost |
| Other Cost | Non-meal costs, a total, a per-head share, and a separate block for a special-purchase split | Typed | Totals, per-head shares |
| Bills | Member by bill matrix (wifi, Khala, rent, electric), paid amounts, amount to be added to deposit | Rent, payments | Per-member balance |
| Monthly Cost Calculation | Per-member settlement | Carry-forward, partial deposits | Meal rate, expense, deposit, return or take, final balance |
| Guest Chart | Guest meals by date for six guest slots, totals, payable, paid, return, left to pay | Guest meals, payments | Payable amounts, guest totals |
| Summary | Total cost, deposits, remaining, other cost, net remains | None | Aggregates |

## 5. Business and accounting rules

As read from the November 2026 workbook, to be validated against every month during import testing.

- **R1 Meal rate (Confirmed):** total market cost divided by total meals, where total meals includes member, guest and extra meals. Open: whether including guest and extra meals is intentional.
- **R2 Member expense (Confirmed):** member meals multiplied by the meal rate.
- **R3 Deposit (Confirmed):** carry-forward from the previous month plus partial deposits plus any non-negative amount from Bills.
- **R4 Return or take (Confirmed):** deposit minus expense.
- **R5 Final balance (Confirmed):** return or take minus the per-head share of Other Cost, rounded to one decimal. The share divides by a hard-coded 7 in the workbook.
- **R6 Guest payable (Confirmed):** the larger of meals times the meal rate and meals times 40, rounded up.
- **R7 Khala block (Confirmed formula, purpose Open):** counts breakfast twice; lunch and dinner once.
- **R8 Bills (Confirmed structure, rules Open):** bill totals split per member with hard-coded per-head multipliers; rent varies by member and changed in Nov 2026 (confirmed by the owner), so rent is stored per month and a change never rewrites earlier months; negative balances do not reach Monthly Cost Calculation.
- **R9 Carry-forward (Confirmed):** each member's opening balance equals the previous month's final balance, checked across all 14 month-to-month transitions. The workbook links it from the previous file in most months; July 2026 has the same values typed in. Sept 2025 is the first month in the set.
- **R10 Rounding (Confirmed per formula):** one-decimal rounding on the final balance, round-up on guest payable; others to be catalogued during validation.

A hard-coded value is an exception when it breaks the pattern of the other months, and exceptions are ignored and not carried into the system. Found so far: Bills column C typed in Jan 2026 (-500 and -150), a -202 adjustment in Bills E2 in Feb 2026, +550 on the Other Cost total in March 2026, Bills M6 typed as 0 in Sept 2025, and in Nov 2026 a constant added in Summary plus Summary references to empty Bills cells. Hard-coded values that repeat in every month are rules, not exceptions.

## 6. Data requirements

- Members and a monthly roster (fixed at seven in all 15 months; mid-month changes Open).
- Daily meals per member as decimals, distinguishing blank from explicit zero.
- Guest slots with dates, meals, payments.
- Market purchases, other costs, bills and bill shares, deposits and payments.
- Monthly settlement results stored as immutable snapshots with the parameters used.
- Provenance for imported values: source file, sheet and cell.
- Audit trail of edits, closing and reopening.

## 7. UI and workflow requirements

- The month is the workbook; the nine sheets are tabs in workbook order.
- Active and Archive areas are separate; archived months are read-only.
- Dense, spreadsheet-like grids with sticky headers and date column, keyboard navigation, horizontal scroll, inline editing.
- Computed cells visually distinct from input cells.
- The Meals sheet keeps the original arrangement and is not reduced to a one-row-per-meal table.

## 8. Import and export requirements

- Import historical workbooks through a review step showing what will be created and any mismatches.
- Validate imported results against the workbook's stored values.
- Export a month to an Excel file that resembles the original layout.
- Open: whether exported files must keep working formulas or may contain values only.

## 9. Security requirements

- Role-based access as in section 3, enforced on the server.
- Formula and parameter configuration restricted to administrators. Every rule value (rent, per-head bill amounts, divisors, the guest rate floor, the Khala breakfast factor, rounding) is editable by an administrator, versioned, and snapshotted per month so history never changes.
- Closed months cannot be edited except through the admin reopen workflow.
- Secrets are never stored in the repository.

## 10. Open questions

1. Resolved by the data, see R9. Still open: what is the opening balance for Sept 2025, the first month?
2. How do unpaid (negative) bill balances carry into later months?
3. When an old month is reopened and its results change, do later months recalculate or keep their snapshots?
4. Is including guest and extra meals in the meal-rate divisor intentional?
5. What is the Khala block used for?
6. What are the two columns of the Notes rent table, and why does rent differ by member?
7. What happened in March 2026, Sept 2026 and Oct 2026 (zero or low market cost)?
8. What is the Goru and Khashi block in Other Cost?
9. Is the seven-member roster fixed, or can members join or leave mid-month?
10. Does every member get a login, and who is the manager?
11. Should exported Excel files keep formulas or contain values only?

## 11. Acceptance criteria

- For each of the 15 existing months, the system's meal rate, member expenses, deposits, return or take, final balances and guest payables match the workbook's stored values after rounding.
- A closed month's results do not change when any parameter changes later.
- Reopening and re-closing a month produces a new settlement version and preserves the earlier one.
- Blank and zero meal entries are stored and exported differently.
- A member cannot edit anything; a manager cannot edit a closed or unassigned month; only an administrator can change formula parameters.
- Import of a historical workbook shows a review report before anything is saved.

## 12. Proposed milestones

Proposed and pending approval; the order follows the dependency analysis.

1. Specification approved, open questions 1 to 5 answered.
2. Architecture proposal approved.
3. Shared foundations: data model, authentication, workbook navigation, accounting core with validation harness.
4. Input sheets: Notes, Market Costings, Other Cost.
5. Guest Chart, then Meals and Total Meal.
6. Bills, then Monthly Cost Calculation, then Summary.
7. Archive and reopen workflow.
8. Excel import and export, with validation against all 15 months.
