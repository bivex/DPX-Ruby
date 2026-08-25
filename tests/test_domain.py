import pytest
from pattern_detector.domain.value_objects import (
    PatternCategory,
    PatternType,
    Confidence,
    ConfidenceLevel,
    SourceLocation,
    EvidenceItem,
)
from pattern_detector.domain.pattern import PATTERN_CATALOG
from pattern_detector.domain.code_model import (
    RubyMethod,
    RubyClass,
    RubyModule,
    RubyFile,
    CodeModel,
)
from pattern_detector.domain.detection import Detection, DetectionReport


def test_confidence_levels():
    c1 = Confidence(0.95)
    assert c1.level == ConfidenceLevel.VERY_HIGH
    assert c1.percentage == 95

    c2 = Confidence(0.75)
    assert c2.level == ConfidenceLevel.HIGH

    c3 = Confidence(0.60)
    assert c3.level == ConfidenceLevel.MEDIUM

    c4 = Confidence(0.30)
    assert c4.level == ConfidenceLevel.LOW


def test_pattern_catalog():
    assert len(PATTERN_CATALOG) == 42
    for p_type in PatternType:
        assert p_type in PATTERN_CATALOG
        meta = PATTERN_CATALOG[p_type]
        assert meta.default_weight > 0.5
        assert len(meta.description) > 10


def test_code_model_indexing():
    model = CodeModel()
    m1 = RubyMethod(name="call", params="user_id", line_number=10)
    cls1 = RubyClass(name="CreateUserService", methods=[m1], line_number=5)
    mod1 = RubyModule(name="Taggable", is_concern=True, line_number=20)

    f = RubyFile(
        file_path="app/services/create_user_service.rb",
        raw_content="",
        classes=[cls1],
        modules=[mod1],
    )
    model.add_file(f)

    assert model.get_class("CreateUserService") == cls1
    assert model.get_module("Taggable") == mod1
    assert cls1.is_service is True
    assert model.get_class("nonexistent") is None


def test_detection_report_serialization():
    loc = SourceLocation("app/models/user.rb", 15, 1)
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
        execution_time_seconds=0.015,
        detections=[d],
    )

    assert report.total_detections == 1
    assert report.category_counts[PatternCategory.RUBY_IDIOMATIC.value] == 1
    d_dict = d.to_dict()
    assert d_dict["pattern_type"] == "activesupport_concern"
    assert d_dict["confidence"]["percentage"] == 95
