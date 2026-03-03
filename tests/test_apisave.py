def test_add_aeroplane(temp_saver, sample_plane):
    temp_saver.add_aeroplane(sample_plane)
    data = temp_saver._read_file()

    assert len(data) == 1
    assert data[0]["callsign"] == "AFR123"


def test_get_aeroplane(temp_saver, sample_plane):
    temp_saver.add_aeroplane(sample_plane)

    results = temp_saver.get_aeroplane({"origin_country": "France"})
    assert len(results) == 1

    empty_results = temp_saver.get_aeroplane({"origin_country": "USA"})
    assert len(empty_results) == 0


def test_delete_aeroplane(temp_saver, sample_plane):
    temp_saver.add_aeroplane(sample_plane)
    temp_saver.delete_aeroplane(sample_plane)

    data = temp_saver._read_file()
    assert len(data) == 0
