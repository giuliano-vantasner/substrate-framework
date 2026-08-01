"""Shared verification primitives for campaign and framework code."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable


class CheckFailure(AssertionError):
    """Raised when a verification condition fails."""


@dataclass
class CheckLedger:
    """Collect named checks and emit the repository's terminal tally."""

    claim_id: str
    passed: list[str] = field(default_factory=list)

    def check(self, name: str, condition: object, detail: str = "") -> None:
        if not bool(condition):
            suffix = f" -- {detail}" if detail else ""
            raise CheckFailure(f"FAIL [{self.claim_id}] {name}{suffix}")
        self.passed.append(name)
        print(f"PASS [{self.claim_id}] {name}")

    def mutation_sensitive(
        self,
        name: str,
        predicate: Callable[[object], object],
        baseline: object,
        mutations: Iterable[object],
    ) -> None:
        """Require a predicate to accept the derivation and reject every mutation."""

        mutated = list(mutations)
        self.check(f"{name}: baseline", predicate(baseline), "baseline was rejected")
        self.check(f"{name}: mutations supplied", bool(mutated), "no mutations were tested")
        for index, candidate in enumerate(mutated, start=1):
            self.check(
                f"{name}: mutation {index} rejected",
                not bool(predicate(candidate)),
                "the check is insensitive to a changed input",
            )

    def finish(self) -> int:
        if not self.passed:
            raise CheckFailure(f"FAIL [{self.claim_id}] no checks ran")
        print(f"ALL {len(self.passed)} CHECKS PASS [{self.claim_id}]")
        return len(self.passed)
