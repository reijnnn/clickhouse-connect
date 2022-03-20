from uuid import UUID

from tests.helpers import to_bytes
from clickhouse_connect.driver.native import parse_response


uint16_nulls = ("0104 0969 6e74 5f76 616c 7565 104e 756c"
                "6c61 626c 6528 5549 6e74 3136 2901 0001"
                "0000 0014 0000 0028 00")

low_cardinality = ("0102 026c 6316 4c6f 7743 6172 6469 6e61"
                   "6c69 7479 2853 7472 696e 6729 0100 0000"
                   "0000 0000 0006 0000 0000 0000 0300 0000"
                   "0000 0000 0004 4344 4d41 0347 534d 0200"
                   "0000 0000 0000 0102 0101 026c 6316 4c6f"
                   "7743 6172 6469 6e61 6c69 7479 2853 7472"
                   "696e 6729 0100 0000 0000 0000 0006 0000"
                   "0000 0000 0200 0000 0000 0000 0004 554d"
                   "5453 0100 0000 0000 0000 01")

low_card_array = ("0102 066c 6162 656c 731d 4172 7261 7928"
                  "4c6f 7743 6172 6469 6e61 6c69 7479 2853"
                  "7472 696e 6729 2901 0000 0000 0000 0000"
                  "0000 0000 0000 0000 0000 0000 0000 00")

simple_map = ("0101 066e 6e5f 6d61 7013 4d61 7028 5374"
              "7269 6e67 2c20 5374 7269 6e67 2902 0000"
              "0000 0000 0004 6b65 7931 046b 6579 3206"
              "7661 6c75 6531 0676 616c 7565 32")

low_card_map = ("0102 086d 6170 5f6e 756c 6c2b 4d61 7028"
                "4c6f 7743 6172 6469 6e61 6c69 7479 2853"
                "7472 696e 6729 2c20 4e75 6c6c 6162 6c65"
                "2855 5549 4429 2901 0000 0000 0000 0002"
                "0000 0000 0000 0004 0000 0000 0000 0000"
                "0600 0000 0000 0003 0000 0000 0000 0000"
                "0469 676f 7206 6765 6f72 6765 0400 0000"
                "0000 0000 0102 0102 0100 0000 0000 0000"
                "0000 0000 0000 0000 0000 0000 235f 7dc5"
                "799f 431d a9e1 93ca ccff c652 235f 7dc5"
                "799f 437f a9e1 93ca ccff 0052 235f 7dc5"
                "799f 431d a9e1 93ca ccff c652")


def check_result(result, expected, row_num=0, col_num=0):
    result_set = result[0]
    row = result_set[row_num]
    value = row[col_num]
    assert value == expected


def test_uint16_nulls():
    result = parse_response(to_bytes(uint16_nulls))
    assert result[0] == ((None,), (20,), (None,), (40,))


def test_low_cardinality():
    result = parse_response(to_bytes(low_cardinality))
    assert result[0] == (('CDMA',), ('GSM',), ('UMTS',))


def test_low_card_array():
    result = parse_response(to_bytes(low_card_array))
    assert result[0][0] == ((),), ((),)


def test_map():
    result = parse_response(to_bytes(simple_map))
    check_result(result, {'key1': 'value1', 'key2': 'value2'})
    result = parse_response(to_bytes(low_card_map))
    check_result(result, {'george': UUID('1d439f79-c57d-5f23-52c6-ffccca93e1a9'), 'igor': None})
