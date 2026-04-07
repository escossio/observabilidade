from __future__ import annotations


def build_layout(count: int, start_x: int = 40, y: int = 130, spacing: int = 155) -> list[tuple[int, int]]:
    return [(start_x + index * spacing, y) for index in range(count)]


def compute_map_size(count: int, start_x: int = 40, spacing: int = 155, icon_size: int = 96, height: int = 360) -> tuple[int, int]:
    width = start_x * 2 + max(1, count - 1) * spacing + icon_size
    return max(800, width), height
