"""Synthesize the sound bed and effects for the shorts (original sounds, no licence to credit).

Usage: python3 synth_audio.py <output_dir> <duration_seconds>

Writes into <output_dir>:
  ambiance.wav   dark evolving pad (A minor), meant to sit well under the voice
  riser.wav      1.4 s rising sweep before a reveal
  hit.wav        low impact (sub drop + soft noise thump)
  tick.wav       tiny paper-like tick for text pops
"""
import sys
import wave
import numpy as np

SR = 44100


def write(path, x, peak=0.9):
    x = np.asarray(x, dtype=np.float64)
    m = np.max(np.abs(x)) or 1.0
    x = x / m * peak
    pcm = (x * 32767).astype(np.int16)
    if pcm.ndim == 1:
        pcm = np.stack([pcm, pcm], axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def lowpass(x, cutoff):
    # One-pole low-pass in the frequency domain (deterministic, no extra dependencies).
    n = len(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    X = np.fft.rfft(x)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, n)


def ambiance(duration):
    t = np.arange(int(duration * SR)) / SR
    rng = np.random.default_rng(7)
    out = np.zeros_like(t)
    # Slow chord drift: A minor (A, C, E) with the third entering later for a darker colour.
    notes = [(55.0, 1.0, 0.0), (82.41, 0.7, 0.0), (110.0, 0.55, 0.0), (130.81, 0.35, 6.0), (164.81, 0.22, 12.0)]
    for f, amp, enter in notes:
        env = np.clip((t - enter) / 6.0, 0, 1)
        for detune in (-0.35, 0.0, 0.35):
            lfo = 0.75 + 0.25 * np.sin(2 * np.pi * (0.05 + 0.013 * f / 55) * t + f)
            out += amp * env * lfo * (np.sin(2 * np.pi * (f + detune) * t)
                                      + 0.35 * np.sin(2 * np.pi * 2 * (f + detune) * t)
                                      + 0.12 * np.sin(2 * np.pi * 3 * (f + detune) * t)) / 3
    # Sub-bass breathing.
    out += 0.9 * np.sin(2 * np.pi * 36.7 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t))
    # Air: band-limited noise that swells slowly.
    noise = lowpass(rng.standard_normal(len(t)), 2500)
    noise -= lowpass(noise, 400)
    out += 0.05 * noise * (0.5 + 0.5 * np.sin(2 * np.pi * 0.09 * t + 1.3))
    fade = np.clip(t / 2.0, 0, 1) * np.clip((duration - t) / 2.0, 0, 1)
    return lowpass(out, 900) * fade


def riser(length=1.4):
    t = np.arange(int(length * SR)) / SR
    f = 180 + 900 * (t / length) ** 2
    phase = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(phase) + 0.4 * np.sin(2 * phase)
    rng = np.random.default_rng(3)
    noise = rng.standard_normal(len(t))
    noise = noise - lowpass(noise, 1500)
    env = (t / length) ** 1.6
    return (tone * 0.6 + noise * 0.5) * env * np.clip((length - t) / 0.03, 0, 1)


def hit(length=1.1):
    t = np.arange(int(length * SR)) / SR
    f = 38 + 110 * np.exp(-t * 14)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    rng = np.random.default_rng(11)
    thump = lowpass(rng.standard_normal(len(t)), 700) * np.exp(-t * 18)
    return sub + 0.5 * thump


def tick(length=0.09):
    t = np.arange(int(length * SR)) / SR
    rng = np.random.default_rng(5)
    n = rng.standard_normal(len(t))
    n = n - lowpass(n, 1800)
    return n * np.exp(-t * 55) + 0.3 * np.sin(2 * np.pi * 620 * t) * np.exp(-t * 70)


if __name__ == "__main__":
    out_dir, duration = sys.argv[1], float(sys.argv[2])
    write(f"{out_dir}/ambiance.wav", ambiance(duration), 0.8)
    write(f"{out_dir}/riser.wav", riser(), 0.9)
    write(f"{out_dir}/hit.wav", hit(), 0.95)
    write(f"{out_dir}/tick.wav", tick(), 0.8)
    print("ok")
