import sys
from get_block_id import main as get_block_id_main
from get_entity_id import main as get_entity_id_main
from get_particle_id import main as get_particle_id_main
from get_id_utils import get_version


def main():
    """Main function to extract and save all IDs"""
    version = get_version()
    sys.argv = [sys.argv[0], version]

    print("Extracting Block ID...")
    get_block_id_main()

    print("Extracting Entity ID...")
    get_entity_id_main()

    print("Extracting Particle ID...")
    get_particle_id_main()


if __name__ == "__main__":
    main()
