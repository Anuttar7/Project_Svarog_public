import os
import numpy as np
import json

def plot_profile(props: dict, save_path: str = None) -> str:
    """
    Generates cross-sectional profile plot without LaTeX dependency.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    R = props["geometry"]["FLANGE_MEAN_RADIUS"]
    theta = np.radians(props["geometry"]["FLANGE_SUBTENDED_ANGLE_DEG"])
    w = props["geometry"]["BONDED_WEB_LENGTH"]

    phi = np.linspace(0, theta, 100)
    x_right = R * (1.0 - np.cos(phi)) * 1e3  # [mm]
    y_right = (w + R * np.sin(phi)) * 1e3    # [mm]

    x_left = -x_right
    y_left = y_right

    plt.figure(figsize=(7, 5))
    plt.plot(x_right, y_right, "b-", lw=2, label="Right Flange")
    plt.plot(x_left, y_left, "r-", lw=2, label="Left Flange")
    plt.plot([0, 0], [0, w * 1e3], "k-", lw=3, label="Bonded Web")
    plt.axhline(props["section_properties"]["BOOM_CENTROID_Y"] * 1e3, color="gray", linestyle="--", label=f"Centroid (y={props["section_properties"]["BOOM_CENTROID_Y"]*1e3:.1f} mm)")

    plt.title(f"Svarog TRAC Boom Thin-Shell Cross Section\n(R={R*1e3:.1f} mm, theta={props["geometry"]["FLANGE_SUBTENDED_ANGLE_DEG"]:.0f} deg, w={w*1e3:.1f} mm)")
    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    plt.grid(True, alpha=0.3)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.legend(loc="upper left")

    out_file = os.path.join(save_path, "section_diagram.png")
    plt.savefig(out_file, dpi=150, bbox_inches="tight")
    plt.close()
    return out_file

with open("boom_properties.json", "r") as f:
    plot_profile(json.load(f), ".")