import os
import io
import zipfile
from enum import Enum
from PIL import Image
import argparse

Mode = Enum('Mode', 'zip dir')
PageMode = Enum('PageMode', 'R2L L2R')
ImageExt = ('jpg', 'png')


def getFileName(page_num, ext):
    return f"{page_num:03}{ext}"


class MangaSplitter():
    def __init__(self) -> None:
        pass

    def split(self, path, multiple=True, mode=Mode.zip, page_mode=PageMode.R2L):
        self.mode = mode
        self.page_mode = page_mode
        mangas = self.__get_mangas(path) if multiple else [path]
        save_dir = os.path.join(os.path.dirname(
            path), f"{os.path.basename(path)}_split")
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for manga in mangas:
            print(f"Processing: {manga}")
            page_num = 0
            out_name = os.path.join(save_dir, os.path.basename(
                manga)) if multiple else save_dir
            if self.mode == Mode.zip:
                m_zip = zipfile.ZipFile(manga)
                out_zip = zipfile.ZipFile(out_name, 'w')
            else:
                m_zip = None
                if not os.path.exists(out_name):
                    os.mkdir(out_name)

            pages = self.__get_pages(manga, m_zip)
            _, ext = os.path.splitext(pages[0])
            save_format = 'PNG' if ext.endswith('png') else 'jpeg'
            for page in pages:
                splitted_imgs = self.__split_page(
                    m_zip.open(page) if m_zip else os.path.join(manga, page))
                for im in splitted_imgs:
                    im_name = getFileName(page_num, ext)
                    if m_zip:
                        img_byte_arr = io.BytesIO()
                        im.save(img_byte_arr, format=save_format,
                                subsampling=0, quality=90)
                        out_zip.writestr(im_name,
                                         img_byte_arr.getvalue())
                    else:
                        im.save(os.path.join(out_name, im_name),
                                format=save_format, subsampling=0, quality=90)
                    page_num += 1
            if self.mode == Mode.zip:
                m_zip.close()
                out_zip.close()

    def __get_mangas(self, path):
        for f in os.scandir(path):
            if (f.name.endswith('zip') if self.mode == Mode.zip else f.is_dir()):
                yield f.path

    def __get_pages(self, path: str, m_zip: zipfile.ZipFile):
        return m_zip.namelist() if m_zip else sorted([f for f in os.listdir(path) if f.endswith(ImageExt)])

    def __split_page(self, file):
        im = Image.open(file)
        (w, h) = im.size
        if w > h:
            l = im.crop((0, 0, w // 2, h))
            r = im.crop((w // 2, 0, w, h))
            return [l, r] if self.page_mode == PageMode.L2R else [r, l]
        else:
            return [im]


if __name__ == "__main__":
    parser = argparse.ArgumentParser("MangaSplitter")
    parser.add_argument("path", help="path to your manga", type=str)
    parser.add_argument("-dir", action="store_const", const=Mode.dir, default=Mode.zip, dest="mode",
                        help="if manga episode is in directory (default: zip)")
    parser.add_argument("-l2r", action="store_const", const=PageMode.L2R, default=PageMode.R2L, dest="orientation",
                        help="if each page is from left to right (default r2l)")
    parser.add_argument("-single", action="store_false", default=True, dest="multiple",
                        help="if the path is an episode rather than a dir w/ multiple episodes")

    args = parser.parse_args()
    s = MangaSplitter()
    s.split(args.path, multiple=args.multiple,
            mode=args.mode, page_mode=args.orientation)
