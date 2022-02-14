def make_vcard(
    name,
    phone_number,
):
    return [
        "BEGIN:VCARD",
        "VERSION:2.1",
        f"N:{name};",
        f"FN:{name}",
        f"TEL;WORK;VOICE:{phone_number}",
        f"REV:1",
        "END:VCARD",
    ]


def write_vcard(f, vcard):
    with open(f, "a") as f:
        f.writelines([line + "\n" for line in vcard])
