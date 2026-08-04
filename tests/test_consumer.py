import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


APPLICATION_DIR = Path(__file__).resolve().parents[1] / "application"
sys.path.insert(0, str(APPLICATION_DIR))

import consumer  # noqa: E402


class ConsumerTests(unittest.TestCase):
    def setUp(self):
        self.channel = Mock()
        self.method = Mock(delivery_tag=42)

    @patch.object(consumer, "r")
    def test_acknowledges_successful_arithmetic_job(self, redis_client):
        pipeline = redis_client.pipeline.return_value

        consumer.on_message(
            self.channel,
            self.method,
            None,
            b'{"id": "operation-id", "expression": "2 + 3"}',
        )

        pipeline.set.assert_any_call(
            consumer._k_result("operation-id"), "5", ex=consumer.TTL_SECONDS
        )
        pipeline.set.assert_any_call(
            consumer._k_status("operation-id"), "done", ex=consumer.TTL_SECONDS
        )
        self.channel.basic_ack.assert_called_once_with(delivery_tag=42)

    @patch.object(consumer, "r")
    def test_records_division_by_zero_and_acknowledges(self, redis_client):
        consumer.on_message(
            self.channel,
            self.method,
            None,
            b'{"id": "operation-id", "expression": "1 / 0"}',
        )

        redis_client.set.assert_any_call(
            consumer._k_status("operation-id"), "error", ex=consumer.TTL_SECONDS
        )
        redis_client.set.assert_any_call(
            consumer._k_error("operation-id"),
            "Division par zéro",
            ex=consumer.TTL_SECONDS,
        )
        self.channel.basic_ack.assert_called_once_with(delivery_tag=42)

    @patch.object(consumer, "r")
    def test_records_non_numeric_result_as_error(self, redis_client):
        consumer.on_message(
            self.channel,
            self.method,
            None,
            b'{"id": "operation-id", "expression": "[1, 2]"}',
        )

        redis_client.set.assert_any_call(
            consumer._k_status("operation-id"), "error", ex=consumer.TTL_SECONDS
        )
        self.channel.basic_ack.assert_called_once_with(delivery_tag=42)


if __name__ == "__main__":
    unittest.main()
