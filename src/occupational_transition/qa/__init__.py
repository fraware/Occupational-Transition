"""Ticket QA entrypoints for ``occupational_transition.run_step``.

Each module exposes ``main() -> int`` (``0`` success, non-zero failure). Optional
``None`` is treated as success by ``run_step.run_qa``; booleans and other types
are rejected so exit semantics stay explicit.
"""
