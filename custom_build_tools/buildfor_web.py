import shutil
from pathlib import Path
from zipfile import ZipFile
import logging
from datetime import datetime

logging.basicConfig(filename="build.log",
                    level=logging.INFO,
                    filemode="w",
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    encoding="utf-8",
                    datefmt="%d-%m-%Y%H:%M:%S")
console = logging.StreamHandler()
logging.getLogger().addHandler(console)


INCLUDES = [
    "webserver.py",
    "requirements.txt",
    "templates",
    "static",
    "core",
    "config_template.json"
]

root = Path(__file__).parent

DEST = root / "build-web"

def clear_old_build():
    if DEST.exists():
        shutil.rmtree(DEST)
        msg = f"old build folder deleted: {DEST}"
        logging.info(msg)
    DEST.mkdir(exist_ok=True)

def copy_items():
    not_copied_items = []
    copied_items = []
    for item in INCLUDES:
        src_path = root / item
        if not src_path.exists():
            msg = f"Item not found: {src_path}"
            logging.warning(msg)
            not_copied_items.append(item)
            continue

        dest_path = DEST / item

        try:
            if src_path.is_dir():
                shutil.copytree(src_path, dest_path)
            elif src_path.is_file():
                shutil.copy2(src_path, dest_path)
            copied_items.append(item)

        except Exception as e:
            not_copied_items.append(item)
            msg = f"Could not copy {src_path} to {dest_path}: {e}"
            logging.info(msg)

    if not not_copied_items:
        errors = 0
    else:
        errors = len(not_copied_items)
    msg = f"building completed with {errors} error(s)"
    logging.info(msg)
    if errors != 0:
        msg = f"Not copied items: {not_copied_items} | No .ZIP File created!"
        logging.info(msg)
        return errors
    else:
        zip_file = create_zipfile()
        msg = f"ZIP file created: {zip_file}"
        logging.info(msg)
        return True


def create_zipfile():
    zip_folder = root / "build-zip"
    zip_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + "webui.zip"
    zip_file  = zip_folder / zip_name
    zip_folder.mkdir(exist_ok=True)

    with ZipFile(file=zip_file, mode="w") as archive:
        for item in DEST.rglob("*"):
            archive.write(item, arcname=item.relative_to(DEST))
    return zip_file
if __name__ == "__main__":
    clear_old_build()
    outcome = copy_items()
    if outcome is not True:
        msg = "Building failed"
        logging.error(msg)
    else:
        msg = "Building succeeded"
        logging.info(msg)