import platform
import argparse
from pathlib import Path


def get_version() -> str:
    """Get Minecraft version from command line arguments"""
    parser = argparse.ArgumentParser(description="Extract Minecraft data.")
    parser.add_argument("version", help="Minecraft version (e.g., 1.19.2)")
    args = parser.parse_args()
    return args.version


def get_jar_path(version: str) -> Path:
    """Get the path to the Minecraft JAR file for the specified version"""
    if platform.system() == "Windows":
        minecraft_dir = Path.home() / "AppData" / "Roaming" / ".minecraft"
    else:
        minecraft_dir = Path.home() / ".minecraft"
    return minecraft_dir / "versions" / version / f"{version}.jar"


def is_version_1_13_or_later(version: str) -> bool:
    """Check if the Minecraft version is 1.13 or later"""
    major, minor, _patch = map(int, version.split("."))
    if major < 1:
        return False
    if major == 1 and minor < 13:
        return False
    return True
