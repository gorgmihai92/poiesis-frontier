# Gate example: three conclusions

Test input for the challenge stamp, and for the entry gate of poiesis-frontier: one conclusion kept, one dropped
and one never challenged. The first two are synthetic, for the test: "topic A" and "topic B" stand for nothing, and
their numbers were not measured. Their stamps were computed for this file with the stamp format's hash and seal. The
third came out of a second pass of the lab's trend-scan run of 2026-11-17, after the challenger had answered
(`fixtures/trend-scan/challenge.published.json`, row `c1`), and nothing records a challenge of it. Only the lines
the stamp reads are kept: the sentence, the id and the verdict shown.

## Kept

### Topic A has more works each year than the year before, from 12 (2016) to 40 (2024).

- **Id:** IN-001
- **Challenge:** kept · with caveats: synthetic, for the test; one database, a short series

## Dropped

### Topic B has fewer works than any other topic in the sample, 3 of 60.

- **Id:** IN-002
- **Challenge:** dropped · synthetic, for the test; a count this small is within chance

## Not challenged

### No single source is behind the 2025 rise of synthetic biology: its share rose within China, the US, India, South Korea and Japan, beyond each country's overall growth.

- **Id:** IN-003
- **Challenge:** not challenged · found in a second pass, after the challenger had answered
