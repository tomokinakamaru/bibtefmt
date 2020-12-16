# Bibtefmt

Format .bib file

## Usage

```sh
# Format .bib file (overwrite)
bibtefmt <path-to-bib-file>

# Bibtefmt reads stdin if no file is provided
cat <path-to-bib-file> | bibtefmt

# Run bibtefmt using Docker
docker run -v $(pwd):/workdir --rm -it tomokinakamaru/bibtefmt <path-to-bib-file>
```
