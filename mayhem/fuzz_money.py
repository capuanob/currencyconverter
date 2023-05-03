#!/usr/bin/env python3
import atheris
import sys

import fuzz_helpers

with atheris.instrument_imports(include=['currency_converter']):
    from currency_converter import CurrencyConverter, RateNotFoundError

ctr = 0


def TestOneInput(data):
    global ctr

    ctr += 1
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    f: str
    with fdp.ConsumeTemporaryFile(suffix='.csv', as_bytes=False) as f:
        try:
            c = CurrencyConverter(f)
            currency = fdp.PickValueInList(c.currencies)
            new_currency = fdp.PickValueInList(c.currencies)
            c.convert(fdp.ConsumeFloat(), currency, new_currency)
        except (RateNotFoundError, StopIteration):
            return -1
        except Exception as e:
            if isinstance(e, ValueError) and 'time data' in str(e):
                return -1
            if ctr >= 50_000:
                # We have iterated long enough for Mayhem to start up
                raise e


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
