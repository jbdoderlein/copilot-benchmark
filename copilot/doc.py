"""Representation of a copilot document."""
import os

class Document:
    """Copilot Document"""
    def __init__(self, path : str,
                    lang : str,
                    insert_spaces : bool =True,
                    tab_size : int =4,
                    indent_size : int =4):
        self.uri = "file://" + os.path.abspath(path)
        self.relative_path = os.path.basename(path)
        self.path = path
        self.lang = lang
        self.insert_spaces = insert_spaces
        self.tab_size = tab_size
        self.indent_size = indent_size
        self.content = ""

        with open(path, 'r') as file:
            self.update_content(file.read())


    def register_positions(self) -> None:
        """Update cursor position in content where $$$ or end of document"""
        lines = self.content.split('\n')
        for i, line in enumerate(lines):
            if "$$$" in line:
                self.position.append({
                    "line": i,
                    "character": line.index("$$$")
                })
        self.content = self.content.replace("$$$", "")

    def update_content(self, content : str) -> None:
        """Update the content of the document"""
        self.content = content
        self.position = []
        self.register_positions()

    def get_current_curor_position(self) -> dict:
        """Get the current cursor position"""
        if len(self.position) == 0:
            raise Exception("No cursor position found")
        return self.position[0]

    def add_content(self, content : str, keep_cursor : bool = False) -> None:
        """Add content to the document at the current cursor position"""
        position = self.get_current_curor_position()['character']
        for line in self.content.split('\n')[:self.get_current_curor_position()['line']]:
            position += len(line) + 1
        self.content = self.content[:position] + content + "\n" + self.content[position:]
        # Update all cursors
        for i, _ in enumerate(self.position):
            self.position[i]["line"] += content.count('\n')+1
        if keep_cursor:
            self.position[0]["character"] = 0
        else:
            self.position.pop(0)

    def save(self, path):
        """Save the document to a file"""
        with open(path, 'w') as file:
            file.write(self.content)

    def to_dict(self) -> dict:
        """Convert the document to a copilot dictionary"""
        return {
            "uri": self.uri,
            "relativePath": self.relative_path,
            "source": self.content,
            "languageId": self.lang,
            "insertSpaces": self.insert_spaces,
            "tabSize": self.tab_size,
            "indentSize": self.indent_size,
            "position": self.get_current_curor_position(),
            "path": self.path
        }
