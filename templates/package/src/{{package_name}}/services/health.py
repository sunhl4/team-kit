from {{package_name}}.models.identity import PackageId


def health(package_id: PackageId) -> dict[str, str]:
    return {"id": package_id.value, "summary": "ok"}
