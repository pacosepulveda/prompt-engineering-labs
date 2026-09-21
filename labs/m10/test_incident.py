import unittest

from incident_analyzer import analyze_incident


class TestIncidentRegression(unittest.TestCase):
    def test_public_function_accepts_dict(self):
        result = analyze_incident({"service": "identity-api"})
        self.assertEqual(result["service"], "identity-api")

    def test_non_dict_rejected(self):
        with self.assertRaises(TypeError):
            analyze_incident("identity-api")

    def test_missing_service_uses_unknown(self):
        result = analyze_incident({"service_status": "available"})
        self.assertEqual(result["service"], "unknown")

    def test_missing_status_uses_unknown(self):
        result = analyze_incident({"service": "identity-api"})
        self.assertEqual(result["status"], "unknown")

    def test_summary_preserves_existing_format(self):
        result = analyze_incident({
            "service": "identity-api",
            "service_status": "degraded",
            "affected_users": 12,
            "error_rate": 1.5,
        })
        self.assertEqual(
            result["summary"],
            "identity-api: degraded; 12 users affected; error rate 1.5%",
        )

    def test_summary_omits_missing_optional_metrics(self):
        result = analyze_incident({
            "service": "billing-api",
            "service_status": "available",
        })
        self.assertEqual(result["summary"], "billing-api: available")

    def test_unavailable_requires_human_review(self):
        result = analyze_incident({
            "service": "identity-api",
            "service_status": "unavailable",
        })
        self.assertTrue(result["requires_human_review"])

    def test_security_signal_requires_human_review(self):
        result = analyze_incident({
            "service": "identity-api",
            "service_status": "available",
            "security_signal": True,
        })
        self.assertTrue(result["requires_human_review"])

    def test_one_hundred_users_requires_human_review(self):
        result = analyze_incident({
            "service": "identity-api",
            "service_status": "degraded",
            "affected_users": 100,
        })
        self.assertTrue(result["requires_human_review"])

    def test_small_degradation_does_not_force_human_review(self):
        result = analyze_incident({
            "service": "identity-api",
            "service_status": "degraded",
            "affected_users": 8,
            "error_rate": 0.5,
        })
        self.assertFalse(result["requires_human_review"])


class TestSeverityFeature(unittest.TestCase):
    def test_p1_for_unavailable_service(self):
        result = analyze_incident({
            "service": "identity-api",
            "service_status": "unavailable",
            "affected_users": 2,
            "error_rate": 0.2,
        })
        self.assertEqual(result["severity"], "P1")

    def test_p1_for_security_signal(self):
        result = analyze_incident({
            "service": "identity-api",
            "service_status": "available",
            "affected_users": 1,
            "error_rate": 0.0,
            "security_signal": True,
        })
        self.assertEqual(result["severity"], "P1")

    def test_p1_at_affected_users_boundary(self):
        result = analyze_incident({
            "service": "identity-api",
            "service_status": "degraded",
            "affected_users": 100,
            "error_rate": 0.1,
        })
        self.assertEqual(result["severity"], "P1")

    def test_p2_boundaries(self):
        cases = [
            {
                "service": "identity-api",
                "service_status": "degraded",
                "affected_users": 25,
                "error_rate": 0.1,
            },
            {
                "service": "identity-api",
                "service_status": "degraded",
                "affected_users": 2,
                "error_rate": 5.0,
            },
        ]
        for incident in cases:
            with self.subTest(incident=incident):
                self.assertEqual(analyze_incident(incident)["severity"], "P2")

    def test_p3_for_low_impact_degradation(self):
        result = analyze_incident({
            "service": "identity-api",
            "service_status": "degraded",
            "affected_users": 12,
            "error_rate": 1.2,
        })
        self.assertEqual(result["severity"], "P3")

    def test_p4_and_undetermined(self):
        cases = [
            ({"service": "identity-api", "service_status": "available"}, "P4"),
            ({"service": "identity-api"}, "UNDETERMINED"),
        ]
        for incident, expected in cases:
            with self.subTest(incident=incident):
                self.assertEqual(analyze_incident(incident)["severity"], expected)


if __name__ == "__main__":
    unittest.main()
