# Protocol B: RA_Consensus (frozen 2026-10-22, before any real-data run)

**Status:** code tested on synthetic data only. No real-data result exists for RA_Consensus yet.

## The idea (hypothesis)
MI was among the worst selectors on CIC but the best on the UNSW holdout; ANOVA was the reverse; RFE-RF was never far from the best.
RA_Consensus keeps a feature only if it ranks well under three different criteria (MI, ANOVA F, random-forest importance), then removes near-duplicates.
Details: `selector_rank_consensus.py`. Variants: RA_noRF, RA_mean, RA_noRed.

## Rules (set now, not to be changed after seeing results)
1. **Development data only:** (a) dev split of the UNSW *training* file (70/30, duplicate-grouped, fixed seed), (b) CIC grouped 10-fold CV, 1 repeat.
2. **The official UNSW test file is not touched** until the dev criteria pass.
3. **Dev criteria** (`check_criteria.py`; all three must pass):
   - C1: worst-case gap of RA_Consensus (over the two dev sets, accuracy points to the best selector) <= RFE-RF's worst-case gap + 0.2
   - C2: gap <= 1.0 point on each dev set
   - C3: median selection time <= 3.0 s
4. **If any criterion fails:** stop, report a negative result, do not tune. (One redesign would need a new protocol file and a new dev split seed.)
5. **If all pass:** one test run on the official UNSW test file (`run_final_test.sh`, refuses to start without the PASS marker). Declared success: pooled accuracy not more than 0.2 points below RFE-RF and selection time under half of RFE-RF's. Report the result either way, with all baselines.
6. Selection hyperparameters (100 trees, depth 12, max-correlation penalty, geometric mean) are fixed and were chosen without looking at real data.

## Commands
See `run_dev.sh`. After it finishes, `check_criteria.py` prints PASS/FAIL per criterion.
