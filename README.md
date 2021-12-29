# Manga Splitter
Split landscape manga in portraits to protect your eyes.

Works well for both zip or directory.

<div align="center"><img src="./.github/original.jpg" style="zoom:20%;" /></div>

### Usage
Suppose directory of manga contains multiple episodes in zip /directory

```
python3 MangaSplitter.py [-dir] [-l2r] [-single] path
```
`-dir` if manga episode is in directory

`-l2r` if each page is from left to right (default right to left)

`-single` if the path is an episode rather than a dir w/ multiple episodes


Output directory is `{path}_split`
