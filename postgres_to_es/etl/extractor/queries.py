GENRE_ENRICH_QUERY = """SELECT DISTINCT
                        fw.id, fw.modified
                    FROM
                        content.film_work fw
                    LEFT JOIN
                        content.genre_film_work gfw ON gfw.film_work_id = fw.id
                    WHERE
                        gfw.genre_id IN %s
                    ORDER BY
                        fw.modified;
                    """


PERSON_ENRICH_QUERY = """SELECT DISTINCT
                            fw.id, fw.modified
                        FROM
                            content.film_work fw
                        LEFT JOIN
                            content.person_film_work pfw ON pfw.film_work_id = fw.id
                        WHERE
                            pfw.person_id IN %s
                        ORDER BY
                            fw.modified;
                        """


MERGE_QUERY = """SELECT
                fw.id,
                fw.rating as rating,
                fw.title,
                fw.description,
                COALESCE (
                   json_agg(
                       DISTINCT jsonb_build_object(
                           'id', g.id,
                           'name', g.name
                       )
                   ) FILTER (WHERE g.id is not null),
                   '[]'
                ) as genres,
                COALESCE (
                   json_agg(
                       DISTINCT jsonb_build_object(
                           'id', p.id,
                           'name', p.full_name
                       )
                   ) FILTER (WHERE p.id is not null AND pfw.role = 'director'),
                   '[]'
                ) as directors,
                COALESCE (
                   json_agg(
                       DISTINCT jsonb_build_object(
                           'id', p.id,
                           'name', p.full_name
                       )
                   ) FILTER (WHERE p.id is not null AND pfw.role = 'actor'),
                   '[]'
                ) as actors,
                COALESCE (
                   json_agg(
                       DISTINCT jsonb_build_object(
                           'id', p.id,
                           'name', p.full_name
                       )
                   ) FILTER (WHERE p.id is not null AND pfw.role = 'writer'),
                   '[]'
                ) as writers
            FROM
                content.film_work fw
            LEFT JOIN
                content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN
                content.person p ON p.id = pfw.person_id
            LEFT JOIN
                content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN
                content.genre g ON g.id = gfw.genre_id
            WHERE
               fw.id IN %s
            GROUP BY
                fw.id;
            """
