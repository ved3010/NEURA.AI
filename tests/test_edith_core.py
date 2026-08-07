"""
E.D.I.T.H. Core Unit Tests
"""

import unittest
from edith.memory import remember_fact, recall_memory, add_task, get_tasks
from edith.tools.protocols import trigger_protocol


class TestEdithCore(unittest.TestCase):
    def test_memory_and_recall(self):
        res_store = remember_fact("unit_test_key", "test_value_123")
        self.assertIn("Tactical note recorded", res_store)
        
        res_recall = recall_memory("unit_test_key")
        self.assertIn("test_value_123", res_recall)

    def test_tasks(self):
        res_add = add_task("Test task item")
        self.assertIn("added to roster", res_add)
        
        res_get = get_tasks()
        self.assertIn("Test task item", res_get)

    def test_protocols(self):
        res_edith = trigger_protocol("edith")
        self.assertIn("PROTOCOL E.D.I.T.H.", res_edith)
        
        res_sentry = trigger_protocol("sentry")
        self.assertIn("PROTOCOL SENTRY", res_sentry)


if __name__ == "__main__":
    unittest.main()
