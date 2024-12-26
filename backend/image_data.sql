CREATE TABLE IF NOT EXISTS image_data (
    id TEXT NOT NULL PRIMARY KEY,
    owner TEXT,
    ownername TEXT,
    title TEXT,
    ispublic INTEGER,
    license TEXT,
    description TEXT,
    url_m TEXT,
    url_m_cdn TEXT,
    height_m TEXT,
    width_m TEXT,
    url_sq TEXT,
    url_sq_cdn TEXT,
    height_sq TEXT,
    width_sq TEXT
);
