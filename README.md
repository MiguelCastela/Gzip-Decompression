# GZIP Decompressor

A GZIP decompressor written in Python from scratch. It reads a `.gz` file and
reconstructs the original file by implementing the DEFLATE algorithm, without
relying on Python's built-in compression libraries.

This project was developed for the Information Theory course (Teoria da
Informacao) of the Informatics Engineering degree at the University of Coimbra.

## What it does

The tool decompresses files that were compressed with GZIP using DEFLATE with
dynamic Huffman coding (BTYPE 2). The decompression is implemented step by step:

1. Read and validate the GZIP header.
2. Read the dynamic block header (HLIT, HDIST, HCLEN).
3. Build the Huffman tree for the code length alphabet.
4. Rebuild the literal/length and distance code length tables.
5. Build the literal/length and distance Huffman trees.
6. Decode the data stream using LZ77 back references.
7. Write the reconstructed bytes to the output file.

## Project structure

```
.
├── src/
│   ├── gzip_decompressor.py   Main decompressor (GZIP header + DEFLATE decoding)
│   ├── huffman_tree.py        Huffman tree data structure
│   └── test_huffman_tree.py   Small manual test for the Huffman tree
├── examples/
│   ├── FAQ.txt.gz             Sample compressed files
│   ├── sample_audio.mp3.gz
│   ├── sample_image.jpeg.gz
│   ├── sample_large_text.txt.gz
│   └── decompressed/          Expected decompressed outputs for reference
└── docs/
    ├── assignment.pdf         Original assignment statement
    └── report.pdf             Project report
```

## Requirements

Python 3. No external dependencies.

## Usage

Run the decompressor on a compressed file:

```
python src/gzip_decompressor.py path/to/file.gz
```

If no file is given, it falls back to the bundled `examples/FAQ.txt.gz`:

```
python src/gzip_decompressor.py
```

The decompressed file is written to the current directory, using the original
file name stored in the GZIP header. The program also prints the intermediate
results of each decoding step, which is useful for following how DEFLATE works.

## Tests

To exercise the Huffman tree in isolation:

```
python src/test_huffman_tree.py
```
