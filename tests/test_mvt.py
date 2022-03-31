"""tests ard_tiler.mosaic."""

import json
import os
import numpy as np

import pytest

from rio_tiler.io import COGReader
from rio_tiler_mvt.mvt import encoder

import vector_tile_base

asset = os.path.join(os.path.dirname(__file__), "fixtures", "test.tif")
x = 72
y = 63
z = 7

tile, mask = COGReader(asset).tile(x, y, z, resampling_method="nearest")


def test_mvt_encoder():
    """Test MVT encoder."""
    # test with default
    vt = encoder(tile, mask)
    mvt = vector_tile_base.VectorTile(vt)
    assert len(mvt.layers) == 1
    layer = mvt.layers[0]
    assert layer.name == "my_layer"
    assert layer.extent == 4096
    assert layer.version == 2

    assert len(layer.features) == 75
    feat = layer.features[0]
    assert feat.type == "point"
    props = feat.attributes
    assert len(props) == 1
    assert props["band1"] == "21.08714485168457"

    # Test polygon
    vt = encoder(tile, mask, feature_type="polygon")
    mvt = vector_tile_base.VectorTile(vt)
    layer = mvt.layers[0]
    feat = layer.features[0]
    assert feat.type == "polygon"
    props = feat.attributes
    assert props["band1"] == "21.08714485168457"

    # Test band name
    vt = encoder(tile, mask, band_names=["pop"])
    mvt = vector_tile_base.VectorTile(vt)
    props = mvt.layers[0].features[0].attributes
    assert props["pop"] == "21.08714485168457"

    # Test layer name
    vt = encoder(tile, mask, layer_name="facebook")
    mvt = vector_tile_base.VectorTile(vt)
    assert len(mvt.layers) == 1
    layer = mvt.layers[0]
    assert layer.name == "facebook"

    # Test bad feature type
    with pytest.raises(Exception):
        encoder(tile, mask, feature_type="somethingelse")

    
def test_clipped_polygons():
    clipped_polygons = json.load(open(os.path.join(os.path.dirname(__file__), "fixtures", "clipped_polygons.json")))
    layer_channels = json.load(open(os.path.join(os.path.dirname(__file__), "fixtures", "layer_channels.json")))
    mask = np.load(os.path.join(os.path.dirname(__file__), "fixtures", "mask.np"))
    tile = np.load(os.path.join(os.path.dirname(__file__), "fixtures", "tile.np"))

    clipped_polygons = {tuple(d["key"]): d["value"] for d in clipped_polygons}
    # print(tile)
    # print(mask)

    vt = encoder(tile, mask, layer_channels, "tile", feature_type="polygon", clipped_polygons=clipped_polygons)
    mvt = vector_tile_base.VectorTile(vt)

    print(mvt.layers[0].features[0])