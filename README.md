# GetEveryWebsiteSubPath

A lightweight Python-based web crawler that recursively finds all subpaths (URLs) on a website by parsing `<a href="">` links — without relying on traditional brute-force (fuzzing) methods.

---

## Description

Unlike fuzzers that guess URLs, **GetEveryWebsiteSubPath** analyzes actual link structures on a webpage using HTML parsing and depth-first recursion. It helps identify the reachable subpaths of a site while avoiding unnecessary requests to non-HTML resources like PDFs, images, videos, and binaries.

---

## Features

- Recursive crawling via `<a href="">` attributes
- Skips non-relevant file types (e.g., `.pdf`, `.png`, `.zip`)
- Optional sub-path filtering (stay within base URL)
- Optional recursion depth limit
- Optionally logs found URLs to a `.txt` file
- Colored terminal output with `colorama` for clarity

---

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `colorama`

Install dependencies:

```bash
pip install requests beautifulsoup4 colorama
```

---

## Usage

Run the tool:

```bash
python get_every_website_subpath.py
```

You will be prompted for:

- **URL** - The website to start crawling from (must be a valid URL)
- **Only search sub-paths?** - `0` (no) or `1` (yes). Limits results to the same base path
- **Max Depth** - Optional recursion limit (e.g., 3). Leave blank for unlimited
- **Save to file** - Enter a filename (e.g., `results.txt`) to save found URLs

---

## File Type Filtering

To speed up crawling and avoid irrelevant downloads, the tool skips links ending with these file extensions:

```bash
.pdf, .docx, .xlsx, .jpg, .mp3, .mp4, .zip, .exe, .json, .svg, etc.
```

---

## Output Example

```bash
Processing URL: https://example.com
[NEW URL]: https://example.com/about
[NEW URL]: https://example.com/contact
[NOT SUBPATH]: https://external.com/page
```

---

## How It Works

- Uses `requests` to fetch pages
- Parses HTML with `BeautifulSoup`
- Extracts `<a href="">` values
- Recursively visits and logs new links (with optional depth and domain filtering)

---

## Author

Made by [William Jacobsen](https://github.com/Williamjacobsen) — 2025

---

## License

This project is open source. Use it responsibly and respect target websites' `robots.txt` and terms of service.

![image](https://github.com/user-attachments/assets/70b1f2c8-9b17-4daf-b487-c001864746d3)
![image](https://github.com/user-attachments/assets/1d900f71-aa91-40a8-a729-e8a2f75e431e)
