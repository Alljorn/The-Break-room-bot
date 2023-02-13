# -*- coding: utf-8 -*-


def init_data_base(DATA_BASE):
    cur = DATA_BASE.cursor()
    """
    cur.execute("CREATE TABLE distributor(id, content)")
    cur.execute("CREATE TABLE distributor_inventory(id, content, quantity)")
    cur.execute("CREATE TABLE roles_ref(id, level_permission, name)")
    cur.execute("CREATE TABLE supply(name, type_name, price, effect_name)")
    cur.execute("CREATE TABLE supplies_types_ref(id, name)")
    cur.execute("CREATE TABLE user(id, content, money, role)")
    cur.execute("CREATE TABLE user_inventory(id, content, quantity)")
    """
    print("Vérification de la Database...")
    res = cur.execute("SELECT name FROM sqlite_master")
    for i in res.fetchall():
        print(i)
    table = ["distributor", "user"]
    for i in table:
        res = cur.execute(f"SELECT * FROM {i}")
        for i in res.fetchall():
            print(i)
    print()
