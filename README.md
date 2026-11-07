# Offline Cebuano Text to Speech in QnVoice for iOS

This repository contains the Cebuano voice profile used by QnVoice, the evaluation record, and audio generated on an iPhone 15 Pro and an Apple M1 Pro. The profile uses a synthetic voice reference and its encoded AudioVAE features with QnVoice's quantized VoxCPM2 weights.

- [Cebuano model on Hugging Face](https://huggingface.co/CholoAsis/qnvoice-cebuano-voxcpm2)
- [Exact published voice profile](https://huggingface.co/CholoAsis/qnvoice-cebuano-voxcpm2/tree/a7cd9a9220634ac973384676efab06174ff9cdc7)
- [Research white paper (10-page PDF)](QnVoice-Cebuano-Text-to-Speech-for-iOS.pdf)
- [Per-phrase evaluation results](benchmarks/evaluation.json)

## Use in QnVoice

In QnVoice for iOS, choose **Speak → Cebuano**. Select Cebuano in **Type** to read your words directly, or choose English to translate them before playback. The app uses a separate bundled English-to-Cebuano translator. Cebuano synthesis requires a device with at least 6 GB of memory.

## Listen

| Cebuano phrase | Source | Audio |
| --- | --- | --- |
| Maayong buntag. | iPhone 15 Pro | [WAV](samples/iphone-1.wav) |
| Daghang salamat sa imong tabang. | iPhone 15 Pro | [WAV](samples/iphone-2.wav) |
| Kumusta ka? Asa ta mangaon? | iPhone 15 Pro | [WAV](samples/iphone-5.wav) |
| Tagpila ang usa ka kilo nga mangga? | Apple M1 Pro | [WAV](samples/sample-mangoes.wav) |

The six iPhone 15 Pro requests reached playback in 3.14–4.67 seconds, with a median of 3.54 seconds across the five later requests. On 16 paired desktop phrases, automated transcription of the selected reference produced 3.32% character error and 18.89% word error. The paper describes the sample set, model selection, and limits of those measurements.

## Run locally

Build the [pinned VoxCPM2 GGUF CLI](https://github.com/tc-mb/llama.cpp-omni/tree/e0eca9d8f57ac8f5a5ad6191a8007b93436c1e71/tools/omni/voxcpm2) and make it available as `voxcpm2-cli` on your path. The first command downloads and verifies the two shared GGUF files, which total about 2.08 GB. The second command uses the local files. [Pinned shared weights](https://huggingface.co/CholoAsis/qnvoice-filipino-voxcpm2-gguf/tree/5b912ca3328145b384134040dcc520114f000e32)

```sh
python3 speak.py --fetch --verify
python3 speak.py --text 'Maayong buntag.' --output cebuano.wav
```

Use `--weights /path/to/weights` to reuse existing verified files, `--runner /path/to/voxcpm2-cli` to select an executable, or `--research-reference` to hear the second reference evaluated in the paper. The runner verifies the reference files and GGUF weights against [voice-config.json](voice-config.json). To verify the files in this repository, run `shasum -a 256 -c SHA256SUMS`.

## License and attribution

The shared VoxCPM2 weights use Apache 2.0. QnSub Software Solutions permits personal and commercial use of the synthetic references with a citation requirement for apps. [Reference terms](LICENSE) · [Apache 2.0 license](Apache-2.0.txt) · [Attribution](NOTICE)
