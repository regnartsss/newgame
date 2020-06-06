from sql import sql_insertscript_no_await

table_resource = """CREATE TABLE resource (
    user_id       INT  DEFAULT (0),
    wood          INT  DEFAULT (0),
    stone         INT  DEFAULT (0),
    iron          INT  DEFAULT (0),
    food          INT  DEFAULT (0),
    gold          INT  DEFAULT (0),
    diamond       INT  DEFAULT (0),
    resource      TEXT DEFAULT (NULL),
    lvl           INT  DEFAULT (0),
    number        INT  DEFAULT (0),
    cell          INT  DEFAULT (0),
    timer         TEXT,
    production    INT  DEFAULT (0),
    farm_timer    TEXT DEFAULT (NULL),
    time_start    TEXT DEFAULT (NULL),
    time_stop     TEXT DEFAULT (NULL),
    mining_start  INT  DEFAULT (0),
    field         TEXT DEFAULT (NULL),
    number_attack INT  DEFAULT (0)
)

"""
sql_insertscript_no_await(table_resource)