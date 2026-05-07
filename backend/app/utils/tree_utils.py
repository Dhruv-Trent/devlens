def build_file_tree(files):
    root = {
        "name": "root",
        "path": "",
        "type": "folder",
        "children": []
    }

    for file in files:
        parts = file.path.split("/")
        current = root

        for index, part in enumerate(parts):
            is_file = index == len(parts) - 1

            existing = next(
                (child for child in current["children"] if child["name"] == part),
                None
            )

            if existing:
                current = existing
                continue

            node = {
                "name": part,
                "path": "/".join(parts[: index + 1]),
                "type": "file" if is_file else "folder",
                "children": [] if not is_file else [],
            }

            if is_file:
                node["file_id"] = file.id

            current["children"].append(node)
            current = node

    def sort_tree(node):
        node["children"].sort(key=lambda x: (x["type"] == "file", x["name"].lower()))
        for child in node["children"]:
            sort_tree(child)

    sort_tree(root)
    return root