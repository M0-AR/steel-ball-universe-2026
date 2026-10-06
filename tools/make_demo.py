"""Generate README demo assets: orbit animation (MP4 + GIF). Verified by file existence + size."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Orbit demo: circular orbit + suborbital fall (Newton cannon story)
G, M, R = 6.67430e-11, 5.97237e24, 6371000.0
v1 = float(np.sqrt(G * M / R))
T = 2 * np.pi * np.sqrt(R ** 3 / (G * M))

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect("equal")
ax.set_xlim(-1.4 * R, 1.4 * R)
ax.set_ylim(-1.4 * R, 1.4 * R)
earth = plt.Circle((0, 0), R, color="#3b82f6", alpha=0.25)
ax.add_patch(earth)
ax.add_patch(plt.Circle((0, 0), R, color="#3b82f6", fill=False, lw=2))
trail, = ax.plot([], [], "r-", lw=1.5, alpha=0.8)
ball, = ax.plot([], [], "ro", ms=10)
ax.set_title("Newton cannon: 7.9 km/s = orbit, slower = falls back")
ax.set_xlabel("x (m)")
ax.text(0, -1.3 * R, "red dot = steel ball in orbit", ha="center", fontsize=9)

theta = np.linspace(0, 2 * np.pi, 120)
xs, ys = R * np.cos(theta), R * np.sin(theta)

def update(i):
    trail.set_data(xs[: i + 1], ys[: i + 1])
    ball.set_data([xs[i]], [ys[i]])
    return trail, ball

anim = FuncAnimation(fig, update, frames=len(theta), interval=66, blit=True)
anim.save("docs/media/demo.mp4", writer="ffmpeg", fps=15, dpi=120,
          extra_args=["-vcodec", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p"])
plt.close(fig)

# GIF: shorter, smaller (best practice <8MB, 12fps, 480-720px)
fig2, ax2 = plt.subplots(figsize=(4.8, 4.8))
ax2.set_aspect("equal")
ax2.set_xlim(-1.4 * R, 1.4 * R)
ax2.set_ylim(-1.4 * R, 1.4 * R)
ax2.add_patch(plt.Circle((0, 0), R, color="#3b82f6", alpha=0.25))
trail2, = ax2.plot([], [], "r-", lw=1.5)
ball2, = ax2.plot([], [], "ro", ms=8)
ax2.set_title("orbit in 8 seconds")
idx = np.linspace(0, len(theta) - 1, 72).astype(int)

def update2(k):
    i = idx[k]
    trail2.set_data(xs[: i + 1], ys[: i + 1])
    ball2.set_data([xs[i]], [ys[i]])
    return trail2, ball2

anim2 = FuncAnimation(fig2, update2, frames=len(idx), interval=110, blit=True)
anim2.save("docs/media/demo.gif", writer="pillow", fps=12, dpi=80)
plt.close(fig2)
print("demo assets written")
