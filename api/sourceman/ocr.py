import subprocess
from pathlib import Path

print("hello ocr.py")

# class NougatExtractor:
#     def __init__(self, batch_size: int = 4, min_words: int = 25):
#         """
#         Extract text from a pdf file using nougat-ocr.

#         Args:
#             batch_size (int, optional): batch size for nougat-ocr. Defaults to 4.
#             min_words (int, optional): minimum number of words for a paragraph to be included in the output. Defaults to 25.
#         """
#         self.batch_size = batch_size
#         self.min_words = min_words

#     def extract_pdf_text(self, path: Path, log=None) -> str:
#         """
#         extract text from a pdf file using nougat-ocr

#         Args:
#             path (Path): path to the pdf file
#             log (_FILE, optional): file object to write stdout and stderr to. Defaults to None (i.e. output to stdout/stderr).
#         """
#         assert path.exists(), f"file {path} does not exist"
#         assert path.suffix == ".pdf", f"file {path} is not a pdf"
#         result = subprocess.run(
#             ["nougat", str(path), "-o", str(path.parent), "-b", str(self.batch_size)],
#             stdout=log,
#             stderr=log,
#         )
#         assert result.returncode == 0, f"error extracting text from {path}"
#         text = path.with_suffix(".mmd").read_text()
#         path.with_suffix(".mmd").unlink()
#         return text
