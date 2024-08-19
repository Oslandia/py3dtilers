from __future__ import annotations

from typing import TYPE_CHECKING

from ..Common import GeometryNode, GeometryTree
from .tile_to_feature import TileToFeatureList

if TYPE_CHECKING:
    from py3dtiles.tileset import TileSet, Tile


class TilesetTree(GeometryTree):

    def __init__(self, tileset: TileSet, tileset_paths, geometric_errors=[None, None, None]):
        root_tile = tileset.root_tile

        root_nodes = list()
        for i, tile in enumerate(root_tile.children):
            offset = [tile.transform[0][3], tile.transform[1][3], tile.transform[2][3]]
            root_node, depth = self.tile_to_node(tile, tileset_paths[i], offset, geometric_errors)
            root_nodes.append(root_node)

        super().__init__(root_nodes)

    def tile_to_node(self, tile: Tile, tileset_path, offset, geometric_errors=[None, None, None]):
        """
        Create a GeometryNode and its children from tiles.
        The geometric error of the nodes depends on their depth in the tileset hierarchy.
        A node should always have a lower geometric error than its parent.
        The root of the tree should have the highest geometric error and the leaves the lowest geometric error.
        :param tile: the tile to convert to node
        :param tileset_path: the path of the original tileset of the tile
        :param offset: the offset used to translate the features of this tile
        :param geometric_errors: if not None, use the geometric error of the current depth to overwrite the tile geometric error

        :return: a GeometryNode, an Int
        """
        children_depth = 0
        children = list()
        if len(tile.children) > 0:
            for child in tile.children:
                child, child_depth = self.tile_to_node(child, tileset_path, offset, geometric_errors)
                children.append(child)
                children_depth = child_depth if child_depth > children_depth else children_depth

        i = children_depth if children_depth < len(geometric_errors) else len(geometric_errors) - 1
        geometric_error = tile.geometric_error if geometric_errors[i] is None else geometric_errors[i]

        feature_list = TileToFeatureList(tile, tileset_path)
        feature_list.translate_features(offset)
        node = GeometryNode(feature_list, geometric_error, with_texture=True)
        node.set_child_nodes(children)

        return node, children_depth + 1
