import os
import io
import zipfile
from enum import Enum
from PIL import Image

Mode = Enum('Mode', 'zip dir')
PageMode = Enum('PageMode', 'R2L L2R')
ImageExt = ('jpg', 'png')


def getFileName(page_num, ext):
    return f"{page_num:03}{ext}"


class Splitter():
    def __init__(self) -> None:
        pass

    def split(self, path, multiple=True, mode=Mode.zip, page_mode=PageMode.R2L):
        self.mode = mode
        self.page_mode = page_mode
        page_num = 0
        mangas = self.__get_mangas(path) if multiple else [path]
        save_dir = os.path.join(os.path.dirname(
            path), f"{os.path.basename(path)}_split")
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        for manga in mangas:
            print(f"Processing: {manga}")
            out_name = os.path.join(save_dir, os.path.basename(manga))
            m_zip = zipfile.ZipFile(
                manga) if self.mode == Mode.zip else None
            out_zip = zipfile.ZipFile(
                out_name, 'w') if self.mode == Mode.zip else None
            pages = self.__get_pages(manga, m_zip)
            _, ext = os.path.splitext(pages[0])
            save_format = 'PNG' if ext.endswith('png') else 'jpeg'
            for page in pages:
                splitted_imgs = self.__split_page(m_zip.open(page) if m_zip else page)
                for im in splitted_imgs:
                    img_byte_arr = io.BytesIO()
                    im.save(img_byte_arr, format=save_format)
                    out_zip.writestr(getFileName(page_num, ext),
                                     img_byte_arr.getvalue())
                    page_num += 1
            m_zip.close()
            out_zip.close()

    def __get_mangas(self, path):
        for f in os.scandir(path):
            if (f.name.endswith('zip') if self.mode == Mode.zip else f.is_dir()):
                yield f.path

    def __get_pages(self, path: str, m_zip: zipfile.ZipFile):
        return m_zip.namelist() if m_zip else [f for f in os.listdir(path) if f.endswith(ImageExt)]

    def __split_page(self, file):
        im = Image.open(file)
        (w, h) = im.size
        if w > h:
            l = im.crop((0, 0, w // 2, h))
            r = im.crop((w // 2, 0, w, h))
            return [l, r] if self.page_mode == PageMode.L2R else [r, l]
        else:
            return [im]


s = Splitter()
s.split('../tl')
