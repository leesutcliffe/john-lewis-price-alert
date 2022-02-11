from pathlib import Path

import toml

ROOT = Path(__file__).parent.parent
toml_path = ROOT / "pyproject.toml"
lock_path = ROOT / "poetry.lock"
requirements_path = ROOT / "requirements.txt"

parsed_toml = toml.load(toml_path)
main_deps = parsed_toml["tool"]["poetry"]["dependencies"]
packages = [i for i in main_deps.keys() if i != "python"]

parsed_lock = toml.load(lock_path)
package_with_version = {i["name"]: i["version"] for i in parsed_lock["package"] if i["name"] in packages}

with open(requirements_path, "w") as f:
    for k, v in package_with_version.items():
        f.write(f"{k}=={v}\n")
