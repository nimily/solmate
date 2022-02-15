import argparse
import os

from solmate.anchor import codegen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--idl-dir", type=str, required=False)
    parser.add_argument("--out-dir", type=str, required=False)
    parser.add_argument("--parent-module", type=str, required=False)
    parser.add_argument("--skip", nargs='+', required=False)
    args = parser.parse_args()



    if args.idl_dir is None:
        args.idl_dir = os.getcwd()
    if args.out_dir is None:
        args.out_dir = os.getcwd()
    if args.parent_module is None:
        args.parent_module = "codegen"
    if args.skip is None:
        args.skip = ["TwoIterators"]

    skip_types = set(args.skip)

    codegen.cli(args.idl_dir, args.out_dir, args.parent_module, skip_types)


if __name__ == "__main__":
    main()
