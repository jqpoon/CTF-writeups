# just_an_image

Since the flag can't be found by just looking at the image, it is probably hidden in the metadata or some other part of the file.

We start by running `exiftool` on the image.

```bash
$ exiftool logo.jpg
ExifTool Version Number         : 12.16
File Name                       : logo.jpg
Directory                       : .
...
Artist                          : HTF{
...
Copyright                       : wh3r3_th3r3_4r3_
...
Title                           : 5tr1ng5_th3r3_1s_h0p3
Author                          : }
...
```

Since flag contents are normally written in `l33tsp34k`, seeing such strings confirm that we are on the right track.

`HTF{wh3r3_th3r3_4r3_5tr1ng5_th3r3_1s_h0p3}`