import json

from csvprofile import infer_type, profile
from csvprofile.cli import main

CSV = "id,name,score,note\n1,Ann,3.5,\n2,Bob,4,hi\n3,Ann,NA,hi\n"


def test_infer_type():
    assert infer_type(["1", "2"]) == "int"
    assert infer_type(["1", "2.5"]) == "float"
    assert infer_type(["1", "x"]) == "str"
    assert infer_type([]) == "empty"


def test_profile_columns(tmp_path):
    p = tmp_path / "d.csv"
    p.write_text(CSV)
    from csvprofile import read_csv

    rows, cols = read_csv(str(p))
    by = {r["column"]: r for r in profile(rows, cols)}
    assert by["id"]["type"] == "int" and by["id"]["max"] == 3
    assert by["name"]["distinct"] == 2 and by["name"]["type"] == "str"
    assert by["score"]["nulls"] == 1 and by["score"]["mean"] == 3.75
    assert by["note"]["nulls"] == 1


def test_cli_table_and_json(tmp_path, capsys):
    p = tmp_path / "d.csv"
    p.write_text(CSV)
    assert main([str(p)]) == 0
    assert "score" in capsys.readouterr().out
    assert main([str(p), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)[0]["column"] == "id"


def test_cli_missing_file(capsys):
    assert main(["/no/such/file.csv"]) == 2
    assert "error" in capsys.readouterr().err
