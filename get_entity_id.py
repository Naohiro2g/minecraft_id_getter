import sys
import zipfile
import glob
from pathlib import Path
from get_id_utils import get_version, get_jar_path
from get_id_utils import is_version_1_21_or_later


def extract_entity_ids(minecraft_jar_path, minecraft_dir, version):
    """Extract entity IDs from the Minecraft JAR file"""
    extracted_path = Path(minecraft_dir) / "versions" / version
    try:
        with zipfile.ZipFile(minecraft_jar_path, "r") as jar:
            jar.extractall(extracted_path)
    except (FileNotFoundError, zipfile.BadZipFile) as e:
        print(f"Error: {e}")
        sys.exit(1)

    entity_names = []
    if is_version_1_21_or_later(version):
        entity_path = extracted_path / "data/minecraft/loot_table/entities"
    else:
        entity_path = extracted_path / "data/minecraft/loot_tables/entities"

    json_files = glob.glob(str(entity_path / "*.json"))

    for file_path in json_files:
        entity_name = Path(file_path).stem
        entity_names.append(entity_name)

    return sorted(entity_names)


def save_to_file(entity_names, output_file, version, version_path):
    """Save entity IDs to a Python file"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Entity ID list of Minecraft version {version}\n")
        f.write(
            f"#   auto-generated by get_entity_id.py as entity_{version_path}.py\n\n"
        )
        for name in entity_names:
            constant_name = name.upper()
            f.write(f'{constant_name} = "{name}"\n')


def main():
    """Main function to extract and save entity IDs"""
    version = get_version()
    version_path = version.replace(".", "_")
    minecraft_jar_path = get_jar_path(version)

    entity_names = extract_entity_ids(
        minecraft_jar_path, Path(minecraft_jar_path).parent, version
    )
    script_dir = Path(__file__).resolve().parent
    file_name = f"entity_{version_path}.py"
    output_file = script_dir / file_name
    save_to_file(entity_names, output_file, version, version_path)
    print(f"Entity names list has been saved to:\n{output_file}.")


if __name__ == "__main__":
    main()
