# Manga Splitter
Split landscape manga into portrait to protect your eyes.

Works for both zip or directory.

### Usage
Suppose directory of manga contains multiple episodes in zip (default)/directory

```
python3 MangaSplitter.py [-dir] [-l2r] [-single] path
```
`-dir` if manga episode is in directory

`-l2r` if each page is from left to right (default right to left)

`-single` if the path is an episode rather than a dir w/ multiple episodes


Output directory is `{path}_split`
