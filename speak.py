"""Run the QnVoice Cebuano voice profile using a local VoxCPM2 GGUF CLI."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent


def verify(path, asset):
    if not path.is_file() or path.stat().st_size != asset["bytes"]:
        return False
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest() == asset["sha256"]


def download(url, path, asset):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=path.parent) as temporary:
        staged = Path(temporary) / path.name
        print(f"Downloading {path.name}", flush=True)
        with urlopen(url, timeout=120) as response, staged.open("wb") as file:
            shutil.copyfileobj(response, file, length=1024 * 1024)
        if not verify(staged, asset):
            raise SystemExit(f"SHA-256 mismatch for {path.name}.")
        staged.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", type=Path, default=ROOT / "weights")
    parser.add_argument("--fetch", action="store_true", help="Download the exact shared weights before running.")
    parser.add_argument("--verify", action="store_true", help="Verify files and stop before synthesis.")
    parser.add_argument("--runner", default="voxcpm2-cli")
    parser.add_argument("--research-reference", action="store_true", help="Use the separate reference tested in the paper.")
    parser.add_argument("--text", default="Maayong buntag.")
    parser.add_argument("--output", type=Path, default=Path("cebuano.wav"))
    args = parser.parse_args()
    if not args.text.strip():
        parser.error("--text must contain a phrase")

    config = json.loads((ROOT / "voice-config.json").read_text(encoding="utf-8"))
    shared = config["shared_weights"]
    source = f"https://huggingface.co/{shared['repository']}/resolve/{shared['revision']}"
    for name, asset in shared["files"].items():
        path = args.weights / name
        if not verify(path, asset):
            if not args.fetch:
                parser.exit(1, f"Missing or mismatched weight {path}. Run once with --fetch.\n")
            download(f"{source}/{name}", path, asset)
        print(f"Verified {name}", flush=True)

    key = "research_reference" if args.research_reference else "reference"
    reference = "research-reference.wav" if args.research_reference else "voice-reference.wav"
    for name, asset in config[key]["files"].items():
        if not verify(ROOT / name, asset):
            parser.exit(1, f"Missing or mismatched voice reference file {name}.\n")
    if args.verify:
        return
    runner = shutil.which(args.runner)
    if runner is None:
        parser.error("Install the pinned VoxCPM2 CLI or pass its executable with --runner.")
    synthesis = config["synthesis"]
    subprocess.run(
        [runner, "--text", args.text.strip(), "--reference", str(ROOT / reference), "--output", str(args.output),
         "--stream", "--steps", "93", "--timesteps", str(synthesis["flow_steps"]),
         "--cfg", str(synthesis["cfg"]), "--seed", str(synthesis["seed"]),
         str(args.weights / "voice-language.gguf"), str(args.weights / "voice-acoustic.gguf")],
        check=True,
    )


if __name__ == "__main__":
    main()
