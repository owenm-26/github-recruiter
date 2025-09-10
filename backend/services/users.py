import base64
import json
import xml.etree.ElementTree as ET
import tomllib  # built-in from Python 3.11+
from typing import Any

def decode_base64_content(encoded_content: str) -> str:
    """Decode base64-encoded file content into a UTF-8 string."""
    return base64.b64decode(encoded_content).decode("utf-8")


def parse_manifest(manifest_file: str, decoded_content: str, dependencies_key: list[str] | None):
    """
    Parse a manifest file and return dependency names.
    Supports JSON, line-based text, XML, and TOML.
    """
    deps = set()

    # JSON (e.g., package.json, composer.json)
    if manifest_file.endswith(".json"):
        try:
            manifest_data = json.loads(decoded_content)
        except json.JSONDecodeError:
            return deps
        for dep_key in dependencies_key or []:
            if dep_key in manifest_data:
                deps.update(manifest_data[dep_key].keys())

    # Plain text (e.g., requirements.txt, Gemfile, go.mod, DESCRIPTION)
    elif manifest_file.endswith(".txt") or manifest_file in ["Gemfile", "go.mod", "DESCRIPTION"]:
        for line in decoded_content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if manifest_file == "Gemfile" and line.startswith("gem "):
                # e.g., gem "rails", "~> 6.1"
                parts = line.split()
                if len(parts) >= 2:
                    pkg = parts[1].strip("'\"")
                    deps.add(pkg)
            elif manifest_file == "go.mod":
                if line.startswith("require"):
                    # e.g., require github.com/gin-gonic/gin v1.6.3
                    parts = line.split()
                    if len(parts) >= 2:
                        deps.add(parts[1])
            elif manifest_file == "DESCRIPTION":
                if line.startswith(("Depends:", "Imports:")):
                    # e.g., Imports: dplyr, ggplot2
                    pkgs = [p.strip() for p in line.split(":", 1)[1].split(",")]
                    deps.update(pkgs)
            else:  # requirements.txt or fallback
                pkg = line.split("==")[0]
                deps.add(pkg)

    # XML (e.g., pom.xml, packages.config)
    elif manifest_file.endswith(".xml"):
        try:
            root = ET.fromstring(decoded_content)
        except ET.ParseError:
            return deps

        if manifest_file == "pom.xml":
            for dep in root.findall(".//dependency"):
                group_id = dep.findtext("groupId")
                artifact_id = dep.findtext("artifactId")
                if group_id and artifact_id:
                    deps.add(f"{group_id}:{artifact_id}")
        elif manifest_file == "packages.config":
            for pkg in root.findall(".//package"):
                pkg_id = pkg.get("id")
                if pkg_id:
                    deps.add(pkg_id)

    # TOML (e.g., Cargo.toml)
    elif manifest_file.endswith(".toml"):
        try:
            data = tomllib.loads(decoded_content)
        except Exception:
            return deps

        if "dependencies" in data:
            deps.update(data["dependencies"].keys())

    return deps



def process_repo_tree(repo_tree: dict[str, Any], username: str, repo_name: str, language_map: dict, packages_fetcher: callable):
    """
    Process a repository's tree to extract dependencies.
    - repo_tree: JSON response from GitHub tree API
    - packages_fetcher: callback that makes API call and returns JSON for file content
    """
    repo_results = {lang: set() for lang in language_map}

    for lang, config in language_map.items():
        manifest_files = config.get("manifest", [])
        if isinstance(manifest_files, str):  # backward compatibility
            manifest_files = [manifest_files]

        for branch in repo_tree.get("tree", []):
            for manifest_file in manifest_files:
                print("Checking", manifest_file, "in", branch["path"])
                if manifest_file in branch["path"]:
                    print("Found", manifest_file, "in", branch["path"])
                    packages = packages_fetcher(username, repo_name, branch["path"])
                    encoded_content = packages.get("content")
                    if not encoded_content:
                        continue

                    decoded_content = base64.b64decode(encoded_content).decode("utf-8")
                    deps = parse_manifest(manifest_file, decoded_content, config.get("dependencies_key"))
                    repo_results[lang].update(deps)

    return repo_results


def merge_all_results(all_results: dict[str, set], new_results: dict[str, set]):
    """Merge results from one repo into the global results dict."""
    for lang, deps in new_results.items():
        all_results.setdefault(lang, set()).update(deps)
