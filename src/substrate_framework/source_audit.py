"""Deterministic lexical consumer audits for hash-pinned source trees.

Matches produced here are source-navigation evidence. A lexical occurrence in
code, a comment, or a docstring does not by itself establish a semantic or
scientific dependency.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path, PurePosixPath
import re
from typing import Mapping


@dataclass(frozen=True)
class SourceMatch:
    """One matched source file with content provenance."""

    path: str
    sha256: str
    groups: tuple[str, ...]


@dataclass(frozen=True)
class SourceAudit:
    """Deterministic result of one explicitly scoped lexical scan."""

    include_pattern: str
    exclusions: tuple[str, ...]
    token_patterns: tuple[tuple[str, str], ...]
    scanned_file_count: int
    matches: tuple[SourceMatch, ...]

    def paths_for(self, group: str) -> tuple[str, ...]:
        """Return sorted relative paths matching one declared token group."""

        declared = {name for name, _ in self.token_patterns}
        if group not in declared:
            raise KeyError(f"unknown token group: {group}")
        return tuple(match.path for match in self.matches if group in match.groups)

    def paths_with_all(self, *groups: str) -> tuple[str, ...]:
        """Return paths that match every named group."""

        if not groups:
            raise ValueError("at least one token group is required")
        declared = {name for name, _ in self.token_patterns}
        unknown = set(groups) - declared
        if unknown:
            raise KeyError(f"unknown token groups: {sorted(unknown)}")
        required = set(groups)
        return tuple(
            match.path
            for match in self.matches
            if required <= set(match.groups)
        )


def _normalized_exclusions(exclusions: tuple[str, ...]) -> tuple[str, ...]:
    normalized: list[str] = []
    for exclusion in exclusions:
        path = PurePosixPath(exclusion)
        if path.is_absolute() or ".." in path.parts or str(path) in {"", "."}:
            raise ValueError(f"invalid relative exclusion: {exclusion!r}")
        normalized.append(path.as_posix().rstrip("/"))
    return tuple(sorted(set(normalized)))


def _is_excluded(relative_path: str, exclusions: tuple[str, ...]) -> bool:
    path = PurePosixPath(relative_path)
    return any(
        path == PurePosixPath(exclusion)
        or PurePosixPath(exclusion) in path.parents
        for exclusion in exclusions
    )


def audit_source_tokens(
    root: Path,
    token_patterns: Mapping[str, str],
    *,
    include_pattern: str = "**/*.py",
    exclusions: tuple[str, ...] = (),
    flags: int = re.IGNORECASE,
) -> SourceAudit:
    """Scan an explicit source root and return sorted, hashed lexical matches.

    ``token_patterns`` maps stable group names to regular-expression strings.
    Exclusions are component-aware relative paths beneath ``root``. Text is
    decoded as UTF-8 with replacement so undecodable bytes cannot silently
    remove a file from the scan.
    """

    source_root = Path(root)
    if not source_root.is_dir():
        raise ValueError(f"source root is not a directory: {source_root}")
    if not include_pattern:
        raise ValueError("include_pattern must be non-empty")
    if not token_patterns:
        raise ValueError("at least one token pattern is required")

    compiled: dict[str, re.Pattern[str]] = {}
    for name, pattern in token_patterns.items():
        if not isinstance(name, str) or not name:
            raise ValueError("token group names must be non-empty strings")
        if not isinstance(pattern, str) or not pattern:
            raise ValueError(f"token pattern for {name!r} must be non-empty")
        compiled[name] = re.compile(pattern, flags)

    normalized_exclusions = _normalized_exclusions(exclusions)
    files: list[tuple[str, Path]] = []
    for path in source_root.glob(include_pattern):
        if not path.is_file():
            continue
        relative = path.relative_to(source_root).as_posix()
        if not _is_excluded(relative, normalized_exclusions):
            files.append((relative, path))
    files.sort(key=lambda item: item[0])

    matches: list[SourceMatch] = []
    for relative, path in files:
        payload = path.read_bytes()
        text = payload.decode("utf-8", errors="replace")
        matched_groups = tuple(
            sorted(name for name, regex in compiled.items() if regex.search(text))
        )
        if matched_groups:
            matches.append(
                SourceMatch(
                    path=relative,
                    sha256=hashlib.sha256(payload).hexdigest(),
                    groups=matched_groups,
                )
            )

    return SourceAudit(
        include_pattern=include_pattern,
        exclusions=normalized_exclusions,
        token_patterns=tuple(sorted(token_patterns.items())),
        scanned_file_count=len(files),
        matches=tuple(matches),
    )
