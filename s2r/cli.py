"""Command-line interface for s2r."""

import os
import sys
import threading
import time
from typing import Optional

from s2r.converter import convert_slurm_to_runai, ConversionError


class Spinner:
    """A simple spinner for showing progress in the terminal."""

    def __init__(self, message: str = "Processing"):
        self.message = message
        self.spinning = False
        self.thread: Optional[threading.Thread] = None
        self.spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

    def start(self) -> None:
        """Start the spinner."""
        self.spinning = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def _spin(self) -> None:
        """Spin animation loop."""
        idx = 0
        while self.spinning:
            char = self.spinner_chars[idx % len(self.spinner_chars)]
            sys.stderr.write(f"\r{char} {self.message}...")
            sys.stderr.flush()
            idx += 1
            time.sleep(0.1)

    def stop(self, success: bool = True) -> None:
        """Stop the spinner and clear the line."""
        self.spinning = False
        if self.thread:
            self.thread.join(timeout=0.5)
        # Clear the spinner line
        sys.stderr.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stderr.flush()


def print_help() -> None:
    """Print help message."""
    print("s2r - Convert SLURM scripts to Run.ai configurations using AI", file=sys.stderr)
    print("", file=sys.stderr)
    print("Usage:", file=sys.stderr)
    print("  s2r <input_file> [output_file]    Convert SLURM script file", file=sys.stderr)
    print("  s2r < script.sh                   Read from stdin (piped input)", file=sys.stderr)
    print("  cat script.sh | s2r               Read from stdin (piped input)", file=sys.stderr)
    print("", file=sys.stderr)
    print("Examples:", file=sys.stderr)
    print("  s2r job.slurm                     Convert and print to stdout", file=sys.stderr)
    print("  s2r job.slurm output.yaml         Convert and save to file", file=sys.stderr)
    print("  s2r < job.slurm > output.yaml     Using shell redirection", file=sys.stderr)
    print("", file=sys.stderr)
    print("Environment variables:", file=sys.stderr)
    print("  AWS_PROFILE                       AWS profile for authentication", file=sys.stderr)
    print("  S2R_API_ENDPOINT                  Custom Lambda Function URL", file=sys.stderr)
    print("  S2R_AWS_REGION                    AWS region (default: us-west-2)", file=sys.stderr)
    print("  S2R_USE_IAM_AUTH                  Use IAM auth (default: true)", file=sys.stderr)


def main() -> None:
    """Main CLI entry point."""
    args = sys.argv[1:]

    # Check for help flag
    if args and args[0] in ("-h", "--help", "help"):
        print_help()
        sys.exit(0)

    # Determine input source
    input_file: Optional[str] = None
    output_file: Optional[str] = None

    if len(args) == 0:
        # Check if stdin is a TTY (interactive terminal)
        if os.isatty(sys.stdin.fileno()):
            # Interactive terminal - show help
            print_help()
            sys.exit(1)
        # Read from stdin (piped input)
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

    # Check if we got any input
    if not slurm_script.strip():
        print_help()
        sys.exit(1)

    # Show spinner if stderr is a terminal (not redirected)
    show_spinner = os.isatty(sys.stderr.fileno())
    spinner = None

    # Convert
    try:
        if show_spinner:
            spinner = Spinner("Sending to AI for conversion")
            spinner.start()

        runai_config = convert_slurm_to_runai(slurm_script)

        if spinner:
            spinner.stop()
    except ConversionError as e:
        if spinner:
            spinner.stop(success=False)
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
