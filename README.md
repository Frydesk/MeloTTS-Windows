# Install Steps on Windows

1. Clone the repository
```
git clone https://github.com/natlamir/MeloTTS-Windows.git
cd MeloTTS-Windows
```

2. Create conda environment and install dependencies
```
conda env create -f environment.yml
conda activate melotts-win
pip install -e .
python -m unidic download
```
If you have trouble doing the download with the `python -m unidic download` you can try this:

- Download the zip from: https://cotonoha-dic.s3-ap-northeast-1.amazonaws.com/unidic-3.1.0.zip
- Place it in: C:\Users\YOUR_USER_ID\miniconda3\envs\melotts-win\Lib\site-packages\unidic
- Rename it to unidic.zip
- Replace the downalod.py file in this same directory with the one from https://github.com/natlamir/ProjectFiles/blob/main/melotts/download.py
- Now re-run the `python -m unidic download`. This info originally gotten from: https://github.com/myshell-ai/MeloTTS/issues/62#issuecomment-2067361999

3. Install pytorch
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

4. Run using:
```
melo-ui
```

# Local Training on Windows
1. In the `melo/data/example` folder, delete the example `metadata.list` file.
2. If you need to convert mp3 to wav, create a folder called `mp3s` in the example folder and copy all your mp3 files into the `mp3s` folder
3. With a conda window activated with the enviroment open in the `melo` folder, run `ConvertMp3toWav.bat` from the conda prompt. This will create a folder `data/example/wavs` with all of the converted wav files.
4. Create a transcript file by running `python transcript.py` which will create a `data/example/metadata.list` file.
5. Run `python preprocess_text.py --metadata data/example/metadata.list` to create the `train.list`, `config.json`, among other files in the `data/example` folder.
6. Modify `config.json` to change the batch size, epochs, learning rate, etc.
7. From the conda prompt run `train.bat` to start the training.
8. File will be created within the `data/example/config` folder with the checkpoints and other logging information.
9. To test out a checkpoint, run: `python infer.py --text "this is a test" -m "C:\ai\MeloTTS-Windows\melo\data\example\config\G_0.pth" -o output` changing the G_0 to the checkpoint you want to test with G_1000, G2000, etc.
10. When you want to use a checkpoint from the UI, create a `melo/custom` folder and copy the .pth and `config.json` file over from the `data/example/config`, rename the .pth to a user-friendly name, and launch the UI to see it in the custom voice dropdown.
11. To see the tensorboard, install `pip install tensorflow`
12. Run `tensorboard --logdir=data\example\config`
13. This will give you the local URL to view the tensorboard.

# Original Readme:
<div align="center">
  <div>&nbsp;</div>
  <img src="logo.png" width="300"/> 
</div>

## Introduction
MeloTTS is a **high-quality multi-lingual** text-to-speech library by [MIT](https://www.mit.edu/) and [MyShell.ai](https://myshell.ai). Supported languages include:

| Language | Example |
| --- | --- |
| English (American)    | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/en/EN-US/speed_1.0/sent_000.wav) |
| English (British)     | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/en/EN-BR/speed_1.0/sent_000.wav) |
| English (Indian)      | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/en/EN_INDIA/speed_1.0/sent_000.wav) |
| English (Australian)  | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/en/EN-AU/speed_1.0/sent_000.wav) |
| English (Default)     | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/en/EN-Default/speed_1.0/sent_000.wav) |
| Spanish               | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/es/ES/speed_1.0/sent_000.wav) |
| French                | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/fr/FR/speed_1.0/sent_000.wav) |
| Chinese (mix EN)      | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/zh/ZH/speed_1.0/sent_008.wav) |
| Japanese              | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/jp/JP/speed_1.0/sent_000.wav) |
| Korean                | [Link](https://myshell-public-repo-host.s3.amazonaws.com/myshellttsbase/examples/kr/KR/speed_1.0/sent_000.wav) |

Some other features include:
- The Chinese speaker supports `mixed Chinese and English`.
- Fast enough for `CPU real-time inference`.

## Usage
- [Use without Installation](docs/quick_use.md)
- [Install and Use Locally](docs/install.md)
- [Training on Custom Dataset](docs/training.md)

The Python API and model cards can be found in [this repo](https://github.com/myshell-ai/MeloTTS/blob/main/docs/install.md#python-api) or on [HuggingFace](https://huggingface.co/myshell-ai).

## Join the Community

**Discord**

Join our [Discord community](https://discord.gg/myshell) and select the `Developer` role upon joining to gain exclusive access to our developer-only channel! Don't miss out on valuable discussions and collaboration opportunities.

**Contributing**

If you find this work useful, please consider contributing to this repo.

- Many thanks to [@fakerybakery](https://github.com/fakerybakery) for adding the Web UI and CLI part.

## Authors

- [Wenliang Zhao](https://wl-zhao.github.io) at Tsinghua University
- [Xumin Yu](https://yuxumin.github.io) at Tsinghua University
- [Zengyi Qin](https://www.qinzy.tech) at MIT and MyShell

**Citation**
```
@software{zhao2024melo,
  author={Zhao, Wenliang and Yu, Xumin and Qin, Zengyi},
  title = {MeloTTS: High-quality Multi-lingual Multi-accent Text-to-Speech},
  url = {https://github.com/myshell-ai/MeloTTS},
  year = {2023}
}
```

## License

This library is under MIT License, which means it is free for both commercial and non-commercial use.

## Acknowledgements

This implementation is based on [TTS](https://github.com/coqui-ai/TTS), [VITS](https://github.com/jaywalnut310/vits), [VITS2](https://github.com/daniilrobnikov/vits2) and [Bert-VITS2](https://github.com/fishaudio/Bert-VITS2). We appreciate their awesome work.
