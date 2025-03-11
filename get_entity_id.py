import sys
import zipfile
import glob
from pathlib import Path
from get_id_utils import get_version, get_jar_path
from get_id_utils import is_version_1_xx_or_later, save_to_file


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
    if is_version_1_xx_or_later(version, 21):
        entity_path = extracted_path / "data/minecraft/loot_table/entities"
    else:
        entity_path = extracted_path / "data/minecraft/loot_tables/entities"

    json_files = glob.glob(str(entity_path / "*.json"))

    for file_path in json_files:
        entity_name = Path(file_path).stem
        entity_names.append(entity_name)

    return sorted(entity_names)


def main():
    """Main function to extract and save entity IDs"""
    version = get_version()
    version_path = version.replace(".", "_")
    minecraft_jar_path = get_jar_path(version)

    if is_version_1_xx_or_later(version, 13):
        entity_names = extract_entity_ids(
            minecraft_jar_path, Path(minecraft_jar_path).parent, version
        )
        script_dir = Path(__file__).resolve().parent
        output_dir = script_dir / "ID_list_files"
        output_dir.mkdir(exist_ok=True)
        file_name = f"entity_{version_path}.py"
        output_file = output_dir / file_name
        save_to_file(entity_names, output_file, version, version_path, "Entity")
        print(f"Entity names list has been saved to:\n{output_file}.")
    else:
        print("Error: This script only supports Minecraft version 1.13 and above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
