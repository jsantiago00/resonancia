"""Analiza canciones con el mismo procesamiento de audio que usa la app (index.html)
y calcula medidas para distinguir el "ánimo" de la música.

Uso:  python herramientas/analizar.py canciones/*.mp3
"""
import json
import sys
from pathlib import Path

import miniaudio
import numpy as np

SR = 44100
FFT = 2048
HOP = SR // 60          # un cuadro por fotograma (60 fps)
NB = 64
MIN_DB, MAX_DB = -85.0, -20.0
WIN_S = 8.0             # ventana de análisis (segundos)


def decode(path):
    d = miniaudio.decode_file(str(path), output_format=miniaudio.SampleFormat.FLOAT32, nchannels=1, sample_rate=SR)
    return np.frombuffer(d.samples, dtype=np.float32).copy()


def band_edges():
    nyq = SR / 2
    n = FFT // 2
    edges = []
    for i in range(NB):
        f0 = 30 * (12000 / 30) ** (i / NB)
        f1 = 30 * (12000 / 30) ** ((i + 1) / NB)
        b0 = int(np.floor(f0 / nyq * n))
        b1 = max(b0 + 1, int(np.ceil(f1 / nyq * n)))
        edges.append((b0, b1))
    return edges


def bands_over_time(x):
    """Imita AnalyserNode.getByteFrequencyData (ventana Blackman, suavizado 0.55, dB -> 0..1)."""
    win = np.blackman(FFT).astype(np.float32)
    edges = band_edges()
    frames = (len(x) - FFT) // HOP
    out = np.zeros((frames, NB), np.float32)
    smooth = np.zeros(FFT // 2, np.float32)
    for k in range(frames):
        seg = x[k * HOP:k * HOP + FFT] * win
        mag = np.abs(np.fft.rfft(seg))[:FFT // 2] / FFT
        smooth = 0.55 * smooth + 0.45 * mag
        db = 20 * np.log10(smooth + 1e-12)
        byte = np.clip((db - MIN_DB) / (MAX_DB - MIN_DB), 0, 1)
        for i, (b0, b1) in enumerate(edges):
            out[k, i] = byte[b0:b1].mean()
    return out


def features(B):
    """Medidas por ventana de 8 s (con paso de 2 s)."""
    flux = np.maximum(np.diff(B, axis=0), 0).sum(axis=1)          # cambio espectral (golpes)
    bflux = np.abs(np.diff(B[:, :10], axis=0)).mean(axis=1)        # movimiento del bajo (wobble)
    hflux = np.abs(np.diff(B[:, 36:], axis=0)).mean(axis=1)        # movimiento de agudos
    loud = B.mean(axis=1)
    bass = B[:, :8].mean(axis=1)
    mid = B[:, 8:30].mean(axis=1)
    high = B[:, 36:].mean(axis=1)
    W, step = int(WIN_S * 60), 120
    rows = []
    for s in range(0, len(flux) - W, step):
        f = flux[s:s + W]
        fz = f - f.mean()
        ac = np.correlate(fz, fz, 'full')[W - 1:]
        ac /= ac[0] + 1e-9
        lo, hi = int(0.3 * 60), int(1.2 * 60)                       # 50..200 BPM
        lag = lo + int(np.argmax(ac[lo:hi]))
        # golpes: picos de flux sobre un umbral adaptativo
        thr = np.convolve(f, np.ones(30) / 30, 'same') * 1.4 + 0.02
        peaks = np.sum((f[1:-1] > thr[1:-1]) & (f[1:-1] >= f[:-2]) & (f[1:-1] >= f[2:]))
        sl = slice(s, s + W)
        rows.append(dict(
            t=s / 60,
            loud=float(loud[sl].mean()),
            bass=float(bass[sl].mean()),
            mid=float(mid[sl].mean()),
            high=float(high[sl].mean()),
            bright=float(high[sl].mean() / (bass[sl].mean() + 1e-3)),
            flux=float(f.mean()),
            fluxVar=float(f.std() / (f.mean() + 1e-6)),
            onsets=float(peaks / WIN_S),
            regular=float(ac[lag]),
            bpm=float(60 * 60 / lag),
            dyn=float(loud[sl].std()),
            bassRel=float(bass[sl].mean() - mid[sl].mean()),
            bflux=float(bflux[sl].mean()),
            hflux=float(hflux[sl].mean()),
        ))
    return rows


def main():
    out = {}
    for p in sys.argv[1:]:
        p = Path(p)
        print(f'Analizando {p.name}...', flush=True)
        B = bands_over_time(decode(p))
        rows = features(B)
        out[p.stem] = rows
        keys = [k for k in rows[0] if k != 't']
        print(f'  {len(rows)} ventanas')
        for k in keys:
            v = np.array([r[k] for r in rows])
            print(f'  {k:8s} p10={np.percentile(v, 10):7.3f}  mediana={np.median(v):7.3f}  p90={np.percentile(v, 90):7.3f}')
    dest = Path(__file__).with_name('analisis.json')
    dest.write_text(json.dumps(out), encoding='utf-8')
    print('Guardado en', dest)


if __name__ == '__main__':
    main()
