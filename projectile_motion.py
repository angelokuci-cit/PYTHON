#!/usr/bin/env python3
"""Projectile motion simulation and visualization."""

from __future__ import annotations

import argparse
import math
from typing import Iterable, Tuple


def time_of_flight(v0: float, angle_rad: float, g: float) -> float:
    vertical_velocity = v0 * math.sin(angle_rad)
    if g <= 0:
        raise ValueError("Gravitational acceleration must be positive.")
    if vertical_velocity <= 0:
        raise ValueError("Launch angle must produce a positive vertical velocity.")
    return (2 * vertical_velocity) / g


def max_height(v0: float, angle_rad: float, g: float) -> float:
    if g <= 0:
        raise ValueError("Gravitational acceleration must be positive.")
    vertical_velocity = v0 * math.sin(angle_rad)
    return (vertical_velocity ** 2) / (2 * g)


def horizontal_range(v0: float, angle_rad: float, g: float) -> float:
    flight_time = time_of_flight(v0, angle_rad, g)
    return v0 * math.cos(angle_rad) * flight_time


def compute_trajectory(
    v0: float, angle_rad: float, g: float, samples: int
) -> Tuple[list[float], list[float], list[float]]:
    flight_time = time_of_flight(v0, angle_rad, g)
    times = [flight_time * step / samples for step in range(samples + 1)]
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)
    x_vals = [v0 * cos_angle * time for time in times]
    y_vals = [v0 * sin_angle * time - 0.5 * g * time**2 for time in times]
    return times, x_vals, y_vals


def angle_range_analysis(
    v0: float,
    g: float,
    angles_deg: Iterable[int],
) -> Tuple[list[int], list[float], int, float]:
    angles = []
    ranges = []
    for angle in angles_deg:
        if 0 < angle < 90:
            angle_rad = math.radians(angle)
            angles.append(angle)
            ranges.append(horizontal_range(v0, angle_rad, g))
    if not ranges:
        raise ValueError("No valid angles provided for range analysis.")
    best_range, best_angle = max(zip(ranges, angles))
    return angles, ranges, best_angle, best_range


def plot_results(
    times: list[float],
    x_vals: list[float],
    y_vals: list[float],
    angles: list[int],
    ranges: list[float],
    best_angle: int,
    best_range: float,
    save_path: str | None,
) -> None:
    if save_path:
        import matplotlib

        matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes[0, 0].plot(x_vals, y_vals, color="tab:blue")
    axes[0, 0].set_title("Trajectory y(x)")
    axes[0, 0].set_xlabel("x (m)")
    axes[0, 0].set_ylabel("y (m)")
    axes[0, 0].grid(True)

    axes[0, 1].plot(times, x_vals, label="x(t)")
    axes[0, 1].plot(times, y_vals, label="y(t)")
    axes[0, 1].set_title("Position vs Time")
    axes[0, 1].set_xlabel("Time (s)")
    axes[0, 1].set_ylabel("Position (m)")
    axes[0, 1].legend()
    axes[0, 1].grid(True)

    axes[1, 0].plot(angles, ranges, color="tab:green")
    axes[1, 0].scatter([best_angle], [best_range], color="tab:red", zorder=3)
    axes[1, 0].set_title("Range vs Angle")
    axes[1, 0].set_xlabel("Angle (deg)")
    axes[1, 0].set_ylabel("Range (m)")
    axes[1, 0].grid(True)

    axes[1, 1].axis("off")
    axes[1, 1].text(
        0.05,
        0.7,
        f"Best angle: {best_angle}°\nMax range: {best_range:.2f} m",
        fontsize=12,
    )

    fig.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    else:
        plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simulate projectile motion using x(t) = v0 cos θ t and y(t) = v0 sin θ t - ½ g t²."
    )
    parser.add_argument("--v0", type=float, default=50.0, help="Initial velocity (m/s).")
    parser.add_argument("--angle", type=float, default=45.0, help="Launch angle (degrees).")
    parser.add_argument("--g", type=float, default=9.81, help="Gravitational acceleration (m/s²).")
    parser.add_argument("--samples", type=int, default=200, help="Number of time samples.")
    parser.add_argument(
        "--analysis-start", type=int, default=5, help="Start angle for range analysis (degrees)."
    )
    parser.add_argument(
        "--analysis-end", type=int, default=85, help="End angle for range analysis (degrees)."
    )
    parser.add_argument(
        "--analysis-step", type=int, default=1, help="Angle step for range analysis (degrees)."
    )
    parser.add_argument(
        "--save",
        type=str,
        default=None,
        help="Save plots to a file instead of showing them.",
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Skip plotting (prints metrics and analysis only).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not (0 < args.angle < 90):
        raise ValueError("Angle must be between 0 and 90 degrees.")
    if args.samples < 2:
        raise ValueError("Samples must be at least 2.")

    angle_rad = math.radians(args.angle)
    flight_time = time_of_flight(args.v0, angle_rad, args.g)
    peak_height = max_height(args.v0, angle_rad, args.g)
    range_distance = horizontal_range(args.v0, angle_rad, args.g)

    times, x_vals, y_vals = compute_trajectory(args.v0, angle_rad, args.g, args.samples)

    analysis_angles = range(args.analysis_start, args.analysis_end + 1, args.analysis_step)
    angles, ranges, best_angle, best_range = angle_range_analysis(args.v0, args.g, analysis_angles)

    print(f"Initial velocity: {args.v0:.2f} m/s")
    print(f"Launch angle: {args.angle:.2f}°")
    print(f"Gravity: {args.g:.2f} m/s²")
    print(f"Time of flight: {flight_time:.2f} s")
    print(f"Maximum height: {peak_height:.2f} m")
    print(f"Range: {range_distance:.2f} m")
    print(f"Best range from {args.analysis_start}° to {args.analysis_end}°: {best_range:.2f} m at {best_angle}°")

    if not args.no_plot:
        plot_results(
            times,
            x_vals,
            y_vals,
            angles,
            ranges,
            best_angle,
            best_range,
            args.save,
        )


if __name__ == "__main__":
    main()
