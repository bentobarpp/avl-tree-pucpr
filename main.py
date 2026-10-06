"""
Executa a sequência de inserções e remoções pedida, gerando:
  - log.txt                 -> log textual completo com todos os cálculos de FB e rotações
  - diagrams/insert_NN.svg  -> estado da árvore após cada inserção
  - diagrams/remove_NN.svg  -> estado da árvore após cada remoção
  - diagrams/final_*.svg    -> estados finais (após inserções / após remoções)
"""

from avl_tree import AVLTree
from svg_render import render_svg

INSERTS = [55, 26, 29, 13, 12, 11, 16, 1, 5, 29, -15, 4, 16, 8, 4, 5, 3, 1312, 100, 88]
REMOVES = [4, 29, 100, 5, -15, 16, 55]


def main():
    tree = AVLTree()
    full_log = []

    full_log.append("##########################################################")
    full_log.append("# FASE 1 - INSERÇÕES")
    full_log.append("##########################################################")

    for i, key in enumerate(INSERTS, start=1):
        before_len = len(tree.log)
        inserted = tree.insert(key)
        full_log.extend(tree.log[before_len:])
        full_log.append(f"\n   Árvore após processar {key}:\n" + _indent(tree.ascii()))
        render_svg(
            tree,
            f"diagrams/insert_{i:02d}_{key}.svg",
            title=f"Após inserir {key} (passo {i}/{len(INSERTS)})",
            highlight={key} if inserted else set(),
        )

    render_svg(tree, "diagrams/final_after_insertions.svg", title="Árvore AVL após todas as inserções")
    full_log.append("\n" + "=" * 58)
    full_log.append("Árvore final após todas as inserções:")
    full_log.append(_indent(tree.ascii()))
    full_log.append(f"In-order: {tree.inorder()}")
    full_log.append(f"Altura da árvore: {tree.height()}")

    full_log.append("\n\n##########################################################")
    full_log.append("# FASE 2 - REMOÇÕES")
    full_log.append("##########################################################")

    for i, key in enumerate(REMOVES, start=1):
        before_len = len(tree.log)
        tree.delete(key)
        full_log.extend(tree.log[before_len:])
        full_log.append(f"\n   Árvore após remover {key}:\n" + _indent(tree.ascii()))
        render_svg(
            tree,
            f"diagrams/remove_{i:02d}_{key}.svg",
            title=f"Após remover {key} (passo {i}/{len(REMOVES)})",
        )

    render_svg(tree, "diagrams/final_after_removals.svg", title="Árvore AVL final (após todas as remoções)")
    full_log.append("\n" + "=" * 58)
    full_log.append("Árvore final após todas as remoções:")
    full_log.append(_indent(tree.ascii()))
    full_log.append(f"In-order: {tree.inorder()}")
    full_log.append(f"Altura da árvore: {tree.height()}")

    with open("log.txt", "w") as f:
        f.write("\n".join(full_log))

    print("\n".join(full_log))
    print("\n\nLog completo salvo em log.txt")
    print("Diagramas SVG salvos em diagrams/")


def _indent(text: str, prefix: str = "      ") -> str:
    return "\n".join(prefix + line for line in text.splitlines())


if __name__ == "__main__":
    main()
