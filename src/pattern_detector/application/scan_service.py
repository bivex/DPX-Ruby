from typing import List, Optional
from ..domain.detection import DetectionReport
from ..ports.inbound.parser_port import RubyParserPort
from ..ports.inbound.detector_port import PatternDetectorPort
from ..ports.outbound.exporter_port import ExporterPort


class ScanService:
    def __init__(
        self,
        parser: RubyParserPort,
        detector: PatternDetectorPort,
        exporters: Optional[List[ExporterPort]] = None,
    ):
        self.parser = parser
        self.detector = detector
        self.exporters = exporters or []

    def scan_paths(
        self,
        paths: List[str],
        html_out: Optional[str] = None,
        json_out: Optional[str] = None,
        md_out: Optional[str] = None,
        sarif_out: Optional[str] = None,
    ) -> DetectionReport:
        model = self.parser.parse_code_model(paths)
        report = self.detector.detect(model)

        from ..adapters.outbound.exporters.html_hud_exporter import HtmlHudExporter
        from ..adapters.outbound.exporters.json_exporter import JsonExporter
        from ..adapters.outbound.exporters.markdown_exporter import MarkdownExporter
        from ..adapters.outbound.exporters.sarif_exporter import SarifExporter

        if html_out:
            HtmlHudExporter().export(report, html_out)
        if json_out:
            JsonExporter().export(report, json_out)
        if md_out:
            MarkdownExporter().export(report, md_out)
        if sarif_out:
            SarifExporter().export(report, sarif_out)

        return report
