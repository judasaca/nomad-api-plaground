import zipfile
import os
import argparse


def generate_nested_zip(
    output_path: str = "nested_tree.zip",
    depth: int = 3,
    width: int = 2,
):
    """
    Generates a zip file containing a nested folder/file tree structure.

    Args:
        output_path: Path for the output zip file.
        depth: How many levels deep the tree goes (1 = root level only).
        width: How many folders/files are created at each level.
    """
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        _build_tree(zf, depth, width, current_depth=1, parent_path="root")

    print(f"✅ Zip file created: {output_path}")
    print(f"   Depth: {depth}, Width: {width}")


def _build_tree(
    zf: zipfile.ZipFile,
    max_depth: int,
    width: int,
    current_depth: int,
    parent_path: str,
):
    """
    Recursively builds the folder/file tree inside the zip archive.
    """
    # Create text files at the current level
    for i in range(1, width + 1):
        file_name = f"file_depth{current_depth}_item{i}.txt"
        file_path = os.path.join(parent_path, file_name)
        content = (
            f"This is a file at depth level {current_depth}, item {i}.\n"
            f"Full path: {file_path}\n"
        )
        zf.writestr(file_path, content)

    # Recurse into subfolders if we haven't reached max depth
    if current_depth < max_depth:
        for i in range(1, width + 1):
            folder_name = f"folder_depth{current_depth}_item{i}"
            folder_path = os.path.join(parent_path, folder_name)
            _build_tree(
                zf,
                max_depth,
                width,
                current_depth=current_depth + 1,
                parent_path=folder_path,
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a zip file with a nested folder/file tree."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="nested_tree.zip",
        help="Output zip file path (default: nested_tree.zip)",
    )
    parser.add_argument(
        "-d", "--depth",
        type=int,
        default=3,
        help="Number of nesting levels (default: 3)",
    )
    parser.add_argument(
        "-w", "--width",
        type=int,
        default=2,
        help="Number of folders/files per level (default: 2)",
    )

    args = parser.parse_args()

    if args.depth < 1:
        parser.error("Depth must be at least 1.")
    if args.width < 1:
        parser.error("Width must be at least 1.")

    generate_nested_zip(
        output_path=args.output,
        depth=args.depth,
        width=args.width,
    )
