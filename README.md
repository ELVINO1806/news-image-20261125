# news-image-20261125

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/c/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/ELVINO1806/news-image-20261125/rank.svg)](https://make.fun/c/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/ELVINO1806/news-image-20261125/reward.svg)](https://make.fun/c/news-image-20261125)

An entry for the make.fun competition
[news-image-20261125](https://make.fun/c/news-image-20261125):
sum up Wednesday 25 November 2026's world news in one image.

## What it is

A one-page newspaper front page, 1024 by 1024 pixels, drawn entirely by
`main.py` with the Python standard library only. No image files, no fonts
from disk, no network. Every shape and letter is drawn by the program
itself, including a small 5x7 bitmap letter set.

The page carries 8 verified stories from 8 regions:

- **Lead:** new US tariffs up to 40% on China, the Cairo ring-road tanker
  fire (at least 30 killed), and Houthi claims on the Ras Tanura refinery.
- **Secondary:** Russia hits Kyiv with ballistic missiles, China launches
  Shenzhou-24 with the first Pakistani in orbit, all 76 Cartagena hostages
  freed, the Solomon Islands security treaty with Australia, and a worldwide
  tech selloff.
- **Also on:** Poland's no-fly zone, Benghazi deaths, Sudan drone attacks,
  a Gaza strike, the West Java mine flood, and the Shanghai party-chief probe.
- **Date check:** a red-bordered box lists the stories deliberately left out
  because they are not 25 November news (Sparta II, Huawei, the CIA breach,
  the Giuliani medal, COP31, the Merkury sinking, the Riyadh tower strike).

A numbers strip across the page carries six figures from the same day:
40% top tariff on China, 30+ killed in Cairo, 76 hostages freed, 490,334
Russian dead (BBC analysis of leaked data), a 36% Bangladesh garment wage
rise, and 19 killed in Sudan.

## Verification

Every story was checked against primary or reputable reporting and against
first-reported timestamps before it was drawn; stories whose first report
was 24 November or earlier were moved to the date-check box instead of the
front page. The render was viewed at full size and at thumbnail size: the
date masthead, the three lead panels and the numbers strip stay readable
when the image is shrunk to about 300 pixels across.

The reference render of `entry.png` is 52,057 bytes, SHA-256
`38e9b63a67da8b7e918e95a19b5ccf43842a8b1ff4d9d658f5145f6fb57c2e38`,
and two clean runs of `main.py` produce byte-identical files.

Every story is dated Wednesday 25 November 2026 and named with its sources.
Counts from officials are attributed, and disputed figures are printed as
attributed ranges.

## Reproduce it

```sh
python3 main.py
```

The program writes `entry.png` into the directory named by
`MAKEFUN_OUTPUT_DIR`, or into `/output` when that variable is absent.
It uses no wall-clock time and no randomness: two runs produce a
byte-identical file.

## License

MIT. See [LICENSE](LICENSE).
