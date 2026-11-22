#!/usr/bin/env python3
"""What a sample of a given size can detect. Run with `python3 -I`.

  power.py detect --n 8                 two groups of 8 and one measure: the smallest difference a test would find
  power.py detect --n 12 --paired       12 people who each try both variants
  power.py power  --n 15 --d 0.5        the chance that a difference of that size comes out significant
  power.py n      --d 0.4 --power 0.9   how many people per group a difference of that size takes
  power.py count  --n 8 --at-least 3 --if 0.2 --if 0.6
                                        a criterion on a count ("at least 3 of 8"): how often each true rate meets it
  power.py count  --n 20 --null 0.65 --if 0.8
                                        a count tested against a known rate
  power.py two    --n 8 --p1 0.2 --p2 0.8
                                        two groups and a yes/no outcome
  power.py see    --n 5 --p 0.31        the chance of seeing a thing at least once among n people
  power.py rate   --n 8 --k 3           3 of 8 showed it: the range the true rate could be in

A difference between two variants is given as d: the difference between the two averages divided by the standard
deviation of the measure. With --sd the script also prints it in the measure's own units. A paired comparison
(--paired) uses dz, the average of the per-person differences divided by their standard deviation.

The numbers are exact for what they assume and say nothing else. They assume people who answer independently of
each other, and for `detect`, `power` and `n` a measure that is roughly normal with the same spread in both
groups. The script does not know which effect is plausible: that comes from earlier data or from a source.
"""
from __future__ import annotations

import argparse
import math
import sys

STEPS = 1200  # intervals of Simpson's rule; even


def phi(x: float) -> float:
    """The standard normal distribution function."""
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def _w_density(w: float, df: float) -> float:
    """Density of W = sqrt(V/df), where V is chi-square with df degrees of freedom."""
    if w <= 0.0:
        return math.sqrt(2.0 / math.pi) if df == 1 else 0.0
    log_g = (df / 2.0) * math.log(df) + (df - 1.0) * math.log(w) - df * w * w / 2.0
    log_g += (1.0 - df / 2.0) * math.log(2.0) - math.lgamma(df / 2.0)
    return math.exp(log_g)


def t_cdf(t: float, df: float, delta: float = 0.0) -> float:
    """P(T <= t) for Student's t with df degrees of freedom and noncentrality delta.

    T = (Z + delta) / W with Z standard normal and W as above, so P(T <= t) is the average of
    phi(t * W - delta) over W. The average is taken by Simpson's rule over twelve standard deviations of W.
    """
    half = 12.0 / math.sqrt(2.0 * df)
    lo, hi = max(0.0, 1.0 - half), 1.0 + half
    if df < 3:  # W has a heavy left part when df is small: integrate it from 0
        lo, hi = 0.0, 1.0 + 40.0 / math.sqrt(df)
    cuts = {lo, hi}
    if t != 0.0:  # phi(t*w - delta) turns from 0 to 1 within a few 1/|t| of w = delta/t: integrate that part finely
        w0, width = delta / t, 12.0 / abs(t)
        cuts.update(min(hi, max(lo, x)) for x in (w0 - width, w0 + width))
    edges = sorted(cuts)
    total = 0.0
    for a, b in zip(edges, edges[1:]):
        if b <= a:
            continue
        h = (b - a) / STEPS
        part = 0.0
        for i in range(STEPS + 1):
            w = a + i * h
            weight = 1 if i in (0, STEPS) else (4 if i % 2 else 2)
            part += weight * phi(t * w - delta) * _w_density(w, df)
        total += part * h / 3.0
    return min(1.0, max(0.0, total))


def t_crit(df: float, alpha: float = 0.05, two_sided: bool = True) -> float:
    """The value a t statistic has to pass to be significant at alpha."""
    target = 1.0 - (alpha / 2.0 if two_sided else alpha)
    lo, hi = 0.0, 10.0
    while t_cdf(hi, df) < target and hi < 1e6:
        hi *= 4.0
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if t_cdf(mid, df) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def _df_and_scale(n1: int, n2: int | None, paired: bool) -> tuple[int, float]:
    """Degrees of freedom, and the factor that turns an effect size into the noncentrality."""
    n2 = n1 if n2 is None else n2
    df = n1 - 1 if paired else n1 + n2 - 2
    if df < 1:
        raise ValueError("a comparison needs at least 2 pairs, or 3 people across the two groups")
    return df, math.sqrt(n1) if paired else math.sqrt(n1 * n2 / (n1 + n2))


def power_means(d: float, n1: int, n2: int | None = None, alpha: float = 0.05, paired: bool = False,
                two_sided: bool = True, crit: float | None = None) -> float:
    """The chance that a t test comes out significant when the true effect is d."""
    df, scale = _df_and_scale(n1, n2, paired)
    crit = t_crit(df, alpha, two_sided) if crit is None else crit
    delta = d * scale
    power = 1.0 - t_cdf(crit, df, delta)
    if two_sided:
        power += t_cdf(-crit, df, delta)
    return power


def critical_d(n1: int, n2: int | None = None, alpha: float = 0.05, paired: bool = False,
               two_sided: bool = True) -> float:
    """The smallest observed effect that would be significant at this sample size."""
    df, scale = _df_and_scale(n1, n2, paired)
    return t_crit(df, alpha, two_sided) / scale


def detectable_d(power: float, n1: int, n2: int | None = None, alpha: float = 0.05, paired: bool = False,
                 two_sided: bool = True) -> float:
    """The true effect the design finds with the given chance (a sensitivity analysis)."""
    df, _ = _df_and_scale(n1, n2, paired)
    crit = t_crit(df, alpha, two_sided)
    lo, hi = 0.0, 1.0
    while power_means(hi, n1, n2, alpha, paired, two_sided, crit) < power and hi < 1e4:
        hi *= 2.0
    for _ in range(50):
        mid = (lo + hi) / 2.0
        if power_means(mid, n1, n2, alpha, paired, two_sided, crit) < power:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def n_needed(d: float, power: float = 0.8, alpha: float = 0.05, paired: bool = False,
             two_sided: bool = True, limit: int = 1_000_000) -> int | None:
    """The smallest number per group (or of pairs) that reaches the power for a true effect d."""
    if d <= 0:
        raise ValueError("the effect has to be above zero")
    lo, hi = 2, 4
    while power_means(d, hi, None, alpha, paired, two_sided) < power:
        lo, hi = hi, hi * 2
        if hi > limit:
            return None
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if power_means(d, mid, None, alpha, paired, two_sided) < power:
            lo = mid
        else:
            hi = mid
    if power_means(d, lo, None, alpha, paired, two_sided) >= power:
        return lo
    return hi


def binom_pmf(k: int, n: int, p: float) -> float:
    return math.comb(n, k) * p**k * (1.0 - p) ** (n - k)


def binom_at_least(k: int, n: int, p: float) -> float:
    """P(X >= k) for X binomial(n, p)."""
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    return min(1.0, sum(binom_pmf(i, n, p) for i in range(k, n + 1)))


def binom_at_most(k: int, n: int, p: float) -> float:
    """P(X <= k) for X binomial(n, p)."""
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    return min(1.0, sum(binom_pmf(i, n, p) for i in range(0, k + 1)))


def critical_count(n: int, null: float, alpha: float = 0.05, less: bool = False) -> tuple[int | None, float]:
    """The count that rejects a known rate `null`, one-sided, and the alpha actually reached.

    Upward (the default): the smallest k with P(X >= k | null) <= alpha. With less=True: the largest k with
    P(X <= k | null) <= alpha. None when no count rejects.
    """
    if less:
        for k in range(n, -1, -1):
            tail = binom_at_most(k, n, null)
            if tail <= alpha:
                return k, tail
        return None, 0.0
    for k in range(0, n + 1):
        tail = binom_at_least(k, n, null)
        if tail <= alpha:
            return k, tail
    return None, 0.0


def _hyper(x1: int, n1: int, n2: int, m: int) -> float:
    """P(x1 successes in group 1 | m successes in all), under no difference."""
    return math.comb(n1, x1) * math.comb(n2, m - x1) / math.comb(n1 + n2, m)


def fisher_p(x1: int, x2: int, n1: int, n2: int) -> float:
    """Two-sided p of Fisher's exact test: the tables no more likely than the one seen, summed."""
    m = x1 + x2
    seen = _hyper(x1, n1, n2, m)
    total = 0.0
    for y in range(max(0, m - n2), min(n1, m) + 1):
        prob = _hyper(y, n1, n2, m)
        if prob <= seen * (1.0 + 1e-9):
            total += prob
    return min(1.0, total)


def fisher_significant(n1: int, n2: int, alpha: float = 0.05) -> list[tuple[int, int]]:
    """Every outcome (x1, x2) that Fisher's exact test calls significant."""
    return [(a, b) for a in range(n1 + 1) for b in range(n2 + 1) if fisher_p(a, b, n1, n2) <= alpha]


def power_two(p1: float, p2: float, n1: int, n2: int | None = None, alpha: float = 0.05) -> float:
    """The chance that Fisher's exact test comes out significant when the true rates are p1 and p2."""
    n2 = n1 if n2 is None else n2
    return min(1.0, sum(binom_pmf(a, n1, p1) * binom_pmf(b, n2, p2) for a, b in fisher_significant(n1, n2, alpha)))


def seen_at_least(n: int, p: float, times: int = 1) -> float:
    """The chance that a thing each person shows with probability p turns up at least `times` among n people."""
    return binom_at_least(times, n, p)


def rate_to_see(n: int, chance: float, times: int = 1) -> float:
    """The rate at which n people would show the thing at least `times` with the given chance."""
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if seen_at_least(n, mid, times) < chance:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def rate_interval(k: int, n: int, level: float = 0.95) -> tuple[float, float]:
    """The exact range of true rates compatible with k of n at the given level.

    With k = 0 or k = n the range is one-sided, which for k = 0 gives 1 - (1 - level)^(1/n).
    """
    if not 0 <= k <= n or n < 1:
        raise ValueError("k has to be between 0 and n")
    one_sided = k in (0, n)
    tail = (1.0 - level) if one_sided else (1.0 - level) / 2.0

    def solve(too_low) -> float:
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2.0
            if too_low(mid):
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2.0

    lower = 0.0 if k == 0 else solve(lambda p: binom_at_least(k, n, p) < tail)
    upper = 1.0 if k == n else solve(lambda p: binom_at_most(k, n, p) > tail)
    return lower, upper


def pct(x: float) -> str:
    return f"{100.0 * x:.1f}%"


def _size(d: float) -> str:
    """Cohen's conventional labels, as the G*Power manual gives them (0.2, 0.5, 0.8)."""
    if d < 0.2:
        return "below what is conventionally called small (0.2)"
    if d < 0.5:
        return "conventionally small to medium (0.2 to 0.5)"
    if d < 0.8:
        return "conventionally medium to large (0.5 to 0.8)"
    return "above what is conventionally called large (0.8)"


def _design(a: argparse.Namespace) -> str:
    sides = "two-sided" if not a.one_sided else "one-sided"
    if a.paired:
        return f"{a.n} people who each try both variants (paired t test, {sides}, alpha {a.alpha:g})"
    n2 = a.n2 or a.n
    return f"two groups of {a.n} and {n2} (independent t test, {sides}, alpha {a.alpha:g})"


def _units(d: float, sd: float | None) -> str:
    return f" = {d * sd:.2f} in the measure's units (sd {sd:g})" if sd else ""


def cmd_detect(a: argparse.Namespace) -> int:
    two_sided = not a.one_sided
    name = "dz" if a.paired else "d"
    print(_design(a))
    crit = critical_d(a.n, a.n2, a.alpha, a.paired, two_sided)
    print(f"Smallest observed difference that would be significant: {name} = {crit:.2f}{_units(crit, a.sd)}")
    levels = a.power or [0.8, 0.9, 0.95]
    print("True difference the design would find:")
    for level in levels:
        d = detectable_d(level, a.n, a.n2, a.alpha, a.paired, two_sided)
        print(f"  {level:.0%} of the time: {name} = {d:.2f}{_units(d, a.sd)}")
    d80 = detectable_d(levels[0], a.n, a.n2, a.alpha, a.paired, two_sided)
    print(f"Reading: {name} = {d80:.2f} is {_size(d80)}.")
    print("A smaller true difference would usually be missed, and a missed difference is not evidence of no difference.")
    return 0


def cmd_power(a: argparse.Namespace) -> int:
    two_sided = not a.one_sided
    name = "dz" if a.paired else "d"
    print(_design(a))
    p = power_means(a.d, a.n, a.n2, a.alpha, a.paired, two_sided)
    print(f"Power for a true difference of {name} = {a.d:g}{_units(a.d, a.sd)}: {p:.6f}")
    print(f"Reading: such a difference would come out significant about {round(100 * p)} times in 100.")
    return 0


def cmd_n(a: argparse.Namespace) -> int:
    two_sided = not a.one_sided
    name = "dz" if a.paired else "d"
    n = n_needed(a.d, a.power, a.alpha, a.paired, two_sided)
    sides = "two-sided" if two_sided else "one-sided"
    kind = "paired t test" if a.paired else "independent t test"
    if n is None:
        print(f"More than a million per group would be needed for {name} = {a.d:g}.")
        return 0
    reached = power_means(a.d, n, None, a.alpha, a.paired, two_sided)
    unit = "pairs" if a.paired else "people in each group"
    print(f"{kind}, {sides}, alpha {a.alpha:g}, true difference {name} = {a.d:g}{_units(a.d, a.sd)}")
    print(f"For power {a.power:g}: {n} {unit} (power reached: {reached:.4f})")
    return 0


def cmd_count(a: argparse.Namespace) -> int:
    rates = a.rate or [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    if a.null is None and a.at_least is None:
        print("Give --at-least K (a criterion on the count) or --null P (a known rate to test against).", file=sys.stderr)
        return 2
    if a.null is not None:
        k, reached = critical_count(a.n, a.null, a.alpha, a.less)
        way = "at most" if a.less else "at least"
        print(f"{a.n} people, a known rate of {a.null:g}, one-sided exact binomial test, alpha {a.alpha:g}")
        if k is None:
            print("No count rejects the known rate at this alpha: the group is too small for this test.")
            return 0
        print(f"Critical count: {way} {k} of {a.n} (alpha actually reached: {reached:.6f})")
        for p in rates:
            power = binom_at_most(k, a.n, p) if a.less else binom_at_least(k, a.n, p)
            print(f"  if the true rate is {p:g}: power {power:.6f}")
        return 0
    print(f"Criterion: at least {a.at_least} of {a.n}")
    for p in rates:
        met = binom_at_least(a.at_least, a.n, p)
        print(f"  if the true rate is {p:g}: met {pct(met)} of the time, not met {pct(1.0 - met)}")
    print("Reading: the criterion separates two true rates only if it is met often at one and seldom at the other.")
    return 0


def cmd_two(a: argparse.Namespace) -> int:
    n2 = a.n2 or a.n
    if max(a.n, n2) > 80:
        print("Groups above 80 are not computed here: the exact sum gets slow, and at that size a study is no "
              "longer the small one this script is for.", file=sys.stderr)
        return 2
    print(f"two groups of {a.n} and {n2}, a yes/no outcome (Fisher's exact test, two-sided, alpha {a.alpha:g})")
    sig = fisher_significant(a.n, n2, a.alpha)
    if not sig:
        print("No outcome is significant at this alpha: the groups are too small for this test.")
    else:
        closest = min(sig, key=lambda t: (abs(t[0] / a.n - t[1] / n2), t))
        print(f"Least extreme outcome that is significant: {closest[0]} of {a.n} against {closest[1]} of {n2}")
    if a.p1 is not None and a.p2 is not None:
        power = power_two(a.p1, a.p2, a.n, n2, a.alpha)
        print(f"Power when the true rates are {a.p1:g} and {a.p2:g}: {power:.4f}")
        print(f"Reading: such a difference would come out significant about {round(100 * power)} times in 100.")
    return 0


def cmd_see(a: argparse.Namespace) -> int:
    what = "at least once" if a.times == 1 else f"at least {a.times} times"
    print(f"{a.n} people, {what}")
    for p in a.p or [0.05, 0.1, 0.2, 0.31, 0.5]:
        print(f"  a thing each person shows with probability {p:g}: seen {pct(seen_at_least(a.n, p, a.times))} of the time")
    for chance in (0.8, 0.95):
        print(f"  seen {chance:.0%} of the time only if at least {pct(rate_to_see(a.n, chance, a.times))} of people show it")
    print("Reading: rarer things will usually not appear in a group this size. Not seeing one says little.")
    return 0


def cmd_rate(a: argparse.Namespace) -> int:
    lower, upper = rate_interval(a.k, a.n, a.level)
    print(f"{a.k} of {a.n} ({pct(a.k / a.n)})")
    if a.k == 0:
        print(f"The true rate could be as high as {pct(upper)} ({a.level:.0%} level, exact). Rule of three: 3/{a.n} = {pct(min(1.0, 3.0 / a.n))}")
        print("Reading: nobody showing it does not mean it does not happen.")
    elif a.k == a.n:
        print(f"The true rate could be as low as {pct(lower)} ({a.level:.0%} level, exact).")
    else:
        print(f"The true rate is between {pct(lower)} and {pct(upper)} ({a.level:.0%} level, exact).")
    return 0


def _means_options(p: argparse.ArgumentParser, n_required: bool = True) -> None:
    if n_required:
        p.add_argument("--n", type=int, required=True, help="people per group, or the number of pairs with --paired")
        p.add_argument("--n2", type=int, help="size of the second group when it differs")
    p.add_argument("--paired", action="store_true", help="each person tries both variants")
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--one-sided", action="store_true", help="the direction was fixed in advance")
    p.add_argument("--sd", type=float, help="standard deviation of the measure, to print differences in its units")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("detect", help="the smallest difference a comparison of this size would find")
    _means_options(p)
    p.add_argument("--power", type=float, action="append", help="a power level; repeat it (default 0.8, 0.9, 0.95)")
    p.set_defaults(run=cmd_detect)

    p = sub.add_parser("power", help="the chance of finding a difference of a given size")
    _means_options(p)
    p.add_argument("--d", type=float, required=True, help="the true difference, in standard deviations")
    p.set_defaults(run=cmd_power)

    p = sub.add_parser("n", help="how many people a difference of a given size takes")
    _means_options(p, n_required=False)
    p.add_argument("--d", type=float, required=True, help="the true difference, in standard deviations")
    p.add_argument("--power", type=float, default=0.8)
    p.set_defaults(run=cmd_n)

    p = sub.add_parser("count", help="a criterion or a test on a count of people")
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--at-least", type=int, help="the criterion: at least this many of n")
    p.add_argument("--null", type=float, help="a known rate to test the count against")
    p.add_argument("--less", action="store_true", help="with --null: test for fewer, not more")
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--if", dest="rate", type=float, action="append", help="a true rate to try; repeat it")
    p.set_defaults(run=cmd_count)

    p = sub.add_parser("two", help="two groups and a yes/no outcome")
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--n2", type=int)
    p.add_argument("--p1", type=float, help="true rate in the first group")
    p.add_argument("--p2", type=float, help="true rate in the second group")
    p.add_argument("--alpha", type=float, default=0.05)
    p.set_defaults(run=cmd_two)

    p = sub.add_parser("see", help="the chance of seeing a thing at least once among n people")
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--p", type=float, action="append", help="how often one person shows it; repeat it")
    p.add_argument("--times", type=int, default=1, help="at least this many times (default 1)")
    p.set_defaults(run=cmd_see)

    p = sub.add_parser("rate", help="k of n showed it: the range the true rate could be in")
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--k", type=int, default=0)
    p.add_argument("--level", type=float, default=0.95)
    p.set_defaults(run=cmd_rate)

    a = ap.parse_args()
    for name in ("n", "n2"):
        value = getattr(a, name, None)
        if value is not None and value < 1:
            ap.error(f"--{name} has to be at least 1")
    for name in ("alpha", "level", "null", "p1", "p2"):
        value = getattr(a, name, None)
        if value is not None and not 0.0 < value < 1.0:
            ap.error(f"--{name} has to be between 0 and 1")
    for name in ("rate", "p"):
        for value in getattr(a, name, None) or []:
            if not 0.0 <= value <= 1.0:
                ap.error(f"--{'if' if name == 'rate' else name} takes a rate between 0 and 1")
    power_ = getattr(a, "power", None)
    for value in (power_ if isinstance(power_, list) else [power_] if power_ is not None else []):
        if not getattr(a, "alpha", 0.0) < value < 1.0:
            ap.error("--power has to be above alpha and below 1")
    if getattr(a, "times", 1) < 1:
        ap.error("--times has to be at least 1")
    try:
        return a.run(a)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
