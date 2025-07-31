# wheel-matrix

`wheel-matrix` is a Python tool that simplifies the complexity of managing Python package distributions by generating a comprehensive Markdown matrix of available wheel files for different Python versions and platforms. This tool aids in the visualization of compatibility and availability of wheel files for Python packages across various operating systems (Linux, Windows, macOS) and architectures (x86_64, i686, arm64, etc.), streamlining the process of identifying the necessary distributions for package users and maintainers.

## Features

- Generates a Markdown formatted matrix of available wheel distributions.
- Supports multiple platforms including Linux, Windows, and macOS.
- Identifies distributions for a range of Python versions, considering only versions newer than Python 3.7.
- Easy to integrate into documentation or CI/CD pipelines for automated updates.


## Example

This table was produced by `wheel-matrix pyfxr`:

| Python | linux x86_64 | linux i686 | linux aarch64 | windows win32 | windows amd64 | mac x86_64 | mac arm64 | musllinux aarch64 | musllinux i686 | musllinux x86_64 |
| ------ | ------------ | ---------- | ------------- | ------------- | ------------- | ---------- | --------- | ----------------- | -------------- | ---------------- |
| cp313  | ❌           | ❌         | ❌            | ❌            | ❌            | ❌         | ❌        | ❌                | ❌             | ❌               |
| cp312  | ✅           | ✅         | ✅            | ✅            | ✅            | ✅         | ✅        | ✅                | ✅             | ✅               |
| cp311  | ✅           | ✅         | ✅            | ✅            | ✅            | ✅         | ✅        | ✅                | ✅             | ✅               |
| cp310  | ✅           | ✅         | ✅            | ✅            | ✅            | ✅         | ✅        | ✅                | ✅             | ✅               |
| cp39   | ✅           | ✅         | ✅            | ✅            | ✅            | ✅         | ✅        | ✅                | ✅             | ✅               |
| cp38   | ✅           | ✅         | ✅            | ✅            | ✅            | ✅         | ✅        | ✅                | ✅             | ✅               |
| cp36   | ✅           | ✅         | ✅            | ✅            | ✅            | ✅         | ❌        | ✅                | ✅             | ✅               |
| cp37   | ✅           | ✅         | ✅            | ✅            | ✅            | ✅         | ❌        | ✅                | ✅             | ✅               |
| pp310  | ✅           | ✅         | ✅            | ❌            | ✅            | ✅         | ✅        | ❌                | ❌             | ❌               |
| pp36   | ✅           | ❌         | ❌            | ✅            | ❌            | ✅         | ❌        | ❌                | ❌             | ❌               |
| pp37   | ✅           | ✅         | ✅            | ✅            | ✅            | ✅         | ❌        | ❌                | ❌             | ❌               |
| pp38   | ✅           | ✅         | ✅            | ❌            | ✅            | ✅         | ✅        | ❌                | ❌             | ❌               |
| pp39   | ✅           | ✅         | ✅            | ❌            | ✅            | ✅         | ✅        | ❌                | ❌             | ❌               |
In this table:
- ✅ indicates a wheel exists for that Python/version and platform.
- ❌ means no wheel is available.
- 🐌 shows that a universal wheel (`py3-none-any`) is available.

## Installation

`wheel-matrix` can be installed from PyPI with pip:

```bash
pip install wheel-matrix
```

Ensure you have Python 3.10 or newer to run `wheel-matrix`.

## Usage

To use `wheel-matrix`, run the following command in your terminal:

```bash
wheel-matrix <package-name> [<version>] [--platforms=all] [--output=md|json|gha-matrix]
```

- `<package-name>`: Name of the Python package for which to generate the wheel matrix.
- `<version>`: (Optional) Specific version of the package. If not provided, the latest version will be used.
- `--platforms=all`: Include every architecture known to the tool, instead of the recommended subset.
- `--output=`: Select the output format. ``md`` (default) prints a Markdown table,
  ``json`` prints the raw data and ``gha-matrix`` prints a GitHub Actions matrix
  describing the missing wheels.

Example:

```bash
wheel-matrix pandas
```

This will print a Markdown formatted matrix to the console, showing the availability of wheel files for different combinations of Python versions and operating systems.

## Contributing

Contributions to `wheel-matrix` are welcome!

Please feel free to submit pull requests or create issues on the [GitHub repository](https://github.com/lordmauve/wheel-matrix).


## License

`wheel-matrix` is released under the MIT License. See the LICENSE file in the GitHub repository for more details.
