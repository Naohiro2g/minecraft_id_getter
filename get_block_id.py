import sys
import zipfile
import glob
from pathlib import Path
from get_id_utils import get_version, get_jar_path
from get_id_utils import is_version_1_xx_or_later, save_to_file


def extract_block_ids(minecraft_jar_path, minecraft_dir, version):
    """Extract block IDs from the Minecraft JAR file"""
    extracted_path = Path(minecraft_dir) / "versions" / version
    try:
        with zipfile.ZipFile(minecraft_jar_path, "r") as jar:
            jar.extractall(extracted_path)
            blockstates_dir = extracted_path / "assets/minecraft/blockstates"
            local_block_ids = []
            json_files = glob.glob(str(blockstates_dir / "*.json"))
            for file_path in json_files:
                block_id = Path(file_path).stem
                local_block_ids.append(block_id)
    except (FileNotFoundError, zipfile.BadZipFile) as e:
        print(f"\nError: {e}\n")
        print(f"Are you sure you have Minecraft {version}? Try another version.")
        sys.exit(1)
    return sorted(local_block_ids)


def main():
    """Main function to extract and save block IDs"""
    version = get_version()
    version_path = version.replace(".", "_")
    minecraft_jar_path = get_jar_path(version)

    if is_version_1_xx_or_later(version, xx=13):
        block_id_list = extract_block_ids(
            minecraft_jar_path, Path(minecraft_jar_path).parent, version
        )
        script_dir = Path(__file__).resolve().parent
        output_dir = script_dir / "ID_list_files"
        output_dir.mkdir(exist_ok=True)
        file_name = f"block_{version_path}.py"
        output_file = output_dir / file_name
        save_to_file(block_id_list, output_file, version, version_path, "Block")
        print(f"Block IDs have been written to:\n{output_file}")
    else:
        print("Error: This script only supports Minecraft version 1.13 and above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
