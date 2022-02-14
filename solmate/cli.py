import argparse
import os

from solmate.anchor import codegen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--idl-dir', type=str, required=False)
    parser.add_argument('--out-dir', type=str, required=False)
    args = parser.parse_args()

    if args.out_dir is None:
        args.out_dir = os.getcwd()
    if args.idl_dir is None:
        args.idl_dir = os.getcwd()

    codegen.cli(args.idl_dir, args.out_dir)


if __name__ == '__main__':
    main()
