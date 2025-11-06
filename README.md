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

## GitHub Actions Matrix Output

The `gha-matrix` output format is specifically designed for integration with GitHub Actions workflows. It generates a JSON array describing the missing wheels that need to be built.

### Output Format

When you run `wheel-matrix` with `--output=gha-matrix`, it produces a JSON array where each element represents a missing wheel. Each object contains:

- `os`: The GitHub Actions runner to use (e.g., `ubuntu-latest`, `windows-latest`, `macos-13`, `macos-latest`)
- `python`: The Python version as a string (e.g., `"3.13"`, `"3.12"`, `"3.11"`)

Example output:
```json
[
  {
    "os": "ubuntu-latest",
    "python": "3.13"
  },
  {
    "os": "windows-latest",
    "python": "3.13"
  },
  {
    "os": "macos-latest",
    "python": "3.13"
  }
]
```

### Usage in GitHub Actions

You can use this output to create a dynamic build matrix in GitHub Actions that builds only the missing wheels. Here's a complete example workflow:

```yaml
name: Build Missing Wheels

on:
  workflow_dispatch:
    inputs:
      package:
        description: 'Package name'
        required: true
      version:
        description: 'Package version (optional)'
        required: false

jobs:
  generate-matrix:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - name: Install wheel-matrix
        run: pip install wheel-matrix

      - name: Generate matrix
        id: set-matrix
        run: |
          if [ -n "${{ github.event.inputs.version }}" ]; then
            MATRIX=$(wheel-matrix ${{ github.event.inputs.package }} ${{ github.event.inputs.version }} --output=gha-matrix)
          else
            MATRIX=$(wheel-matrix ${{ github.event.inputs.package }} --output=gha-matrix)
          fi
          echo "matrix=$MATRIX" >> $GITHUB_OUTPUT

  build-wheels:
    needs: generate-matrix
    if: needs.generate-matrix.outputs.matrix != '[]'
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        include: ${{ fromJson(needs.generate-matrix.outputs.matrix) }}
    steps:
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}

      - name: Build wheel
        run: |
          # Your wheel building steps here
          # For example, using cibuildwheel or build
          pip install build
          # ... additional build commands
```

This approach ensures that you only run build jobs for the platform and Python version combinations where wheels are actually missing, saving CI/CD resources and time.

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
