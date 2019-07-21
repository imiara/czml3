import datetime as dt

import astropy.time
import pytest
from dateutil.tz import tzoffset

from czml3.types import (
    ArcTypeValue,
    Cartesian3Value,
    CartographicDegreesListValue,
    CartographicRadiansListValue,
    ClassificationTypeValue,
    DistanceDisplayConditionValue,
    FontValue,
    HeightReferenceValue,
    ReferenceValue,
    RgbafValue,
    RgbaValue,
    ShadowModeValue,
    TimeInterval,
    Uri,
    format_datetime_like,
)


def test_classification_type():
    expected_result = '"BOTH"'
    cls = ClassificationTypeValue(string="BOTH")
    assert repr(cls) == expected_result


def test_distance_display_condition():
    expected_result = """[
    0,
    150,
    15000000,
    300,
    10000,
    15000000,
    600,
    150,
    15000000
]"""
    dist = DistanceDisplayConditionValue(
        values=[0, 150, 15000000, 300, 10000, 15000000, 600, 150, 15000000]
    )
    assert repr(dist) == expected_result


def test_shadow_mode():
    expected_result = '"CAST_ONLY"'
    shad = ShadowModeValue(string="CAST_ONLY")
    assert repr(shad) == expected_result


def test_invalid_shadow_mode():

    with pytest.raises(ValueError) as excinfo:
        ArcTypeValue(string="SHADOW")
    assert "Invalid input value" in excinfo.exconly()


def test_arc_type():
    expected_result = '"RHUMB"'
    arc = ArcTypeValue(string="RHUMB")
    assert repr(arc) == expected_result


def test_invalid_arc_type():

    with pytest.raises(ValueError) as excinfo:
        ArcTypeValue(string="ARC")
    assert "Invalid input value" in excinfo.exconly()


def test_cartographic_radian_list():
    expected_result = """[
    0,
    1,
    0
]"""
    car = CartographicRadiansListValue(values=[0, 1, 0])
    assert repr(car) == expected_result


def test_invalid_cartograpic_radian_list():

    with pytest.raises(ValueError) as excinfo:
        CartographicRadiansListValue(values=[1])
    assert (
        "Invalid values. Input values should be arrays of size 3 * N"
        in excinfo.exconly()
    )


def test_cartograpic_degree_list():
    expected_result = """[
    15,
    25,
    50
]"""
    car = CartographicDegreesListValue(values=[15, 25, 50])
    assert repr(car) == expected_result


def test_invalid_cartograpic_degree_list():

    with pytest.raises(ValueError) as excinfo:
        CartographicDegreesListValue(values=[15, 25, 50, 30])
    assert (
        "Invalid values. Input values should be arrays of size 3 * N"
        in excinfo.exconly()
    )


@pytest.mark.parametrize("values", [[2, 2], [5, 5, 5, 5, 5]])
def test_bad_cartesian_raises_error(values):
    with pytest.raises(ValueError) as excinfo:
        Cartesian3Value(values=values)

    assert "Input values must have either 3 or N * 4 values" in excinfo.exconly()


def test_height_reference_value():
    expected_result = '"CLAMP_TO_GROUND"'
    height_reference = HeightReferenceValue(string="CLAMP_TO_GROUND")

    assert repr(height_reference) == expected_result


def test_invalid_height_reference_value():

    with pytest.raises(ValueError) as excinfo:
        HeightReferenceValue(string="CLAMP")

    assert "Invalid height reference value." in excinfo.exconly()


def test_reference_value():
    expected_result = '"id#property"'
    reference = ReferenceValue(string="id#property")

    assert repr(reference) == expected_result


def test_invalid_reference_value():
    with pytest.raises(ValueError) as excinfo:
        ReferenceValue(string="id")

    assert (
        "Invalid reference string format. Input must be of the form id#property"
        in excinfo.exconly()
    )


def test_font_value():
    expected_result = '"20px sans-serif"'
    font = FontValue(font="20px sans-serif")

    assert repr(font) == expected_result


def test_font_property_value():
    expected_result = "20px sans-serif"
    font = FontValue(font="20px sans-serif")

    assert font.font == expected_result


def test_bad_rgba_size_values_raises_error():
    with pytest.raises(ValueError) as excinfo:
        RgbaValue(values=[0, 0, 255])

    assert "Input values must have either 4 or N * 5 values, " in excinfo.exconly()


def test_bad_rgba_4_values_raises_error():
    with pytest.raises(ValueError) as excinfo:
        RgbaValue(values=[256, 0, 0, 255])

    assert "Color values must be integers in the range 0-255." in excinfo.exconly()


def test_bad_rgba_5_color_values_raises_error():

    with pytest.raises(ValueError) as excinfo:
        RgbaValue(values=[0, 0.1, 0.3, 0.3, 255])

    assert "Color values must be integers in the range 0-255." in excinfo.exconly()


def test_bad_uri_raises_error():
    with pytest.raises(ValueError) as excinfo:
        Uri(uri="a")

    assert "uri must be a URL or a data URI" in excinfo.exconly()


def test_bad_rgbaf_size_values_raises_error():
    with pytest.raises(ValueError) as excinfo:
        RgbafValue(values=[0, 0, 0.1])

    assert "Input values must have either 4 or N * 5 values, " in excinfo.exconly()


def test_bad_rgbaf_4_values_raises_error():
    with pytest.raises(ValueError) as excinfo:
        RgbafValue(values=[0.3, 0, 0, 1.4])

    assert "Color values must be floats in the range 0-1." in excinfo.exconly()


def test_bad_rgbaf_5_color_values_raises_error():

    with pytest.raises(ValueError) as excinfo:
        RgbafValue(values=[0, 0.1, 0.3, 0.3, 255])

    assert "Color values must be floats in the range 0-1." in excinfo.exconly()


def test_default_time_interval():
    expected_result = '"0000-00-00T00:00:00Z/9999-12-31T24:00:00Z"'
    time_interval = TimeInterval()

    assert repr(time_interval) == expected_result


def test_custom_time_interval():
    tz = tzoffset("UTC+02", dt.timedelta(hours=2))
    start = dt.datetime(2019, 1, 1, 12, 0, tzinfo=dt.timezone.utc)
    end = dt.datetime(2019, 9, 2, 23, 59, 59, tzinfo=tz)

    expected_result = '"2019-01-01T12:00:00Z/2019-09-02T21:59:59Z"'

    time_interval = TimeInterval(start=start, end=end)

    assert repr(time_interval) == expected_result


def test_bad_time_raises_error():
    with pytest.raises(ValueError):
        format_datetime_like("2019/01/01")


@pytest.mark.xfail
def test_astropy_time_retains_input_format():
    # It would be nice to recover the input format,
    # but it's difficult without conditionally depending on Astropy
    expected_result = "2012-03-15T10:16:06.97400000000198Z"
    time = astropy.time.Time(expected_result)

    result = format_datetime_like(time)

    assert result == expected_result


def test_astropy_time_format():
    expected_result = "2012-03-15T10:16:06Z"
    time = astropy.time.Time("2012-03-15T10:16:06.97400000000198Z")

    result = format_datetime_like(time)

    assert result == expected_result