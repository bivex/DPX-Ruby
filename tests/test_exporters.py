import json
import os
import pytest
from pattern_detector.domain.value_objects import PatternType, Confidence, SourceLocation, EvidenceItem
from pattern_detector.domain.detection import Detection, DetectionReport
from pattern_detector.adapters.outbound.exporters.html_hud_exporter import HtmlHudExporter
from pattern_detector.adapters.outbound.exporters.json_exporter import JsonExporter
from pattern_detector.adapters.outbound.exporters.markdown_exporter import MarkdownExporter
from pattern_detector.adapters.outbound.exporters.sarif_exporter import SarifExporter


def test_all_exporters(tmp_path):
    loc = SourceLocation("app/models/user.rb", 10, 1)
    ev = EvidenceItem("RULE_TEST", 0.95, "Test description", loc)
    d = Detection(
        pattern_type=PatternType.ACTIVESUPPORT_CONCERN,
        target_name="User",
        location=loc,
        confidence=Confidence(0.95),
        evidence=[ev],
    )

    report = DetectionReport(
        target_path="app/",
        scanned_files_count=1,
        execution_time_seconds=0.005,
        detections=[d],
    )

    html_file = tmp_path / "hud.html"
    json_file = tmp_path / "report.json"
    md_file = tmp_path / "report.md"
    sarif_file = tmp_path / "report.sarif"

    HtmlHudExporter().export(report, str(html_file))
    JsonExporter().export(report, str(json_file))
    MarkdownExporter().export(report, str(md_file))
    SarifExporter().export(report, str(sarif_file))

    assert html_file.exists()
    assert "DPX-Ruby" in html_file.read_text()

    assert json_file.exists()
    data = json.loads(json_file.read_text())
    assert data["total_detections"] == 1

    assert md_file.exists()
    assert "DPX-Ruby Analysis Report" in md_file.read_text()

    assert sarif_file.exists()
    sarif_data = json.loads(sarif_file.read_text())
    assert sarif_data["version"] == "2.1.0"
