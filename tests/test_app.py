import sys
import unittest
from pathlib import Path
from unittest.mock import patch


APPLICATION_DIR = Path(__file__).resolve().parents[1] / "application"
sys.path.insert(0, str(APPLICATION_DIR))

import app as api  # noqa: E402


class ApiTests(unittest.TestCase):
    def setUp(self):
        api.app.config.update(TESTING=True)
        self.client = api.app.test_client()

    def test_rejects_missing_expression(self):
        response = self.client.post("/api/calc", json={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Expression missing"})

    @patch.object(api, "publish_job")
    @patch.object(api, "r")
    def test_queues_valid_expression(self, redis_client, publish_job):
        response = self.client.post("/api/calc", json={"expression": "2 + 3"})

        self.assertEqual(response.status_code, 202)
        payload = response.get_json()
        self.assertEqual(payload["status"], "queued")
        self.assertIn("id", payload)
        redis_client.set.assert_called_once()
        publish_job.assert_called_once_with(
            {"id": payload["id"], "expression": "2 + 3"}
        )

    @patch.object(api, "publish_job", side_effect=RuntimeError("unavailable"))
    @patch.object(api, "r")
    def test_reports_rabbitmq_outage(self, redis_client, publish_job):
        response = self.client.post("/api/calc", json={"expression": "2 + 3"})

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json(), {"error": "RabbitMQ unavailable"})
        self.assertEqual(redis_client.set.call_count, 3)
        publish_job.assert_called_once()

    @patch.object(api, "r")
    def test_returns_completed_result(self, redis_client):
        redis_client.get.side_effect = ["done", "5"]

        response = self.client.get("/api/result/operation-id")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "done", "result": "5"})


if __name__ == "__main__":
    unittest.main()
