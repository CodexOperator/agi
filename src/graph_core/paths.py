"""Path safety enforcement (T-016 / graph-core R11).

Ensures all paths used by graph-core stay within the project root.
Cache and state directories are rooted under `context/` for portability.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .errors import GraphCoreError, PathOutsideProjectError


class PathValidator:
    """Validates that paths stay within the project root."""

    def __init__(self, project_root: str | Path) -> None:
        self._project_root = Path(project_root).resolve()

    @property
    def project_root(self) -> Path:
        return self._project_root

    def validate(self, path: str | Path) -> Path:
        """Resolve and validate a path stays within project root.

        Raises PathOutsideProjectError if the resolved path escapes.
        """
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(self._project_root)
        except ValueError:
            raise PathOutsideProjectError(resolved, self._project_root)
        return resolved

    def validate_relative(self, path: str | Path) -> Path:
        """Ensure a path is relative and stays within project root.

        Raises PathOutsideProjectError if path is absolute or escapes.
        """
        p = Path(path)
        if p.is_absolute():
            raise PathOutsideProjectError(p, self._project_root)
        # Check that joining with project root doesn't escape
        resolved = (self._project_root / p).resolve()
        try:
            resolved.relative_to(self._project_root)
        except ValueError:
            raise PathOutsideProjectError(p, self._project_root)
        return resolved

    def cache_dir(self, subdir: str = ".cache") -> Path:
        """Return the cache directory under context/, creating if needed.

        Always returns a path inside project_root/context/<subdir>.
        """
        cache = self._project_root / "context" / subdir
        cache.mkdir(parents=True, exist_ok=True)
        return cache

    def context_dir(self) -> Path:
        """Return the context directory path, creating if needed."""
        ctx = self._project_root / "context"
        ctx.mkdir(parents=True, exist_ok=True)
        return ctx


# Module-level default validator; can be overridden via set_project_root()
_validator: Optional[PathValidator] = None


def get_validator(project_root: str | Path | None = None) -> PathValidator:
    """Get or create a PathValidator.

    If project_root is None and a validator exists, return it.
    Otherwise create a new validator.
    """
    global _validator
    if project_root is None:
        if _validator is None:
            raise GraphCoreError("no project root set and no validator exists")
        return _validator
    _validator = PathValidator(project_root)
    return _validator


def set_project_root(root: str | Path) -> PathValidator:
    """Set the project root and return the validator."""
    return get_validator(root)


def safe_path(path: str | Path) -> Path:
    """Validate a path using the current validator.

    Raises PathOutsideProjectError if validation fails.
    """
    return get_validator().validate(path)


def safe_relative_path(path: str | Path) -> Path:
    """Validate a relative path using the current validator.

    Raises PathOutsideProjectError if path is absolute or escapes.
    """
    return get_validator().validate_relative(path)


def safe_cache_path(filename: str, subdir: str = ".cache") -> Path:
    """Return a safe cache file path under context/<subdir>/<filename>.

    The returned path is guaranteed to be within the project root.
    """
    validator = get_validator()
    cache_dir = validator.cache_dir(subdir)
    # Ensure the filename itself doesn't try to escape
    safe_name = Path(filename)
    if safe_name.is_absolute() or safe_name.parts and safe_name.parts[0] == "..":
        raise PathOutsideProjectError(filename, validator.project_root)
    return cache_dir / safe_name
