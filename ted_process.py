import os
import re
from pathlib import Path
from progress.bar import Bar
import pysrt


class LrcItem:
    def __init__(self, start: list, end: list = [], text: str = "", honyaku: str = ""):
        self.start = start[:3]
        self.end = end[:3]
        self.text = text
        self.honyaku = honyaku

    def __str__(self):
        lrc_str = "[{:0>2d}:{:0>2d}.{:0>2d}]".format(*self.start)
        if self.text:
            lrc_str += self.text
        if self.honyaku:
            lrc_str += " / "
            lrc_str += self.honyaku
        lrc_str += "\n"
        if self.end:
            lrc_str += "[{:0>2d}:{:0>2d}.{:0>2d}]\n".format(*self.end)
        return lrc_str


def testLrcItem(*args, **kwargs):
    lrcItem = LrcItem(*args, **kwargs)
    print(str(lrcItem))
    print(lrcItem)
    pass


class Srt2Lrc:
    def __init__(
        self, srtItems, ti="", al="TED-Japanese", ar="TED", by="@lijunjie2232"
    ):
        self.head = f"[ti:{ti}]\n" + f"[ar:{al}]\n" + f"[al:{al}\n" + f"[by:{by}]\n"

        self.lrcs = []
        for srtItem in srtItems:
            self.lrcs.append(self.parse(srtItem))

    def parse(self, srtItem):
        start_time = list(srtItem.start)
        start_time[1] += 60 * start_time[0]
        start_time[3] //= 10
        start_time = start_time[1:]
        # end_time = list(srtItem.end)
        # end_time[1] += 60 * end_time[0]
        # end_time[3] //= 10
        # end_time = end_time[1:]

        # return LrcItem(start_time, end_time, srtItem.text)

        return LrcItem(start_time, [], srtItem.text)

    def __str__(self):
        return self.head + "".join([str(lrc) for lrc in self.lrcs])

    def save(self, path="./", overwrite=False):
        if Path(path).is_file() and not overwrite:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.__str__())


if __name__ == "__main__":
    testLrcItem([0, 12, 52], [0, 15, 52])
    testLrcItem(
        [00, 20, 00],
        [00, 38, 72],
        "やっと眼を覚ましたかい それなのになぜ眼も合わせやしないんだい？",
        "总算醒来了吗  可为何还是不愿与我对视呢？",
    )

    LANG = "ja"
    srt_path = Path("D:\\Videos\\4K Video Downloader\\TEDx talks in Japanese\\srt")
    lrc_path = Path("D:\\Videos\\4K Video Downloader\\TEDx talks in Japanese\\lrc")

    lyric_pattern = re.compile("(?P<file_name>[\d]{4}\.(?P<title>.*))\.ja\.srt")

    for file in Bar("Processing:", fill=">", bar_prefix="[", bar_suffix="]").iter(
        os.listdir(srt_path)
    ):
        # time.sleep(0.01)
        if not file.endswith(".%s.srt" % LANG):
            continue
        srtItems = pysrt.open(srt_path / file)
        filename_match = lyric_pattern.match(file)
        lrc = Srt2Lrc(srtItems, ti=filename_match["title"])
        lrc.save(lrc_path / (filename_match["file_name"] + ".lrc"), True)
        pass
