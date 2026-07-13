import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HandoffDirectModeTests(unittest.TestCase):
    def test_consumer_contract_declares_v2_and_required_report(self):
        contract_path = ROOT / "contracts" / "img-style-transfer-handoff-v2.json"
        contract = json.loads(contract_path.read_text(encoding="utf-8"))

        self.assertEqual(contract["title"], "IMG_STYLE_TRANSFER_HANDOFF_V2")
        self.assertIn("compliance_report", contract["required"])

    def test_valid_handoff_does_not_restart_content_research(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("## V2 交接直通模式", skill)
        self.assertIn("不重新联网搜索、改写或扩写已锁定内容", skill)
        self.assertIn("needs_input", skill)

    def test_direct_mode_preserves_visual_approval_gates(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("模板选择", skill)
        self.assertIn("封面基准确认", skill)
        self.assertIn("逐张生成", skill)


if __name__ == "__main__":
    unittest.main()
