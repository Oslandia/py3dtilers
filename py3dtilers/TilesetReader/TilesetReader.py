import sys
import os
from pathlib import Path

from .tileset_tree import TilesetTree
from .TilesetMerger import TilesetMerger
from .reader_utils import read_tilesets
from ..Common import Tiler, FromGeometryTreeToTileset


class TilesetTiler(Tiler):

    def __init__(self):
        super().__init__()
        self.tileset_of_root_tiles = list()

    def parse_command_line(self):
        super().parse_command_line()

        if len(self.args.paths) < 1:
            print("Please provide a path to directory containing the root of your 3DTiles.")
            print("Exiting")
            sys.exit(1)

    def retrieve_files(self, paths):
        """
        Retrieve the files from paths given by the user.
        :param paths: a list of paths
        """
        self.files = []

        for path in paths:
            if os.path.isdir(path):
                self.files.append(path)

        if len(self.files) == 0:
            print("No tileset was found")
            sys.exit(1)
        else:
            print(len(self.files), "tilesets found")

    def get_output_dir(self):
        """
        Return the directory name for the tileset.
        """
        if self.args.output_dir is None:
            return "tileset_reader_output"
        else:
            return self.args.output_dir

    def create_tileset_from_feature_list(self, tileset_tree, extension_name=None):
        """
        Override the parent tileset creation.
        """
        self.create_output_directory()
        return FromGeometryTreeToTileset.convert_to_tileset(tileset_tree, self.args, extension_name, self.get_output_dir())

    def transform_tileset(self, tileset):
        """
        Creates a TilesetTree where each node has FeatureList.
        Then, apply transformations (reprojection, translation, etc) on the FeatureList.
        :param tileset: the TileSet to transform

        :return: a TileSet
        """
        geometric_errors = self.args.geometric_error if hasattr(self.args, 'geometric_error') else [None, None, None]
        for tile in tileset.root_tile.children:
            print(tile.content_uri)
        tileset_tree = TilesetTree(tileset, self.tileset_of_root_tiles, geometric_errors)
        return self.create_tileset_from_feature_list(tileset_tree)

    def read_and_merge_tilesets(self):
        """
        Read all tilesets and merge them into a single TileSet instance with the TilesetMerger.
        The paths of all tilesets are keeped to be able to find the source of each tile.
        :param paths_to_tilesets: the paths of the tilesets

        :return: a TileSet
        """
        tilesets = read_tilesets(self.files)
        tileset, self.tileset_of_root_tiles = TilesetMerger.merge_tilesets(tilesets, self.files)
        return tileset


def main():

    tiler = TilesetTiler()
    tiler.parse_command_line()

    tileset = tiler.read_and_merge_tilesets()

    tileset = tiler.transform_tileset(tileset)
    tileset.write_as_json(Path(tiler.get_output_dir(), 'tileset.json'))


if __name__ == '__main__':
    main()
