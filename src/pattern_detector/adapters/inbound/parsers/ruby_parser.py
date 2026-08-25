import os
import re
from typing import List, Optional
from ....domain.code_model import RubyMethod, RubyClass, RubyModule, RubyFile, CodeModel
from ....ports.inbound.parser_port import RubyParserPort


class RegexRubyParser(RubyParserPort):
    """
    Fast single-pass parser for Ruby (.rb, .rake, .erb) codebases.
    """

    def parse_file(self, file_path: str, content: str) -> RubyFile:
        ruby_file = RubyFile(file_path=file_path, raw_content=content)

        # 1. Parse Classes
        self._parse_classes(content, ruby_file)

        # 2. Parse Modules
        self._parse_modules(content, ruby_file)

        return ruby_file

    def parse_code_model(self, paths: List[str]) -> CodeModel:
        model = CodeModel()
        valid_extensions = {
            ".rb", ".rake", ".builder", ".gemspec", ".erb",
            "gemfile", "rakefile", "config.ru", "vagrantfile",
            "fastfile", "podfile", "capfile", "berksfile",
            "cheffile", "guardfile", "appraisals", "brewfile",
        }
        for path in paths:
            if os.path.isfile(path):
                ext = os.path.splitext(path)[1].lower()
                base = os.path.basename(path).lower()
                if ext in valid_extensions or base in valid_extensions or "vagrantfile" in base:
                    try:
                        with open(path, "r", encoding="utf-8", errors="replace") as f:
                            content = f.read()
                        rf = self.parse_file(path, content)
                        model.add_file(rf)
                    except Exception:
                        pass
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        ext = os.path.splitext(file)[1].lower()
                        base = file.lower()
                        if ext in valid_extensions or base in valid_extensions or "vagrantfile" in base:
                            full_path = os.path.join(root, file)
                            try:
                                with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                                    content = f.read()
                                rf = self.parse_file(full_path, content)
                                model.add_file(rf)
                            except Exception:
                                pass
        return model

    def _get_line_number(self, content: str, match_start: int) -> int:
        return content.count("\n", 0, match_start) + 1

    def _extract_block(self, content: str, start_idx: int) -> str:
        lines = content[start_idx:].splitlines()
        collected = []
        depth = 0
        for idx, line in enumerate(lines):
            stripped = line.strip()
            # Ignore comments
            if stripped.startswith("#"):
                collected.append(line)
                continue

            # Check block openings
            if re.match(r'^\s*(?:class|module|def|if|unless|case|while|until|for|begin)\b', line) or " do" in line or line.endswith(" do"):
                depth += 1
            if re.match(r'^\s*end\b', line):
                depth -= 1
                if depth <= 0:
                    collected.append(line)
                    break
            collected.append(line)
        return "\n".join(collected)

    def _parse_methods(self, block_content: str, offset_line: int) -> List[RubyMethod]:
        methods: List[RubyMethod] = []
        method_pattern = re.compile(
            r'^\s*def\s+(self\.)?([a-zA-Z0-9_!?=]+)(?:\s*\((.*?)\)|\s+([^\n=]+))?',
            re.MULTILINE,
        )

        for m in method_pattern.finditer(block_content):
            is_class = bool(m.group(1))
            name = m.group(2)
            params = (m.group(3) or m.group(4) or "").strip()
            line_num = offset_line + block_content.count("\n", 0, m.start())

            method_body = self._extract_block(block_content, m.start())
            methods.append(
                RubyMethod(
                    name=name,
                    params=params,
                    is_class_method=is_class,
                    raw_body=method_body,
                    line_number=line_num,
                )
            )
        return methods

    def _parse_classes(self, content: str, ruby_file: RubyFile) -> None:
        class_pattern = re.compile(
            r'^\s*class\s+([A-Z][a-zA-Z0-9_:]*)(?:\s*<\s*([A-Z][a-zA-Z0-9_:]*))?',
            re.MULTILINE,
        )

        for m in class_pattern.finditer(content):
            cls_name = m.group(1)
            superclass = m.group(2)
            line_num = self._get_line_number(content, m.start())
            block_body = self._extract_block(content, m.start())

            # Mixins
            mixins = re.findall(r'^\s*(?:include|extend|prepend)\s+([A-Z][a-zA-Z0-9_:]*)', block_body, re.MULTILINE)
            # Associations
            associations = re.findall(r'^\s*(?:has_many|belongs_to|has_one|has_and_belongs_to_many)\s+:([a-zA-Z0-9_]+)', block_body, re.MULTILINE)
            # Callbacks
            callbacks = re.findall(r'^\s*(?:before_save|after_save|before_create|after_create|after_commit|before_action|around_action)\s+:([a-zA-Z0-9_]+)', block_body, re.MULTILINE)

            methods = self._parse_methods(block_body, line_num)

            ruby_file.classes.append(
                RubyClass(
                    name=cls_name,
                    superclass=superclass,
                    mixins=mixins,
                    methods=methods,
                    associations=associations,
                    callbacks=callbacks,
                    raw_body=block_body,
                    line_number=line_num,
                )
            )

    def _parse_modules(self, content: str, ruby_file: RubyFile) -> None:
        module_pattern = re.compile(r'^\s*module\s+([A-Z][a-zA-Z0-9_:]*)', re.MULTILINE)

        for m in module_pattern.finditer(content):
            mod_name = m.group(1)
            line_num = self._get_line_number(content, m.start())
            block_body = self._extract_block(content, m.start())

            is_concern = "extend ActiveSupport::Concern" in block_body
            mixins = re.findall(r'^\s*(?:include|extend|prepend)\s+([A-Z][a-zA-Z0-9_:]*)', block_body, re.MULTILINE)
            methods = self._parse_methods(block_body, line_num)

            ruby_file.modules.append(
                RubyModule(
                    name=mod_name,
                    mixins=mixins,
                    methods=methods,
                    is_concern=is_concern,
                    raw_body=block_body,
                    line_number=line_num,
                )
            )
