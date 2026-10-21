"""Word-level French transcription with Whisper large-v3 through faster-whisper (CTranslate2, int8 on CPU).

Fallback for when `hyperframes transcribe` crashes with SIGILL, and for when the transformers pipeline is
OOM-killed (float32 and bfloat16 both exceeded 14 GB for word timestamps on a 16 GB machine).

Usage: python3 transcribe_pt.py <audio.wav> <out transcript.json>
Writes [{"text": ..., "start": ..., "end": ...}, ...], the format `montage/common.py` reads.
"""
import json
import subprocess
import sys
import time

import numpy as np
from faster_whisper import WhisperModel


def load_16k(path):
    # Decode with ffmpeg: faster-whisper's own decoder needs a newer PyAV than the one pip resolves.
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def merge_tokens(words):
    """faster-whisper splits « c'était » into « c » + « 'était » and « -t-elle » into pieces: glue them back."""
    out = []
    for w in words:
        t = w["text"]
        if out and (t.startswith(("'", "\u2019", "-")) or out[-1]["text"].endswith(("'", "\u2019", "-", "\u00ab"))):
            out[-1]["text"] += t
            out[-1]["end"] = w["end"]
        elif t in ("\u00bb", "?", "!", ":", ";") and out:
            out[-1]["text"] += t
            out[-1]["end"] = w["end"]
        else:
            out.append(dict(w))
    return out


def main(audio, out):
    t0 = time.time()
    model = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
    print(f"model loaded in {time.time() - t0:.0f} s", flush=True)
    t0 = time.time()
    segments, info = model.transcribe(load_16k(audio), language="fr", word_timestamps=True, beam_size=5,
                                      vad_filter=False, condition_on_previous_text=False)
    words = []
    for seg in segments:
        for w in seg.words:
            words.append({"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)})
    words = merge_tokens(words)
    print(f"transcribed {info.duration:.1f} s of audio in {time.time() - t0:.0f} s", flush=True)
    json.dump(words, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"wrote {out}: {len(words)} words")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
