import zipfile
import sys
from pathlib import Path
from get_id_utils import get_version, get_jar_path
from get_id_utils import is_version_1_xx_or_later, save_to_file


def extract_particle_ids(minecraft_jar_path, minecraft_dir, version):
    """Extract particle IDs from the Minecraft JAR file"""
    extracted_path = Path(minecraft_dir) / "versions" / version
    try:
        with zipfile.ZipFile(minecraft_jar_path, "r") as jar:
            jar.extractall(extracted_path)
    except (FileNotFoundError, zipfile.BadZipFile) as e:
        print(f"Error: {e}")
        sys.exit(1)

    particle_names = []
    particle_path = extracted_path / "assets/minecraft/particles"
    json_files = particle_path.glob("*.json")

    for file_path in json_files:
        particle_name = file_path.stem
        particle_names.append(particle_name)

    return sorted(particle_names)


def main():
    """Main function to extract and save particle IDs"""
    version = get_version()
    if not is_version_1_xx_or_later(version, 14):
        print("Error: This script only supports Minecraft version 1.14 and above.")
        return

    version_path = version.replace(".", "_")
    minecraft_jar_path = get_jar_path(version)

    particle_names = extract_particle_ids(
        minecraft_jar_path, Path(minecraft_jar_path).parent, version
    )
    script_dir = Path(__file__).resolve().parent
    output_dir = script_dir / "ID_list_files"
    output_dir.mkdir(exist_ok=True)
    file_name = f"particle_{version_path}.py"
    output_file = output_dir / file_name
    save_to_file(particle_names, output_file, version, version_path, "Particle")
    print(f"Particle names list has been saved to:\n{output_file}.")


if __name__ == "__main__":
    main()
