"""
Gera diagramas SVG de uma AVLTree, sem depender de bibliotecas externas
(sem graphviz / matplotlib) — só a biblioteca padrão do Python.

Cada nó mostra: chave, FB (fator de balanceamento) e h (altura).
Nós em `highlight` (ex.: o nó que acabou de ser inserido/removido, ou o
pivô de uma rotação) ficam destacados em outra cor.
"""

from typing import Optional, Set
from avl_tree import AVLTree, Node

NODE_R = 20
X_GAP = 56
Y_GAP = 86
MARGIN = 40

COLOR_BG = "#ffffff"
COLOR_EDGE = "#94a3b8"
COLOR_NODE = "#1e293b"
COLOR_NODE_FILL = "#e2e8f0"
COLOR_HILITE_FILL = "#fde68a"
COLOR_HILITE_STROKE = "#d97706"
COLOR_TEXT = "#0f172a"
COLOR_SUB = "#475569"


def _assign_positions(root: Optional[Node]):
    """Posição x = índice na travessia in-order; y = profundidade."""
    positions = {}
    counter = [0]

    def rec(node: Optional[Node], depth: int):
        if node is None:
            return
        rec(node.left, depth + 1)
        x = counter[0]
        counter[0] += 1
        positions[id(node)] = (x, depth, node)
        rec(node.right, depth + 1)

    rec(root, 0)
    return positions


def render_svg(tree: AVLTree, path: str, title: str = "", highlight: Optional[Set[int]] = None) -> None:
    highlight = highlight or set()
    positions = _assign_positions(tree.root)

    if not positions:
        width, height = 300, 120
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<rect width="100%" height="100%" fill="{COLOR_BG}"/>',
            f'<text x="{width/2}" y="{height/2}" text-anchor="middle" font-family="monospace" font-size="14" fill="{COLOR_SUB}">(árvore vazia)</text>',
            "</svg>",
        ]
        with open(path, "w") as f:
            f.write("\n".join(svg))
        return

    max_x = max(p[0] for p in positions.values())
    max_y = max(p[1] for p in positions.values())

    width = MARGIN * 2 + (max_x + 1) * X_GAP
    height = MARGIN * 2 + 36 + (max_y + 1) * Y_GAP

    def coord(node: Node):
        x, depth, _ = positions[id(node)]
        return (MARGIN + x * X_GAP + X_GAP / 2, MARGIN + 36 + depth * Y_GAP)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="Helvetica,Arial,sans-serif">',
        f'<rect width="100%" height="100%" fill="{COLOR_BG}"/>',
    ]

    if title:
        svg.append(
            f'<text x="{width/2}" y="24" text-anchor="middle" font-size="16" font-weight="600" fill="{COLOR_TEXT}">{title}</text>'
        )

    # edges first (so nodes draw on top)
    def draw_edges(node: Optional[Node]):
        if node is None:
            return
        x1, y1 = coord(node)
        for child in (node.left, node.right):
            if child:
                x2, y2 = coord(child)
                svg.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COLOR_EDGE}" stroke-width="2"/>')
        draw_edges(node.left)
        draw_edges(node.right)

    draw_edges(tree.root)

    def draw_nodes(node: Optional[Node]):
        if node is None:
            return
        x, y = coord(node)
        fill = COLOR_HILITE_FILL if node.key in highlight else COLOR_NODE_FILL
        stroke = COLOR_HILITE_STROKE if node.key in highlight else COLOR_NODE
        bf = AVLTree._bf(node)
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{NODE_R}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        svg.append(
            f'<text x="{x:.1f}" y="{y+5:.1f}" text-anchor="middle" font-size="14" font-weight="700" fill="{COLOR_TEXT}">{node.key}</text>'
        )
        svg.append(
            f'<text x="{x:.1f}" y="{y+NODE_R+14:.1f}" text-anchor="middle" font-size="10" fill="{COLOR_SUB}">fb={bf} h={node.height}</text>'
        )
        draw_nodes(node.left)
        draw_nodes(node.right)

    draw_nodes(tree.root)
    svg.append("</svg>")

    with open(path, "w") as f:
        f.write("\n".join(svg))
