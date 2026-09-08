from mcp.server.fastmcp import FastMCP

mcp = FastMCP("College Support")


@mcp.tool()
def get_college_notice() -> str:
    """Get the latest college notice."""
    from pathlib import Path

    file_path = Path("data/notices/college_notice.txt")

    if file_path.exists():
        return file_path.read_text(encoding="utf-8")

    return "College notice information is not available."


if __name__ == "__main__":
    mcp.run()