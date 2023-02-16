

def init_data_base(DATA_BASE):

    cursor = DATA_BASE.cursor()
    cursor.execute("DROP TABLE IF EXISTS roles_ref;")
    cursor.execute("DROP TABLE IF EXISTS supplies_types_ref;")
    cursor.execute("""
                    CREATE TABLE roles_ref(
                        name TEXT PRIMARY KEY NOT NULL,
                        level_permission INT NOT NULL
                    );""")
    cursor.execute("""
                    INSERT INTO roles_ref (name, level_permission)
                    VALUES ('administrator', 0);""")
    cursor.execute("""
                    INSERT INTO roles_ref (name, level_permission)
                    VALUES ('classic', 1);""")
    cursor.execute("""
                    CREATE TABLE supplies_types_ref(
                        name TEXT PRIMARY KEY NOT NULL
                    );""")
    cursor.execute("""
                    INSERT INTO supplies_types_ref (name)
                    VALUES ("drink");""")
    cursor.execute("""
                    INSERT INTO supplies_types_ref (name)
                    VALUES ("food");""")
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user(
                        id INT NOT NULL PRIMARY KEY,
                        role TEXT NOT NULL DEFAULT "classic",
                        money REAL NOT NULL DEFAULT 0,
                        status INT NOT NULL DEFAULT 0,
                        FOREIGN KEY (role) REFERENCES roles_ref(name)
                    );""")
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS supply(
                        name TEXT PRIMARY KEY NOT NULL,
                        type TEXT NOT NULL,
                        price INT NOT NULL,
                        effect TEXT,
                        FOREIGN KEY (type) REFERENCES supplies_types_ref(name),
                        FOREIGN KEY (effect) REFERENCES effect(name)
                    );""")
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS effect(
                        name TEXT PRIMARY KEY NOT NULL,
                        desciption TEXT NOT NULL DEFAULT "No description."
                    );""")
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_inventory(
                        id INT NOT NULL,
                        content TEXT NOT NULL,
                        quantity INT NOT NULL DEFAULT 1,
                        FOREIGN KEY (id) REFERENCES user(id),
                        FOREIGN KEY (content) REFERENCES supply(name)
                    );""")
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS distributor(
                        id INT PRIMARY KEY NOT NULL,
                        FOREIGN KEY (id) REFERENCES user(id)
                    );""")
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS distributor_inventory(
                        id INT NOT NULL,
                        content TEXT NOT NULL,
                        quantity INT NOT NULL DEFAULT 1,
                        FOREIGN KEY (id) REFERENCES distributor(id),
                        FOREIGN KEY (content) REFERENCES supply(name)
                    );""")
    DATA_BASE.commit()
