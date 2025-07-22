from typing import List


class Formatter:
    def plural(self, name: str, qu: int) -> str:
        return f"{name}{'s' if qu > 1 else ''}"

    def anchorize(self, name: str) -> str:
        return name.lower().replace(" ", "-")

    def nav_item(self, name: str, anchor: str) -> str:
        raise NotImplementedError

    def a(self, name: str, path: str) -> str:
        raise NotImplementedError

    def b(self, content: str) -> str:
        raise NotImplementedError

    def inline_code(self, content: str) -> str:
        raise NotImplementedError

    def code(self, content: str) -> str:
        raise NotImplementedError

    def section(self, title: str, content: str, anchor: str = "") -> str:
        raise NotImplementedError

    def ul(self, content: List[str]) -> str:
        raise NotImplementedError

    def div(self, *args: str) -> str:
        raise NotImplementedError

    def h1(self, name: str) -> str:
        raise NotImplementedError

    def h2(self, name: str) -> str:
        raise NotImplementedError

    def h3(self, name: str) -> str:
        raise NotImplementedError

    def h4(self, name: str) -> str:
        raise NotImplementedError

    def hr(self) -> str:
        raise NotImplementedError

    def new_line(self) -> str:
        raise NotImplementedError
