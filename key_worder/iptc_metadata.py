from pathlib import Path

from iptcinfo3 import IPTCInfo


def _write_iptc(file_path: Path, fields: dict[str, str | list[str]]) -> None:
    info = IPTCInfo(file_path.resolve(), force=True)
    for key, value in fields.items():
        info[key] = value
    # Avoid iptcinfo3's default backup file ({path}~) when replacing in place.
    info.save(options={"overwrite": True})

def add_stock_iptc_metadata(
    file_path: Path,
    title: str | None,
    description: str | None,
    keywords: list[str],
) -> None:
    fields: dict[str, str | list[str]] = {}
    t = (title or "").strip()
    d = (description or "").strip()
    if t:
        fields["object name"] = t
        fields["headline"] = t  # Getty вимагає headline
    if d:
        fields["caption/abstract"] = d
    if keywords:
        fields["keywords"] = keywords
    if not fields:
        return
    _write_iptc(file_path, fields)
