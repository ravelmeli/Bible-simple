"""Generate a background music bed locally with MusicGen (facebook/musicgen-small).

Usage (needs torch, transformers, scipy; weights download from Hugging Face on first run):
    python3 gen_music.py <out.wav> <seconds> [seed] [prompt]

Two 30 s segments are generated with different seeds and cross-faded, so any length up to about 55 s works.
Licence note: the musicgen-small weights are published under CC-BY-NC 4.0 (non-commercial). Whether the
generated audio can be used in monetised videos is not settled; keep the track listed in CREDITS.md.
"""
import sys
import time

import numpy as np
import scipy.io.wavfile as wavfile
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration

PROMPT = ("slow solemn cinematic ambient score, warm low cello and soft string pad, gentle ancient "
          "middle-eastern atmosphere, mysterious and hopeful, sparse and calm, no drums, no vocals")
SEGMENT_TOKENS = 1500  # 50 tokens per second, so 30 s


def main(out, seconds, seed=7, prompt=PROMPT):
    torch.set_num_threads(4)
    proc = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
    sr = model.config.audio_encoder.sampling_rate
    inputs = proc(text=[prompt], padding=True, return_tensors="pt")
    pieces = []
    # Each 30 s segment adds 25 s once cross-faded by 5 s.
    n_segments = 1 if seconds <= 30 else 1 + int(np.ceil((seconds - 30) / 25))
    for k in range(n_segments):
        torch.manual_seed(seed + k)
        t0 = time.time()
        audio = model.generate(**inputs, do_sample=True, guidance_scale=3.0, max_new_tokens=SEGMENT_TOKENS)
        pieces.append(audio[0, 0].numpy())
        print(f"segment {k + 1}/{n_segments}: {len(pieces[-1]) / sr:.1f} s generated in {time.time() - t0:.0f} s", flush=True)
    xf = int(5 * sr)
    track = pieces[0]
    for nxt in pieces[1:]:
        fade = np.linspace(0, 1, xf)
        track = np.concatenate([track[:-xf], track[-xf:] * (1 - fade) + nxt[:xf] * fade, nxt[xf:]])
    track = track[: int(seconds * sr)]
    peak = float(np.max(np.abs(track))) or 1.0
    wavfile.write(out, sr, (track / peak * 0.9 * 32767).astype(np.int16))
    print(f"wrote {out}: {len(track) / sr:.1f} s at {sr} Hz")


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 7,
         sys.argv[4] if len(sys.argv) > 4 else PROMPT)
