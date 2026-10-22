import unittest

from gel_planner import build_plan, parse_pace, suggested_gels


class GelPlannerTests(unittest.TestCase):
    def test_parse_pace(self):
        self.assertAlmostEqual(parse_pace("4:30"), 4.5)
        self.assertAlmostEqual(parse_pace("4m30s"), 4.5)

    def test_example_plan(self):
        plan = build_plan(20, 4.5, 2)
        self.assertEqual([(row[1], round(row[2], 1)) for row in plan], [(25, 5.6), (75, 16.7)])

    def test_suggestion(self):
        self.assertEqual(suggested_gels(90), 2)

    def test_requested_count_is_replanned(self):
        plan = build_plan(30, 4.75, 4)
        self.assertEqual(len(plan), 4)
        self.assertEqual([row[1] for row in plan], [25, 59, 93, 128])


if __name__ == "__main__":
    unittest.main()
