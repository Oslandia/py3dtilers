import unittest
from argparse import Namespace
from pathlib import Path

from py3dtilers.ObjTiler.ObjTiler import ObjTiler


def get_default_namespace():
    return Namespace(obj=None, loa=None, lod1=False, crs_in='EPSG:3946',
                     crs_out='EPSG:3946', offset=[0, 0, 0], with_texture=False, scale=1,
                     output_dir=None, geometric_error=[None, None, None], kd_tree_max=None,
                     texture_lods=0, keep_ids=[], exclude_ids=[])


class Test_Tile(unittest.TestCase):

    def test_basic_case(self):
        obj_tiler = ObjTiler()
        obj_tiler.files = [Path('tests/obj_tiler_data/Cube/cube_1.obj'), Path('tests/obj_tiler_data/Cube/cube_2.obj')]
        obj_tiler.args = get_default_namespace()
        obj_tiler.args.output_dir = Path("tests/obj_tiler_data/generated_tilesets/basic_case")

        tileset = obj_tiler.from_obj_directory()
        if tileset is not None:
            tileset.write_as_json(Path(obj_tiler.args.output_dir))

    def test_texture(self):
        obj_tiler = ObjTiler()
        obj_tiler.files = [Path('tests/obj_tiler_data/TexturedCube/cube.obj')]
        obj_tiler.args = get_default_namespace()
        obj_tiler.args.output_dir = Path("tests/obj_tiler_data/generated_tilesets/texture")
        obj_tiler.args.offset = [1843397, 5173891, 300]  # Arbitrary offset to place the 3DTiles in Lyon city
        obj_tiler.args.with_texture = True
        obj_tiler.args.scale = 50

        tileset = obj_tiler.from_obj_directory()
        if tileset is not None:
            tileset.write_as_json(Path(obj_tiler.args.output_dir))

    def test_texture_lods(self):
        obj_tiler = ObjTiler()
        obj_tiler.files = [Path('tests/obj_tiler_data/TexturedCube/cube.obj')]
        obj_tiler.args = get_default_namespace()
        obj_tiler.args.output_dir = Path("tests/obj_tiler_data/generated_tilesets/texture_lods")
        obj_tiler.args.offset = [1843397, 5173891, 300]  # Arbitrary offset to place the 3DTiles in Lyon city
        obj_tiler.args.with_texture = True
        obj_tiler.args.scale = 50
        obj_tiler.args.texture_lods = 5

        tileset = obj_tiler.from_obj_directory()
        if tileset is not None:
            tileset.write_as_json(Path(obj_tiler.args.output_dir))


if __name__ == '__main__':
    unittest.main()
