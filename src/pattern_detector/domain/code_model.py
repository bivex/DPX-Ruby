from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from .value_objects import SourceLocation


@dataclass
class RubyMethod:
    name: str
    params: str = ""
    is_class_method: bool = False
    raw_body: str = ""
    line_number: int = 1

    @property
    def lines_count(self) -> int:
        return len(self.raw_body.splitlines())


@dataclass
class RubyClass:
    name: str
    superclass: Optional[str] = None
    mixins: List[str] = field(default_factory=list)
    methods: List[RubyMethod] = field(default_factory=list)
    associations: List[str] = field(default_factory=list)
    callbacks: List[str] = field(default_factory=list)
    raw_body: str = ""
    line_number: int = 1

    @property
    def lines_count(self) -> int:
        return len(self.raw_body.splitlines())

    @property
    def is_service(self) -> bool:
        return any(self.name.endswith(k) for k in ["Service", "Interactor", "Workflow", "Operation"]) or any(m.name == "call" for m in self.methods)

    @property
    def is_policy(self) -> bool:
        return self.name.endswith("Policy") or (self.superclass and "Policy" in self.superclass)

    @property
    def is_form(self) -> bool:
        return self.name.endswith("Form") or ("ActiveModel::Model" in self.mixins)

    @property
    def is_query(self) -> bool:
        return self.name.endswith("Query") or self.name.endswith("Scope")

    @property
    def is_job(self) -> bool:
        return self.name.endswith("Job") or (self.superclass and "Job" in self.superclass)


@dataclass
class RubyModule:
    name: str
    mixins: List[str] = field(default_factory=list)
    methods: List[RubyMethod] = field(default_factory=list)
    is_concern: bool = False
    raw_body: str = ""
    line_number: int = 1


@dataclass
class RubyFile:
    file_path: str
    raw_content: str
    classes: List[RubyClass] = field(default_factory=list)
    modules: List[RubyModule] = field(default_factory=list)
    top_level_methods: List[RubyMethod] = field(default_factory=list)

    @property
    def lines_count(self) -> int:
        return len(self.raw_content.splitlines())


@dataclass
class CodeModel:
    files: List[RubyFile] = field(default_factory=list)
    class_index: Dict[str, RubyClass] = field(default_factory=dict)
    module_index: Dict[str, RubyModule] = field(default_factory=dict)

    def add_file(self, file: RubyFile) -> None:
        self.files.append(file)
        for cls in file.classes:
            self.class_index[cls.name.lower()] = cls
        for mod in file.modules:
            self.module_index[mod.name.lower()] = mod

    def get_class(self, name: str) -> Optional[RubyClass]:
        return self.class_index.get(name.lower())

    def get_module(self, name: str) -> Optional[RubyModule]:
        return self.module_index.get(name.lower())
