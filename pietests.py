#!/usr/bin/env python
# -- coding: utf-8 --
# vim: fenc=utf-8:et:ts=4:sts=4:sw=4:fdm=marker

from datetime import datetime
from Domain.Table import Table
from Data.Data import Data, Row
from Domain.Graph import Linegram


def test_create_table():
    rows = [[3110002920, 'Árni', 'Dagur', True, datetime(2000, 10, 31)],
            [1506995079, 'Viktor', 'Máni', False, datetime.now()]]
    table = Table('test_list.txt', 
        ['Kennitala', 'First Name', 'Last name', 'Is awesome', 'DOB'],
        [int, str, str, bool, datetime]
    )
    return table

def test_add_and_get_row(): 
    table = test_create_table()

    row = Row([123, 'Emil Trausti', 'Smyrilsson', True, datetime.now()])
    table.add_row(row)
    assert table.get_row(-1) == row

def test_set_rows():
    table = test_create_table()
    rows = [[3110002920, 'Árni', 'Dagur', True, datetime(2000, 10, 31)],
            [1506995079, 'Viktor', 'Máni', False, datetime.now()]]

    table.set_rows(rows)

    assert table.get_rows() == rows

def test_linegram():
    # graph with parameters values = 4, 7.8, 3, 5.2, 1, 0.2, 9
    # and names_of_x  = 'Four', 'B', 'Ullarpeysa', 'Hundaæði', 'Age star', 'SMALL', '__--!'
    test_graph = """Name of grapph


   15│
   14│
   13│
   12│
   11│
   10│
    9│                                                                                                                                               ━━O
    8│                                                                                                                                             🡕🡕
    7│                                  ━━━━━━O🡖🡖🡖🡖🡖                                                                                             🡕🡕
    6│                           🡕🡕🡕🡕🡕🡕🡕            🡖🡖🡖🡖🡖                                                                                     🡕🡕🡕
    5│                    🡕🡕🡕🡕🡕🡕🡕                        🡖🡖🡖🡖🡖                ━━━━━━━━━━O🡖🡖🡖🡖🡖                                              🡕🡕
    4│                   O                                    ━━━━━ 🡕🡕🡕🡕🡕🡕🡕🡕🡕🡕                🡖🡖🡖🡖🡖                                       🡕🡕
    3│                                                             O                               🡖🡖🡖🡖🡖                               🡕🡕🡕
    2│                                                                                                  ━━━━━                        🡕🡕
    1│                                                                                                       O━━━━━━━━━━━━━━━━━━━━ 🡕🡕
    0│                                                                                                                            O
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
                      Four                    B           Ullarpeysa             Hundaæði             Age star                SMALL                __--!"""
    values = [4, 7.8, 3, 5.2, 1, 0.2, 9]
    names = ['Four', 'B', 'Ullarpeysa', 'Hundaæði', 'Age star', 'SMALL', '__--!']
    graph = Linegram(values=values, names_of_x=names)
    graph.update_table()
    assert str(graph) == test_graph

