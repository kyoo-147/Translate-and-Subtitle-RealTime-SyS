# -*- coding: utf-8 -*-
# Author: mihcuog@AILab
# Contatct: AI-Lab - Smart Things
# File subtitle and translate in video

import whisper
from whisper.tokenizer import LANGUAGES, TO_LANGUAGE_CODE
import argparse
import os
import pysrt
from googletrans import Translator
import googletrans
from gooey import Gooey
from datetime import datetime, timedelta

def translate_separate(srt,translang):
    translator = Translator()
    subs = pysrt.open(srt)
    new_subs = pysrt.SubRipFile()
    for sub in subs:
        translation = translator.translate(sub.text, dest=translang)
        new_sub = pysrt.SubRipItem(
            index=sub.index,
            start=sub.start,
            end=sub.end,
            text=translation.text
        )
        new_subs.append(new_sub)

    new_subs.save(srt[:-4] + '_translated.srt', encoding='utf-8')

def write_srt_file(subs, file, translang=None):
    translator = Translator() if translang else None

    for i, sub in enumerate(subs, start=1):
        start_time = datetime(1, 1, 1) + timedelta(seconds=sub["start"])
        end_time = datetime(1, 1, 1) + timedelta(seconds=sub["end"])
        text = sub["text"].strip()

        if translator:
            translation = translator.translate(text, dest=translang)
            text += "\n"+translation.text

        print(
            f"{i}\n{start_time:%H:%M:%S},{start_time.microsecond // 1000:03d} "
            f"-->{end_time:%H:%M:%S},{end_time.microsecond // 1000:03d}\n"
            f"{text}\n",
            file=file,
            flush=True
        )
@Gooey()
def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("audio", nargs="+", type=str, help="Name of audio file(s) to transcribe")
    parser.add_argument("--model", default="small",
                        choices=whisper.available_models(), help="Name of the Whisper model to use")
    parser.add_argument("--output_dir", "-o", type=str,
                        default=".", help="Directory to save the outputs")
    parser.add_argument("--language", type=str, default=None, choices=sorted(LANGUAGES.keys()) + sorted([k.title() for k in TO_LANGUAGE_CODE.keys()]),
                        help="Language spoken in the audio, skip to perform language detection")
    parser.add_argument("--translang", type=str, default=None, choices=sorted(googletrans.LANGUAGES.values()) + sorted([k for k in googletrans.LANGUAGES.keys()]),
                        help="Language will be translated")
    parser.add_argument("--dualsrt", type=str, default='Y', choices=['N','Y'],
                        help="Save original text and translation in one srt")

    args = parser.parse_args().__dict__
    model_name: str = args.pop("model")
    output_dir: str = args.pop("output_dir")
    translate_lang: str = args.pop("translang")
    dual_srt: str = args.pop("dualsrt")
    os.makedirs(output_dir, exist_ok=True)

    if model_name.endswith(".en"):
        args["language"] = "en"

    model = whisper.load_model(model_name)
    for audio_path in args.pop("audio"):
        result = model.transcribe(audio_path, **args)
        srt_path = os.path.join(output_dir, f"{audio_path[:-4]}.srt")
        with open(srt_path, 'w', encoding="utf-8") as srt:
            if translate_lang and dual_srt in ['Y']:
                write_srt_file(result["segments"],srt,translate_lang)
            else:
                write_srt_file(result["segments"],srt)
                if translate_lang:
                    translate_separate(srt_path, translate_lang)

if __name__ == '__main__':
    main()
