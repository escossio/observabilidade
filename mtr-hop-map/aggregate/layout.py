from __future__ import annotations


def horizontal(count: int, start_x: int = 40, y: int = 130, spacing: int = 155) -> list[tuple[int, int]]:
    return [(start_x + index * spacing, y) for index in range(count)]


def branch(start_x: int, count: int, y: int = 260, spacing: int = 155) -> list[tuple[int, int]]:
    return [(start_x + index * spacing, y) for index in range(count)]

