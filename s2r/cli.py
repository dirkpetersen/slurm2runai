"""Command-line interface for s2r."""

import sys
from typing import Optional

from s2r.converter import convert_slurm_to_runai, ConversionError


def main() -> None:
    """Main CLI entry point.

    Usage:
        s2r < slurm_script.sh                    # Read from stdin, write to stdout
        s2r slurm_script.sh                      # Read from file, write to stdout
        s2r slurm_script.sh output.yaml          # Read from file, write to file
        echo "..." | s2r                         # Pipe from stdin
    """
    args = sys.argv[1:]

    # Determine input source
    input_file: Optional[str] = None
    output_file: Optional[str] = None

    if len(args) == 0:
        # Read from stdin
        input_source = "stdin"
    elif len(args) == 1:
        # Read from file, write to stdout
        input_file = args[0]
        input_source = "file"
    elif len(args) == 2:
        # Read from file, write to file
        input_file = args[0]
        output_file = args[1]
        input_source = "file"
    else:
        print("Usage: s2r [input_file] [output_file]", file=sys.stderr)
        print("  No args: read from stdin, write to stdout", file=sys.stderr)
        print("  One arg: read from file, write to stdout", file=sys.stderr)
        print("  Two args: read from file, write to file", file=sys.stderr)
        sys.exit(1)

    # Read input
    try:
        if input_source == "stdin":
            slurm_script = sys.stdin.read()
        else:
            with open(input_file, "r", encoding="utf-8") as f:
                slurm_script = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    # Convert
    try:
        runai_config = convert_slurm_to_runai(slurm_script)
    except ConversionError as e:
        print(f"Conversion error: {e}", file=sys.stderr)
        sys.exit(1)

    # Write output
    try:
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(runai_config)
            print(f"Run.ai configuration written to: {output_file}", file=sys.stderr)
        else:
            print(runai_config)
    except Exception as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
