-- Create schema
CREATE SCHEMA IF NOT EXISTS content;

-- Create ENUM type for filmwork type
create type film_type as ENUM ('movie', 'tv_show');

-- Create ENUM type for person's role in the filmwork
create type role_type as ENUM (
  'actor',
  'director',
  'writer',
  'producer',
  'composer',
  'cinematographer',
  'editor'
);

-- Create film_work table
-- (Stores individual film works, such as movies or TV shows)
CREATE TABLE IF NOT EXISTS content.film_work (
  id uuid PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  creation_date DATE,
  rating FLOAT,
  type film_type NOT NULL,
  created timestamp with time zone NOT NULL,
  modified timestamp with time zone NOT NULL
);

-- Index for searching by creation_date
CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date);

-- Create genre table
-- (Stores genres that a film work can belong to)
CREATE TABLE IF NOT EXISTS content.genre (
  id uuid PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  created timestamp with time zone NOT NULL,
  modified timestamp with time zone NOT NULL
);

-- Create genre_film_work table
-- (A junction table for many-to-many relationship between films and genres)
CREATE TABLE IF NOT EXISTS content.genre_film_work (
  id uuid PRIMARY KEY,
  genre_id uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
  film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
  created timestamp with time zone NOT NULL
);

-- Unique index: a genre can't be associated multiple times with the same film
CREATE UNIQUE INDEX genre_film_work_unique_idx ON content.genre_film_work (genre_id, film_work_id);

-- Create person table
-- (Stores persons involved in film making)
CREATE TABLE IF NOT EXISTS content.person (
  id uuid PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  created timestamp with time zone NOT NULL,
  modified timestamp with time zone NOT NULL
);

-- Create person_film_work table
-- (A junction table for many-to-many relationship between films and persons)
CREATE TABLE IF NOT EXISTS content.person_film_work (
  id uuid PRIMARY KEY,
  person_id uuid NOT NULL REFERENCES content.person (id) ON DELETE CASCADE,
  film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
  role role_type NOT NULL,
  created timestamp with time zone NOT NULL
);

-- Unique index: a person can't be added multiple times to the same film in the same role
CREATE UNIQUE INDEX film_work_person_role_idx ON content.person_film_work (film_work_id, person_id, role);
