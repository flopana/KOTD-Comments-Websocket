import sqlite3 as sqlite

conn = sqlite.connect('kotd.db')
cursor = conn.cursor()

cursor.execute("""
    create table if not exists comments (
        id integer primary key,
        comment_id text,
        body text,
        author text,
        link_id text,
        author_flair_text text,
        author_flair_css_class text,
        permalink text,
        parent_id text,
        created_utc integer
    )
""")
conn.commit()
