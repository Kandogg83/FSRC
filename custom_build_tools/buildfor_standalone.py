from version  import __version__
from textwrap import dedent

def convert_to_fourpart_version():
    ver_split = __version__.split('.')
    if len(ver_split) < 4:
        for i in range(4 - len(ver_split)):
            ver_split.append('0')
    elif len(ver_split) > 4:
        ver_split = ver_split[:4]
    return ".".join(ver_split)

def create_versiontxt():
    with open("../version_info.txt", "w", encoding="utf-8") as f:
        #dedent removes largest-common indent
        current_version = dedent(f"""   
            # UTF-8
            VSVersionInfo(
              ffi=FixedFileInfo(
                filevers={version_tuple},
                prodvers={version_tuple},
                mask=0x3f,
                flags=0x0,
                OS=0x4,
                fileType=0x1,
                subtype=0x0,
                date=(0, 0)
                ),
              kids=[
                StringFileInfo([
                  StringTable(
                    '040904B0',
                    [StringStruct('CompanyName', 'Kando'),
                     StringStruct('FileDescription', 'FSRC Factorio Server Remote Control'),
                     StringStruct('FileVersion', '{formatted_version}'),
                     StringStruct('InternalName', 'fsrc.exe'),
                     StringStruct('OriginalFilename', 'fsrc.exe'),
                     StringStruct('ProductName', 'FSRC'),
                     StringStruct('ProductVersion', '{formatted_version}')])
                  ]),
                VarFileInfo([VarStruct('Translation', [0x0409, 1200])])
              ]
            )
            """)
        f.write(current_version)


formatted_version = convert_to_fourpart_version()
version_tuple = tuple(map(int, formatted_version.split('.')))

create_versiontxt()





