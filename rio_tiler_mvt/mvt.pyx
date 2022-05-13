import numpy

from vtzero.tile import Tile, Layer, Point, Polygon

cimport numpy

cpdef bytes encoder(
    data,
    mask,
    list band_names = [],
    str layer_name = "my_layer",
    str feature_type = "point",
    clipped_polygons = {}
):
    cdef int sc = 4096 // data.shape[1]
    cdef tuple indexes = numpy.where(mask)

    cdef tuple idx
    cdef int x, y

    if not band_names:
        band_names = [
          f"band{ix}" for ix in range(1, data.shape[0] + 1)
        ]

    mvt = Tile()
    mvt_layer = Layer(mvt, layer_name.encode())
    for idx in zip(indexes[1], indexes[0]):
        i, j = idx
        x = i * sc
        y = j * sc

        if feature_type == 'point':
            feature = Point(mvt_layer)
            feature.add_point(x + sc / 2, y - sc / 2)

        elif feature_type == 'polygon':
            feature = Polygon(mvt_layer)

            if (i, j) in clipped_polygons:
                coords = clipped_polygons[(i,j)]
                points = []

                prevx, prevy = None, None
                for cx, cy in coords:
                    px, py = x + round(cx * sc), y + round(cy * sc)
                    if px != prevx and py != prevy:
                        points.append((px, py))
                    prevx, prevy = px, py

                if len(points) > 0:
                    feature.add_ring(len(points))
                    for px, py in points:
                        feature.set_point(px, py)

            else:
                feature.add_ring(5)
                feature.set_point(x, y)
                feature.set_point(x + sc, y)
                feature.set_point(x + sc, y - sc)
                feature.set_point(x, y - sc)
                feature.set_point(x, y)

        else:
            raise Exception(f"Invalid geometry type: {feature_type}")

        for bidx in range(data.shape[0]):
            key_str = band_names[bidx].encode()
            value = data[bidx, idx[1], idx[0]]

            t = type(value)
            if t is float or t is numpy.float64 or t is numpy.float32 or t is numpy.float16:
                feature.add_property_float(key_str, value)
            elif t is int or t is numpy.int64 or t is numpy.int32 or t is numpy.int16:
                feature.add_property_uint64_t(key_str, value)
            elif t is str:
                feature.add_property_string(key_str, str(value).encode())
            else:
                raise Exception(f"unsupported type for add_property: {value}")

        feature.commit()

    return mvt.serialize()
