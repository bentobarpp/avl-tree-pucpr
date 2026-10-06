"""
Árvore AVL (BST auto-balanceada) com log detalhado de cada cálculo.

Para cada inserção e remoção, o código:
  1. Executa a operação padrão de BST (inserir / remover).
  2. Sobe pelos ancestrais recalculando altura e Fator de Balanceamento (FB):
         FB(nó) = altura(filho_esquerdo) - altura(filho_direito)
  3. Se |FB| > 1, aplica a rotação correta (LL, RR, LR ou RL).

Toda essa sequência de cálculos é registrada em `self.log` (lista de
strings) para que possa ser exibida no terminal e reaproveitada no README.
"""

from __future__ import annotations
from typing import Optional, List


class Node:
    __slots__ = ("key", "left", "right", "height")

    def __init__(self, key: int):
        self.key = key
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.height = 1  # altura de um nó recém-criado (folha) = 1


class AVLTree:
    def __init__(self):
        self.root: Optional[Node] = None
        self.log: List[str] = []

    # ---------------------------------------------------------------- utils
    @staticmethod
    def _h(node: Optional[Node]) -> int:
        return node.height if node else 0

    @staticmethod
    def _bf(node: Optional[Node]) -> int:
        if node is None:
            return 0
        return AVLTree._h(node.left) - AVLTree._h(node.right)

    def _update_height(self, node: Node) -> None:
        node.height = 1 + max(self._h(node.left), self._h(node.right))

    def _log(self, msg: str = "") -> None:
        self.log.append(msg)

    # ------------------------------------------------------------ rotations
    def _rotate_right(self, y: Node) -> Node:
        x = y.left
        t2 = x.right

        x.right = y
        y.left = t2

        self._update_height(y)
        self._update_height(x)

        self._log(
            f"      -> Rotação à DIREITA em torno de {y.key}: "
            f"{x.key} sobe, {y.key} desce para a direita de {x.key}"
            + (f", subárvore {t2.key} é realocada como filho esquerdo de {y.key}" if t2 else "")
        )
        return x

    def _rotate_left(self, x: Node) -> Node:
        y = x.right
        t2 = y.left

        y.left = x
        x.right = t2

        self._update_height(x)
        self._update_height(y)

        self._log(
            f"      -> Rotação à ESQUERDA em torno de {x.key}: "
            f"{y.key} sobe, {x.key} desce para a esquerda de {y.key}"
            + (f", subárvore {t2.key} é realocada como filho direito de {x.key}" if t2 else "")
        )
        return y

    def _rebalance(self, node: Node) -> Node:
        self._update_height(node)
        bf = self._bf(node)
        h_left = self._h(node.left)
        h_right = self._h(node.right)
        self._log(
            f"   nó {node.key}: altura(esq={node.left.key if node.left else '-'})={h_left}, "
            f"altura(dir={node.right.key if node.right else '-'})={h_right}  =>  "
            f"FB({node.key}) = {h_left} - {h_right} = {bf}"
        )

        if bf > 1:
            # pende para a esquerda
            if self._bf(node.left) >= 0:
                self._log(f"   |FB({node.key})| = {bf} > 1 e filho esquerdo não-negativo => caso LL")
                return self._rotate_right(node)
            else:
                self._log(f"   |FB({node.key})| = {bf} > 1 e filho esquerdo negativo => caso LR")
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

        if bf < -1:
            # pende para a direita
            if self._bf(node.right) <= 0:
                self._log(f"   |FB({node.key})| = {abs(bf)} > 1 e filho direito não-positivo => caso RR")
                return self._rotate_left(node)
            else:
                self._log(f"   |FB({node.key})| = {abs(bf)} > 1 e filho direito positivo => caso RL")
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

        return node

    # -------------------------------------------------------------- insert
    def insert(self, key: int) -> bool:
        """Insere `key`. Retorna False se a chave já existe (sem duplicatas)."""
        self._log(f"\n=== INSERIR {key} ===")
        if self._find(self.root, key) is not None:
            self._log(f"   {key} já existe na árvore -> inserção ignorada (BST não admite chaves duplicadas).")
            return False
        self.root = self._insert(self.root, key)
        return True

    def _find(self, node: Optional[Node], key: int) -> Optional[Node]:
        while node:
            if key == node.key:
                return node
            node = node.left if key < node.key else node.right
        return None

    def _insert(self, node: Optional[Node], key: int) -> Node:
        if node is None:
            self._log(f"   {key} inserido como folha.")
            return Node(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        return self._rebalance(node)

    # -------------------------------------------------------------- delete
    def delete(self, key: int) -> bool:
        self._log(f"\n=== REMOVER {key} ===")
        if self._find(self.root, key) is None:
            self._log(f"   {key} não está na árvore -> nada a remover.")
            return False
        self.root = self._delete(self.root, key)
        return True

    def _min_node(self, node: Node) -> Node:
        while node.left:
            node = node.left
        return node

    def _delete(self, node: Optional[Node], key: int) -> Optional[Node]:
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None and node.right is None:
                self._log(f"   {key} é folha -> removido diretamente.")
                return None
            if node.left is None:
                self._log(f"   {key} tem só filho direito ({node.right.key}) -> filho assume o lugar.")
                return node.right
            if node.right is None:
                self._log(f"   {key} tem só filho esquerdo ({node.left.key}) -> filho assume o lugar.")
                return node.left

            successor = self._min_node(node.right)
            self._log(
                f"   {key} tem dois filhos -> sucessor in-order (menor da subárvore direita) = {successor.key}; "
                f"{successor.key} substitui {key} e é removido da subárvore direita."
            )
            node.key = successor.key
            node.right = self._delete(node.right, successor.key)

        return self._rebalance(node)

    # ------------------------------------------------------------- display
    def inorder(self) -> List[int]:
        out: List[int] = []

        def rec(n):
            if n:
                rec(n.left)
                out.append(n.key)
                rec(n.right)

        rec(self.root)
        return out

    def height(self) -> int:
        return self._h(self.root)

    def ascii(self) -> str:
        """Representação textual simples (para debug rápido no terminal)."""
        lines: List[str] = []

        def rec(node: Optional[Node], prefix: str, is_left: bool):
            if node is None:
                return
            rec(node.right, prefix + ("│   " if is_left else "    "), False)
            connector = "└── " if is_left else "┌── "
            lines.append(f"{prefix}{connector}{node.key} (fb={self._bf(node)}, h={node.height})")
            rec(node.left, prefix + ("    " if is_left else "│   "), True)

        if self.root is None:
            return "(árvore vazia)"
        rec(self.root.right, "", False)
        lines.append(f"{self.root.key} (fb={self._bf(self.root)}, h={self.root.height})")
        rec(self.root.left, "", True)
        return "\n".join(lines)
