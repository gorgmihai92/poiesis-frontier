"""power.py against published worked examples, and against second calculations made another way.

The published values and where each was read are in research/notes: gpower-2023-manual.md and
lakens-2022-sample-size-justification.md.
"""
import math
import random
import unittest
from fractions import Fraction

import helpers
import power


class GPowerManual(unittest.TestCase):
    """G*Power 3.1 manual of 1 June 2023, sections 4 and 19, read on 2026-11-22."""

    def test_matched_pairs_power_is_0_832114(self):
        # p. 48: 50 pairs, dz = 0.421637, two-sided, alpha 0.05 -> power 0.832114
        self.assertAlmostEqual(power.power_means(0.421637, 50, paired=True), 0.832114, places=6)

    def test_matched_pairs_critical_t_is_2_009575(self):
        # p. 48: critical t 2.009575 with 49 degrees of freedom
        self.assertAlmostEqual(power.t_crit(49, 0.05), 2.009575, places=6)

    def test_matched_pairs_with_no_correlation_power_is_0_500352(self):
        # p. 48: with dz = 0.2828427 the power is 0.500352
        self.assertAlmostEqual(power.power_means(0.2828427, 50, paired=True), 0.500352, places=6)

    def test_binomial_example_rejects_at_17_of_20(self):
        # p. 12: constant 0.65, one-sided, alpha 0.05, N = 20 -> critical N 17, actual alpha 0.044376
        count, reached = power.critical_count(20, 0.65, 0.05)
        self.assertEqual(count, 17)
        self.assertAlmostEqual(reached, 0.044376, places=6)

    def test_binomial_example_power_is_0_411449(self):
        # p. 12: true proportion 0.8 -> power 0.411449
        self.assertAlmostEqual(power.binom_at_least(17, 20, 0.8), 0.411449, places=6)


class Lakens2022(unittest.TestCase):
    """Lakens 2022, the author's version, pages as in the note. Two-sided independent t tests at alpha 0.05."""

    def test_d_0_4_at_90_percent_power_takes_133_per_condition(self):
        self.assertEqual(power.n_needed(0.4, 0.9), 133)  # p. 7

    def test_with_15_per_group_only_d_above_0_75_is_significant(self):
        self.assertEqual(round(power.critical_d(15), 2), 0.75)  # p. 12

    def test_with_15_per_group_90_percent_power_is_for_d_1_23(self):
        self.assertEqual(round(power.detectable_d(0.9, 15), 2), 1.23)  # p. 18

    def test_with_50_per_group_d_below_0_4_is_not_significant_and_0_57_has_80_percent_power(self):
        self.assertEqual(round(power.critical_d(50), 2), 0.40)  # p. 13
        self.assertEqual(round(power.detectable_d(0.8, 50), 2), 0.57)  # p. 13

    def test_d_0_5_with_90_per_condition_has_more_than_90_percent_power(self):
        self.assertGreater(power.power_means(0.5, 90), 0.90)  # p. 6
        self.assertLess(power.power_means(0.5, 90), 0.93)


class LabPlan(unittest.TestCase):
    """The lab plan's own sentence: five checks with no error leave a rate of up to 45% possible, thirty leave
    it under 10%."""

    def test_none_of_five_leaves_up_to_45_percent(self):
        self.assertAlmostEqual(power.rate_interval(0, 5)[1], 1 - 0.05 ** (1 / 5), places=9)
        self.assertEqual(round(100 * power.rate_interval(0, 5)[1]), 45)

    def test_none_of_thirty_leaves_under_10_percent(self):
        upper = power.rate_interval(0, 30)[1]
        self.assertLess(upper, 0.10)
        self.assertGreater(upper, 0.09)


class SecondCalculation(unittest.TestCase):
    """The same quantities computed another way."""

    def test_central_t_with_1_degree_of_freedom_is_the_cauchy_distribution(self):
        for t in (-3.0, -0.5, 0.0, 0.7, 2.0, 12.706):
            self.assertAlmostEqual(power.t_cdf(t, 1), 0.5 + math.atan(t) / math.pi, places=6)

    def test_central_t_with_2_degrees_of_freedom_has_a_closed_form(self):
        for t in (-4.0, -1.0, 0.0, 0.5, 2.92, 9.0):
            self.assertAlmostEqual(power.t_cdf(t, 2), 0.5 + t / (2 * math.sqrt(2 + t * t)), places=7)

    def test_with_many_degrees_of_freedom_t_is_close_to_normal(self):
        for t, delta in ((1.96, 0.0), (1.0, 2.0), (-0.5, -1.5)):
            self.assertAlmostEqual(power.t_cdf(t, 20000, delta), power.phi(t - delta), places=3)

    def test_noncentral_t_is_symmetric_under_a_change_of_sign(self):
        for t, df, delta in ((2.0, 5, 1.5), (-1.0, 12, 0.7), (3.5, 28, 3.2)):
            self.assertAlmostEqual(power.t_cdf(t, df, delta), 1 - power.t_cdf(-t, df, -delta), places=8)

    def test_noncentral_t_matches_a_simulation(self):
        rng = random.Random(20261122)
        df, delta, t, runs = 8, 2.0, 2.306, 200_000
        below = 0
        for _ in range(runs):
            chi2 = sum(rng.gauss(0, 1) ** 2 for _ in range(df))
            below += (rng.gauss(0, 1) + delta) / math.sqrt(chi2 / df) <= t
        self.assertAlmostEqual(power.t_cdf(t, df, delta), below / runs, delta=0.005)

    def test_power_under_no_difference_is_alpha(self):
        self.assertAlmostEqual(power.power_means(0.0, 12), 0.05, places=6)
        self.assertAlmostEqual(power.power_means(0.0, 9, paired=True, alpha=0.01), 0.01, places=6)
        self.assertAlmostEqual(power.power_means(0.0, 7, two_sided=False), 0.05, places=6)

    def test_power_grows_with_the_sample_and_with_the_difference(self):
        by_n = [power.power_means(0.6, n) for n in (5, 10, 20, 40, 80)]
        by_d = [power.power_means(d, 12) for d in (0.2, 0.5, 0.8, 1.2, 2.0)]
        self.assertEqual(by_n, sorted(by_n))
        self.assertEqual(by_d, sorted(by_d))

    def test_the_detectable_difference_has_the_power_it_was_asked_for(self):
        for n, level, paired in ((6, 0.8, False), (10, 0.9, True), (40, 0.95, False)):
            d = power.detectable_d(level, n, paired=paired)
            self.assertAlmostEqual(power.power_means(d, n, paired=paired), level, places=6)

    def test_the_number_needed_is_the_smallest_that_reaches_the_power(self):
        for d, level, paired in ((0.5, 0.8, False), (0.8, 0.9, False), (0.5, 0.8, True)):
            n = power.n_needed(d, level, paired=paired)
            self.assertGreaterEqual(power.power_means(d, n, paired=paired), level)
            self.assertLess(power.power_means(d, n - 1, paired=paired), level)

    def test_a_count_criterion_is_a_sum_of_binomial_terms(self):
        exact = sum(Fraction(math.comb(8, k)) * Fraction(1, 5) ** k * Fraction(4, 5) ** (8 - k) for k in range(3, 9))
        self.assertAlmostEqual(power.binom_at_least(3, 8, 0.2), float(exact), places=12)
        self.assertAlmostEqual(power.binom_at_least(3, 8, 0.2) + power.binom_at_most(2, 8, 0.2), 1.0, places=12)

    def test_seeing_a_thing_at_least_once_is_one_minus_nobody_showing_it(self):
        self.assertAlmostEqual(power.seen_at_least(5, 0.31), 1 - 0.69**5, places=12)
        self.assertAlmostEqual(power.rate_to_see(5, 0.8), 1 - 0.2 ** (1 / 5), places=9)

    def test_the_range_for_a_count_meets_its_definition(self):
        lower, upper = power.rate_interval(3, 8)
        self.assertAlmostEqual(power.binom_at_least(3, 8, lower), 0.025, places=9)
        self.assertAlmostEqual(power.binom_at_most(3, 8, upper), 0.025, places=9)
        self.assertEqual(power.rate_interval(8, 8)[1], 1.0)
        self.assertAlmostEqual(power.rate_interval(8, 8)[0], 0.05 ** (1 / 8), places=9)

    def test_fisher_p_for_three_against_none_of_three_is_one_in_ten(self):
        self.assertAlmostEqual(power.fisher_p(3, 0, 3, 3), 0.1, places=12)
        self.assertAlmostEqual(power.fisher_p(2, 2, 4, 4), 1.0, places=12)

    def test_fisher_test_rejects_no_more_often_than_alpha_when_there_is_no_difference(self):
        for n in (4, 8, 12):
            for p in (0.1, 0.3, 0.5, 0.8):
                self.assertLessEqual(power.power_two(p, p, n), 0.05 + 1e-12)

    def test_fisher_power_matches_a_sum_over_every_table_in_exact_fractions(self):
        n, p1, p2 = 5, Fraction(1, 10), Fraction(9, 10)

        def pmf(k, p):
            return Fraction(math.comb(n, k)) * p**k * (1 - p) ** (n - k)

        def hyper(a, m):
            return Fraction(math.comb(n, a) * math.comb(n, m - a), math.comb(2 * n, m))

        total = Fraction(0)
        for a in range(n + 1):
            for b in range(n + 1):
                m = a + b
                seen = hyper(a, m)
                p_value = sum(hyper(y, m) for y in range(max(0, m - n), min(n, m) + 1) if hyper(y, m) <= seen)
                if p_value <= Fraction(1, 20):
                    total += pmf(a, p1) * pmf(b, p2)
        self.assertAlmostEqual(power.power_two(0.1, 0.9, 5), float(total), places=12)

    def test_two_groups_of_three_can_never_be_significant(self):
        self.assertEqual(power.fisher_significant(3, 3), [])
        self.assertEqual(power.power_two(0.0001, 0.9999, 3), 0.0)


class CommandLine(unittest.TestCase):
    def test_detect_prints_the_three_levels_and_the_critical_difference(self):
        code, out, err = helpers.run(power, ["detect", "--n", "15"])
        self.assertEqual(code, 0)
        self.assertIn("Smallest observed difference that would be significant: d = 0.75", out)
        self.assertIn("90% of the time: d = 1.23", out)
        self.assertIn("not evidence of no difference", out)

    def test_detect_gives_the_difference_in_the_measures_units_when_the_spread_is_given(self):
        code, out, _ = helpers.run(power, ["detect", "--n", "15", "--sd", "1.5"])
        self.assertEqual(code, 0)
        self.assertIn("d = 1.23 = 1.84 in the measure's units (sd 1.5)", out)

    def test_paired_designs_are_named_as_such(self):
        code, out, _ = helpers.run(power, ["power", "--n", "50", "--paired", "--d", "0.421637"])
        self.assertEqual(code, 0)
        self.assertIn("50 people who each try both variants", out)
        self.assertIn("dz = 0.421637: 0.832114", out)

    def test_n_names_the_number_per_group(self):
        code, out, _ = helpers.run(power, ["n", "--d", "0.4", "--power", "0.9"])
        self.assertEqual(code, 0)
        self.assertIn("For power 0.9: 133 people in each group", out)

    def test_count_with_a_criterion_lists_how_often_each_rate_meets_it(self):
        code, out, _ = helpers.run(power, ["count", "--n", "8", "--at-least", "3", "--if", "0.2", "--if", "0.6"])
        self.assertEqual(code, 0)
        self.assertIn("Criterion: at least 3 of 8", out)
        self.assertIn("if the true rate is 0.2: met 20.3% of the time, not met 79.7%", out)
        self.assertIn("if the true rate is 0.6: met 95.0% of the time, not met 5.0%", out)

    def test_count_against_a_known_rate_prints_the_manuals_numbers(self):
        code, out, _ = helpers.run(power, ["count", "--n", "20", "--null", "0.65", "--if", "0.8"])
        self.assertEqual(code, 0)
        self.assertIn("Critical count: at least 17 of 20 (alpha actually reached: 0.044376)", out)
        self.assertIn("if the true rate is 0.8: power 0.411449", out)

    def test_count_says_when_a_group_is_too_small_to_reject_anything(self):
        code, out, _ = helpers.run(power, ["count", "--n", "3", "--null", "0.5"])
        self.assertEqual(code, 0)
        self.assertIn("too small for this test", out)

    def test_count_needs_a_criterion_or_a_known_rate(self):
        code, out, err = helpers.run(power, ["count", "--n", "8"])
        self.assertEqual(code, 2)
        self.assertIn("--at-least", err)

    def test_two_names_the_least_extreme_significant_outcome(self):
        code, out, _ = helpers.run(power, ["two", "--n", "8", "--p1", "0.2", "--p2", "0.8"])
        self.assertEqual(code, 0)
        self.assertIn("Least extreme outcome that is significant:", out)
        self.assertIn("Power when the true rates are 0.2 and 0.8:", out)

    def test_see_and_rate_print_plain_readings(self):
        code, out, _ = helpers.run(power, ["see", "--n", "5", "--p", "0.31"])
        self.assertEqual(code, 0)
        self.assertIn("probability 0.31: seen 84.4% of the time", out)
        code, out, _ = helpers.run(power, ["rate", "--n", "5"])
        self.assertEqual(code, 0)
        self.assertIn("as high as 45.1%", out)
        self.assertIn("Rule of three: 3/5 = 60.0%", out)

    def test_values_outside_their_range_are_refused(self):
        for argv in (["detect", "--n", "0"], ["detect", "--n", "8", "--alpha", "1.5"], ["rate", "--n", "5", "--k", "9"]):
            code, _, err = helpers.run(power, argv)
            self.assertEqual(code, 2, argv)

    def test_one_person_per_group_is_refused_with_a_reason(self):
        for argv in (["detect", "--n", "1"], ["power", "--n", "1", "--d", "0.5"], ["detect", "--n", "1", "--paired"]):
            code, _, err = helpers.run(power, argv)
            self.assertEqual(code, 2, argv)
            self.assertIn("at least 2 pairs", err)

    def test_two_people_in_one_group_and_one_in_the_other_can_be_compared(self):
        code, out, _ = helpers.run(power, ["detect", "--n", "2", "--n2", "1"])
        self.assertEqual(code, 0)
        self.assertIn("two groups of 2 and 1", out)


if __name__ == "__main__":
    unittest.main()
