class DoctorNode:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


class DoctorTree:
    def __init__(self):
        self.root = None

    def find(self, node, name):
        if node is None or node.name == name:
            return node

        return (
            self.find(node.left, name)
            or self.find(node.right, name)
        )

    def insert(self, parent_name, name, side):
        if side not in ("left", "right"):
            raise ValueError("Side must be 'left' or 'right'.")

        parent = self.find(self.root, parent_name)

        if parent is None:
            raise ValueError(f"Parent {parent_name} not found.")

        if self.find(self.root, name) is not None:
            raise ValueError(
                "Doctor names must be unique in this model."
            )

        if getattr(parent, side) is not None:
            raise ValueError(
                f"The {side} position is already occupied."
            )

        setattr(parent, side, DoctorNode(name))

    def preorder(self, node):
        names = []

        def visit(current):
            if current is not None:
                names.append(current.name)
                visit(current.left)
                visit(current.right)

        visit(node)
        return names

    def inorder(self, node):
        names = []

        def visit(current):
            if current is not None:
                visit(current.left)
                names.append(current.name)
                visit(current.right)

        visit(node)
        return names

    def postorder(self, node):
        names = []

        def visit(current):
            if current is not None:
                visit(current.left)
                visit(current.right)
                names.append(current.name)

        visit(node)
        return names


def run_tests():
    tree = DoctorTree()

    # Empty tree
    for traversal in (
        tree.preorder,
        tree.inorder,
        tree.postorder
    ):
        assert traversal(tree.root) == []

    # Single doctor and the assignment's example hierarchy
    tree.root = DoctorNode("Dr. Croft")
    assert tree.preorder(tree.root) == ["Dr. Croft"]

    tree.insert("Dr. Croft", "Dr. Goldsmith", "right")
    tree.insert("Dr. Croft", "Dr. Phan", "left")
    tree.insert("Dr. Phan", "Dr. Carson", "right")
    tree.insert("Dr. Phan", "Dr. Morgan", "left")

    assert tree.preorder(tree.root) == [
        "Dr. Croft",
        "Dr. Phan",
        "Dr. Morgan",
        "Dr. Carson",
        "Dr. Goldsmith"
    ]

    assert tree.inorder(tree.root) == [
        "Dr. Morgan",
        "Dr. Phan",
        "Dr. Carson",
        "Dr. Croft",
        "Dr. Goldsmith"
    ]

    assert tree.postorder(tree.root) == [
        "Dr. Morgan",
        "Dr. Carson",
        "Dr. Phan",
        "Dr. Goldsmith",
        "Dr. Croft"
    ]

    # Missing parent, invalid side, occupied side, duplicate name
    before = tree.preorder(tree.root)

    invalid_insertions = [
        ("Missing", "Dr. Lee", "left"),
        ("Dr. Croft", "Dr. Lee", "middle"),
        ("Dr. Croft", "Dr. Lee", "left"),
        ("Dr. Morgan", "Dr. Phan", "left"),
    ]

    for args in invalid_insertions:
        try:
            tree.insert(*args)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Invalid insertion should raise ValueError."
            )

    assert tree.preorder(tree.root) == before

    print("Preorder:", tree.preorder(tree.root))
    print("Inorder:", tree.inorder(tree.root))
    print("Postorder:", tree.postorder(tree.root))
    print("All doctor tree tests passed.")


if __name__ == "__main__":
    run_tests()
