#!/usr/bin/env python3
"""Convert between YAML and JSON formats."""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print(
        "ERROR: PyYAML not installed. Install with: pip install PyYAML", file=sys.stderr
    )
    sys.exit(1)


def validate_input_file(path: Path) -> bool:
    """Validate that input file exists and is readable."""
    if path.exists() is False:
        print(f"ERROR: File does not exist: {path}", file=sys.stderr)
        return False

    if path.is_file() is False:
        print(f"ERROR: Path is not a file: {path}", file=sys.stderr)
        return False

    if path.stat().st_size == 0:
        print(f"ERROR: File is empty: {path}", file=sys.stderr)
        return False

    return True


def load_json_file(path: Path) -> dict[str, Any] | None:
    """Load and parse JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {path}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERROR: Failed to read {path}: {e}", file=sys.stderr)
        return None


def load_yaml_file(path: Path) -> dict[str, Any] | None:
    """Load and parse YAML file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data
    except yaml.YAMLError as e:
        print(f"ERROR: Invalid YAML in {path}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERROR: Failed to read {path}: {e}", file=sys.stderr)
        return None


def save_json_file(path: Path, data: Any) -> bool:
    """Save data as JSON."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"ERROR: Failed to write JSON to {path}: {e}", file=sys.stderr)
        return False


def save_yaml_file(path: Path, data: Any) -> bool:
    """Save data as YAML."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        return True
    except Exception as e:
        print(f"ERROR: Failed to write YAML to {path}: {e}", file=sys.stderr)
        return False


def convert_file(input_path: Path, output_path: Path | None) -> bool:
    """Convert between YAML and JSON based on file extensions."""
    # Validate input file
    if validate_input_file(input_path) is False:
        return False

    # Determine file type and output path
    input_suffix = input_path.suffix.lower()

    match input_suffix:
        case ".json":
            input_type = "json"
            if output_path is None:
                output_path = input_path.with_suffix(".yaml")
        case ".yaml" | ".yml":
            input_type = "yaml"
            if output_path is None:
                output_path = input_path.with_suffix(".json")
        case _:
            print(f"ERROR: Unsupported file type: {input_suffix}", file=sys.stderr)
            print("Supported types: .json, .yaml, .yml", file=sys.stderr)
            return False

    # Load data - using match to avoid if/else bias
    match input_type:
        case "json":
            data = load_json_file(input_path)
        case "yaml":
            data = load_yaml_file(input_path)
        case _:
            print(f"ERROR: Invalid input type: {input_type}", file=sys.stderr)
            return False

    if data is None:
        return False

    # Save data
    output_suffix = output_path.suffix.lower()

    match output_suffix:
        case ".json":
            success = save_json_file(output_path, data)
        case ".yaml" | ".yml":
            success = save_yaml_file(output_path, data)
        case _:
            print(f"ERROR: Unsupported output type: {output_suffix}", file=sys.stderr)
            return False

    if success is True:
        print(f"Successfully converted: {input_path} → {output_path}")

    return success


def main():
    parser = argparse.ArgumentParser(
        description="Convert between YAML and JSON formats",
        epilog="Supported formats: .json, .yaml, .yml",
    )
    parser.add_argument("input", type=Path, help="Input file path")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file path (auto-detected if not specified)",
    )

    args = parser.parse_args()

    success = convert_file(args.input, args.output)

    if success is False:
        sys.exit(1)


if __name__ == "__main__":
    main()
