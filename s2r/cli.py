"""Command-line interface for s2r."""

import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from typing import Optional, Tuple

from s2r.converter import convert_slurm_to_runai, ConversionError
from s2r.env import load_env_file, write_env_file, ENV_FILE
from s2r.runai_api import (
    RunaiAPIError,
    create_s3_datasource,
    effective_aws_profile,
    get_aws_credentials,
    get_aws_region,
    list_aws_profiles,
    s3_endpoint_url,
)

VERBOSE = os.environ.get("S2R_VERBOSE", "").lower() in ("1", "true", "yes")


def _warn(msg: str) -> None:
    if VERBOSE:
        print(f"  [warn] {msg}", file=sys.stderr)


def parse_response(response: str) -> Tuple[Optional[str], Optional[str]]:
    """Parse AI response into YAML config and CLI command sections.

    The AI returns markdown with code blocks: a ```yaml block and a ```bash/```shell block.

    Returns:
        Tuple of (yaml_content, cli_command), either may be None if not found.
    """
    yaml_content = None
    cli_command = None

    # Match ```yaml ... ``` blocks (handle CRLF too)
    yaml_match = re.search(r"```ya?ml[ \t]*\r?\n(.*?)```", response, re.DOTALL)
    if yaml_match:
        yaml_content = yaml_match.group(1).strip()

    # Match ```bash, ```shell, ```sh blocks
    cli_match = re.search(r"```(?:bash|shell|sh)[ \t]*\r?\n(.*?)```", response, re.DOTALL)
    if cli_match:
        cli_command = cli_match.group(1).strip()

    # If no code blocks found, return the whole response as-is (fallback)
    if yaml_content is None and cli_command is None:
        return response.strip(), None

    return yaml_content, cli_command


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

    def stop(self) -> None:
        """Stop the spinner and clear the line."""
        self.spinning = False
        if self.thread:
            self.thread.join(timeout=0.5)
        sys.stderr.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stderr.flush()


def _runai_json(args: list) -> Optional[object]:
    """Run a runai CLI command with --json and return parsed JSON, or None on failure."""
    try:
        out = subprocess.check_output(
            ["runai"] + args + ["--json"],
            stderr=subprocess.PIPE, text=True, timeout=15,
        )
    except FileNotFoundError:
        _warn("runai CLI not found in PATH")
        return None
    except subprocess.TimeoutExpired:
        _warn(f"runai {' '.join(args)} timed out")
        return None
    except subprocess.CalledProcessError as e:
        _warn(f"runai {' '.join(args)} exited {e.returncode}: {e.stderr.strip()}")
        return None
    try:
        return json.loads(out)
    except ValueError as e:
        _warn(f"runai {' '.join(args)} returned non-JSON output: {e}")
        return None


def _runai_detect(project: str = "") -> dict:
    """Read project, cluster, and datasources from the runai CLI (JSON output).

    Returns a dict with keys 'project', 'cluster', 'datasources' (list of (name, type) tuples).
    Missing keys mean detection failed for that field; the wizard treats them as optional.
    """
    detected: dict = {}

    def _unwrap(obj: object, key: str) -> list:
        """Return obj[key] if dict-wrapped, or obj if it's already a list."""
        if isinstance(obj, dict):
            return obj.get(key, []) or []
        if isinstance(obj, list):
            return obj
        return []

    clusters = _unwrap(_runai_json(["cluster", "list"]), "clusters")
    if clusters and isinstance(clusters[0], dict) and clusters[0].get("name"):
        detected["cluster"] = clusters[0]["name"]

    projects = _unwrap(_runai_json(["project", "list"]), "projects")
    if projects and isinstance(projects[0], dict) and projects[0].get("name"):
        detected["project"] = projects[0]["name"]

    proj = project or detected.get("project", "")
    if proj:
        ds = _unwrap(_runai_json(["datasource", "list", "-p", proj]), "datasources")
        datasources = [
            (e["name"], e.get("type", ""))
            for e in ds
            if isinstance(e, dict) and e.get("name")
        ]
        if datasources:
            detected["datasources"] = datasources

    return detected


def _prompt(question: str, default: str = "") -> str:
    """Ask a question and return the answer; return default on empty input.

    Raises KeyboardInterrupt on EOF/Ctrl-C — caller decides how to handle.
    """
    hint = f" [{default}]" if default else ""
    answer = input(f"{question}{hint}: ").strip()
    return answer if answer else default


def _yn(question: str) -> bool:
    """Ask a yes/no question, defaulting to yes. Raises KeyboardInterrupt on EOF/Ctrl-C."""
    answer = input(f"{question} [Y/n]: ").strip().lower()
    return answer in ("y", "yes", "")


def _pick_aws_profile(default: str = "") -> str:
    """Show available AWS profiles and let the user pick one. Empty string skips."""
    profiles = list_aws_profiles()
    if not profiles:
        print("  No AWS profiles found in ~/.aws/credentials or ~/.aws/config.", file=sys.stderr)
        return ""
    print("  Available AWS profiles:", file=sys.stderr)
    for i, name in enumerate(profiles, 1):
        marker = "  *" if name == default else "   "
        print(f"  {marker}{i}. {name}", file=sys.stderr)
    answer = _prompt(
        "  Pick a profile by number or name (blank to skip)",
        default=default,
    )
    if not answer:
        return ""
    if answer.isdigit():
        idx = int(answer) - 1
        if 0 <= idx < len(profiles):
            return profiles[idx]
        print(f"  Invalid index {answer}; skipping.", file=sys.stderr)
        return ""
    if answer in profiles:
        return answer
    print(f"  Profile '{answer}' not found; skipping.", file=sys.stderr)
    return ""


def _interactive_setup() -> None:
    """Setup wizard: offer to configure env vars and save to ~/.runai/runai.env."""
    try:
        _interactive_setup_inner()
    except (EOFError, KeyboardInterrupt):
        print("", file=sys.stderr)
        print("Cancelled.", file=sys.stderr)
        sys.exit(130)


def _interactive_setup_inner() -> None:
    print("s2r — SLURM to Run:ai converter", file=sys.stderr)
    print("", file=sys.stderr)

    # Show what's already saved in the env file
    saved = load_env_file()
    s2r_keys = ("RUNAI_PROJECT", "RUNAI_BUCKET", "RUNAI_CACHE", "RUNAI_AWS_PROFILE", "RUNAI_MODEL")
    saved_s2r = {k: saved[k] for k in s2r_keys if k in saved}
    if saved_s2r:
        print(f"Saved in {ENV_FILE}:", file=sys.stderr)
        for k, v in saved_s2r.items():
            print(f"  {k}={v}", file=sys.stderr)
        print("", file=sys.stderr)

    already = {k: os.environ.get(k, "") for k in s2r_keys}

    # Offer to auto-detect from runai CLI if present
    detected: dict = {}
    if shutil.which("runai"):
        print("runai CLI detected in PATH.", file=sys.stderr)
        if _yn("Auto-detect project, cluster, and datasources from 'runai' CLI?"):
            detected = _runai_detect(already.get("RUNAI_PROJECT", ""))
            if detected:
                print("", file=sys.stderr)
                print("Detected:", file=sys.stderr)
                for k, v in detected.items():
                    if k == "datasources":
                        print("  datasources:", file=sys.stderr)
                        for name, dtype in v:
                            print(f"    {name}  ({dtype})", file=sys.stderr)
                    else:
                        print(f"  {k} = {v}", file=sys.stderr)
            else:
                print("Nothing detected (not logged in or no data).", file=sys.stderr)
        print("", file=sys.stderr)

    if not _yn("Configure environment variables now?"):
        print("", file=sys.stderr)
        print_help()
        sys.exit(0)

    print("", file=sys.stderr)
    datasources = detected.get("datasources", [])
    s3s       = [name for name, dtype in datasources if "s3" in dtype.lower()]
    hostpaths = [name for name, dtype in datasources if "hostpath" in dtype.lower()]

    project = _prompt("RUNAI_PROJECT", detected.get("project") or already.get("RUNAI_PROJECT", ""))

    cache_default = already.get("RUNAI_CACHE", "") or (hostpaths[0] if hostpaths else "cache")
    cache = _prompt("RUNAI_CACHE  (datasource name for cache)", cache_default)

    bucket = _prompt("RUNAI_BUCKET  (optional, S3 datasource name or s3://uri)",
                     already.get("RUNAI_BUCKET", "") or (s3s[0] if s3s else ""))

    # Offer to create the S3 datasource if it doesn't exist yet
    if bucket and project and bucket not in s3s:
        print("", file=sys.stderr)
        print(f"  '{bucket}' is not yet registered as a Run:ai datasource.", file=sys.stderr)
        aws_profile_for_create = effective_aws_profile()
        try:
            ak, _ = get_aws_credentials(aws_profile_for_create)
            cred_hint = (
                f"AWS profile '{aws_profile_for_create}'" if aws_profile_for_create
                else f"AWS default profile (key: {ak[:8]}...)"
            )
        except RunaiAPIError as e:
            cred_hint = f"no AWS credentials found ({e})"
        print(f"  Using {cred_hint}", file=sys.stderr)
        if _yn(f"  Create S3 datasource '{bucket}' in Run:ai now?"):
            region = get_aws_region(aws_profile_for_create)
            default_url = s3_endpoint_url(aws_profile_for_create)
            if region:
                print(f"  Detected AWS region: {region}", file=sys.stderr)
            else:
                print("  No AWS region configured — bucket may be in a different region than the endpoint.",
                      file=sys.stderr)
            s3_url = _prompt("  S3 endpoint URL", default_url)
            try:
                create_s3_datasource(
                    bucket_name=bucket,
                    project_name=project,
                    s3_url=s3_url,
                    aws_profile=aws_profile_for_create,
                )
                print(f"  Datasource '{bucket}' created successfully.", file=sys.stderr)
                # Refresh local view so subsequent logic knows it now exists
                s3s.append(bucket)
            except RunaiAPIError as e:
                print(f"  Failed to create datasource: {e}", file=sys.stderr)
                print("  You can create it manually in the Run:ai UI.", file=sys.stderr)
        print("", file=sys.stderr)

    # AWS profile — used as a fallback when shell AWS_PROFILE is empty or 'default'.
    # Drives both: (a) which credentials s2r uses to create the S3 datasource,
    # (b) which --profile flag the generated 'aws s3 sync' upload comment uses.
    print("", file=sys.stderr)
    print("RUNAI_AWS_PROFILE: AWS profile for s2r operations (S3 datasource + upload hints).", file=sys.stderr)
    print("  Used when AWS_PROFILE is empty or 'default'; explicit AWS_PROFILE wins.", file=sys.stderr)
    aws_profile = _pick_aws_profile(default=already.get("RUNAI_AWS_PROFILE", ""))

    # Model picker
    print("", file=sys.stderr)
    print("RUNAI_MODEL: which Claude model to use for conversion.", file=sys.stderr)
    print("  sonnet (default) — Claude Sonnet 4.6, fast, fits within the API Gateway 30s timeout.", file=sys.stderr)
    print("  opus            — Claude Opus 4.7, higher quality but may time out (503) on the", file=sys.stderr)
    print("                    public endpoint due to API Gateway's 30s integration cap.", file=sys.stderr)
    model_default = already.get("RUNAI_MODEL", "") or "sonnet"
    model = _prompt("RUNAI_MODEL  (sonnet|opus)", model_default).strip().lower()
    if model not in ("sonnet", "opus"):
        print(f"  Invalid model '{model}', defaulting to sonnet.", file=sys.stderr)
        model = "sonnet"

    values = {}
    if project:
        values["RUNAI_PROJECT"] = project
    if bucket:
        values["RUNAI_BUCKET"] = bucket
    if cache:
        values["RUNAI_CACHE"] = cache
    if aws_profile:
        values["RUNAI_AWS_PROFILE"] = aws_profile
    if model:
        values["RUNAI_MODEL"] = model

    print("", file=sys.stderr)
    if not values:
        print("Nothing to save.", file=sys.stderr)
        sys.exit(0)

    write_env_file(values)
    print(f"Saved to {ENV_FILE}:", file=sys.stderr)
    for k, v in values.items():
        print(f"  {k}={v}", file=sys.stderr)
    print("", file=sys.stderr)
    print("These will be loaded automatically next time you run s2r.", file=sys.stderr)
    sys.exit(0)


def print_help() -> None:
    """Print help message."""
    print("s2r - Convert SLURM scripts to Run.ai configurations using AI", file=sys.stderr)
    print("", file=sys.stderr)
    print("Usage:", file=sys.stderr)
    print("  s2r <input_file>                  Convert SLURM script, print runai command to stdout", file=sys.stderr)
    print("  s2r < script.sh                   Read from stdin, print runai command to stdout", file=sys.stderr)
    print("  cat script.sh | s2r               Read from stdin, print runai command to stdout", file=sys.stderr)
    print("  s2r job.slurm | bash              Convert and submit to Run:ai in one step", file=sys.stderr)
    print("  s2r --config                      Setup wizard: detect and save env to ~/.runai/runai.env", file=sys.stderr)
    print("  s2r --prompt <input_file>         Print the assembled prompt that would be sent to the LLM (no LLM call)", file=sys.stderr)
    print("", file=sys.stderr)
    print("Note: YAML manifest output ('runai workload submit --file') is not yet implemented.", file=sys.stderr)
    print("      Run:ai 2.25 only accepts standard K8s/Kubeflow kinds (Job, PyTorchJob, etc.)", file=sys.stderr)
    print("      via that path; the imperative 'runai training standard submit' CLI is used instead.", file=sys.stderr)
    print("", file=sys.stderr)
    print("Configuration:", file=sys.stderr)
    print("  ~/.runai/runai.env                Persistent config file (auto-loaded on every run)", file=sys.stderr)
    print("  Run 's2r --config' to create or update it.", file=sys.stderr)
    print("  On first run with no arguments, the setup wizard starts automatically.", file=sys.stderr)
    print("", file=sys.stderr)
    print("Environment variables (override runai.env):", file=sys.stderr)
    print("  RUNAI_PROJECT                     Run:ai project (fills --project in output)", file=sys.stderr)
    print("  RUNAI_BUCKET                      S3 bucket or s3://uri — mounted at /mnt/<name>", file=sys.stderr)
    print("  RUNAI_CACHE                       Datasource name for cache (default: cache)", file=sys.stderr)
    print("  RUNAI_AWS_PROFILE                 AWS profile for s2r (fallback if AWS_PROFILE is unset/default)", file=sys.stderr)
    print("  RUNAI_MODEL                       Claude model: sonnet (default) or opus", file=sys.stderr)
    print("  AWS_PROFILE                       AWS profile for authentication", file=sys.stderr)
    print("  S2R_API_ENDPOINT                  Custom API endpoint URL", file=sys.stderr)
    print("  S2R_AWS_REGION                    AWS region (default: us-west-2)", file=sys.stderr)
    print("  S2R_USE_IAM_AUTH                  Use IAM auth (default: false)", file=sys.stderr)


def main() -> None:
    """Main CLI entry point. Wraps the implementation to catch Ctrl-C cleanly."""
    try:
        _main_impl()
    except KeyboardInterrupt:
        # Stop the spinner if it's still running, then exit silently
        sys.stderr.write("\r" + " " * 60 + "\r")
        sys.stderr.write("Interrupted.\n")
        sys.exit(130)


def _main_impl() -> None:
    args = sys.argv[1:]

    # Check for help flag
    if args and args[0] in ("-h", "--help", "help"):
        print_help()
        sys.exit(0)

    # --configure / --config: run the interactive setup wizard
    if args and args[0] in ("--configure", "--config"):
        _interactive_setup()
        sys.exit(0)

    # --prompt: print the assembled Bedrock prompt (no LLM call, no rate-limit charge)
    dry_run = False
    if args and args[0] == "--prompt":
        dry_run = True
        args = args[1:]

    # Determine input source
    input_file: Optional[str] = None

    if len(args) == 0:
        # Check if stdin is a TTY (interactive terminal)
        if os.isatty(sys.stdin.fileno()):
            if not ENV_FILE.exists():
                # First run — no config yet, offer setup wizard
                _interactive_setup()
            else:
                print_help()
            sys.exit(0)
        # Read from stdin (piped input)
        input_source = "stdin"
    elif len(args) == 1:
        # Read from file, print runai CLI command to stdout (pipe-safe to bash)
        input_file = args[0]
        input_source = "file"
    else:
        print("Usage: s2r [input_file]", file=sys.stderr)
        print("  No args: read from stdin, print runai command to stdout", file=sys.stderr)
        print("  One arg: read file, print runai command to stdout", file=sys.stderr)
        print("  Pipe to bash to execute: s2r job.slurm | bash", file=sys.stderr)
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
        if show_spinner and not dry_run:
            spinner = Spinner("Sending to AI for conversion")
            spinner.start()

        result = convert_slurm_to_runai(slurm_script, dry_run=dry_run)

        if spinner:
            spinner.stop()
    except ConversionError as e:
        if spinner:
            spinner.stop()
        print(f"Conversion error: {e}", file=sys.stderr)
        sys.exit(1)

    # --prompt: dump the assembled Bedrock prompt and exit
    if dry_run:
        print(result)
        sys.exit(0)

    # Parse response into YAML and CLI sections
    yaml_content, cli_command = parse_response(result)

    # Print the runai CLI shell script to stdout — pipe-safe to bash.
    # Note: YAML manifest output via 'runai workload submit --file' is not yet
    # implemented (the TrainingWorkload v2alpha1 CRD is not accepted via that path
    # on Run:ai 2.25; it requires standard K8s/Kubeflow kinds like Job, PyTorchJob, etc.).
    try:
        if cli_command:
            print(cli_command)
        else:
            # Fallback: model returned no fenced bash block — print whatever we got
            print(result)
    except Exception as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
