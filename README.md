# mortgage_vs_renting

A Python model that compares the long run cost of renting versus owning.

This model takes a number of high level parameters associated with owning a
home and generalises comparable costs when renting. It can be used as a tool
to compare the total cost of ownership against rent over a person's lifetime.

## Getting Started

The repository includes a small Python script `mortgage_vs_renting.py` that
performs a basic comparison between renting and buying. You can run it
directly:

```bash
python mortgage_vs_renting.py
```

The script accepts command-line arguments so you can easily experiment with
different scenarios. Run it with `--help` to see all available options, such as
`--purchase-price`, `--monthly-rent`, and `--years`.

## Running Tests

Automated unit tests are provided in the `tests/` directory. They verify key
calculations such as monthly mortgage payments and rental simulations. Run the
suite with `pytest`:

```bash
pytest -q
```

The tests import the main module from its file path so they work even if the
package isn’t installed. They also demonstrate example usage of the comparison
functions.
