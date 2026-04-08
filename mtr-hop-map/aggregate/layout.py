from __future__ import annotations


def horizontal(count: int, start_x: int = 80, y: int = 140, spacing: int = 175) -> list[tuple[int, int]]:
    return [(start_x + index * spacing, y) for index in range(count)]


def branch(start_x: int, count: int, y: int = 320, spacing: int = 175) -> list[tuple[int, int]]:
    return [(start_x + index * spacing, y) for index in range(count)]


def compute_canvas_size(trunk_count: int, branch_depth: int, branch_bands: int) -> tuple[int, int]:
    width = max(2200, 80 * 2 + max(1, trunk_count - 1) * 175 + 180)
    height = max(980, 260 + branch_bands * 160 + max(0, branch_depth) * 18)
    return width, height
