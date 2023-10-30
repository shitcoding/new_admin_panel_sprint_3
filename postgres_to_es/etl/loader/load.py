from clients.elk import ElasticsearchClient
from state.state import State
from utils.logger import logger


class FilmworkLoader:
    def __init__(
        self,
        state: State,
        elk_conn: ElasticsearchClient,
        elk_index: str,
        elk_chunk_size: int,
    ):
        self.state = state
        self.elk_conn = elk_conn
        self.elk_index = elk_index
        self.elk_chunk_size = elk_chunk_size

    def load_to_es(self):
        saved_state = None

        try:
            while True:
                last_modified, modified_rows = yield

                if not saved_state:
                    saved_state = last_modified
                elif saved_state != last_modified:
                    self.state.set_state(str(saved_state))
                    saved_state = last_modified

                logger.info(
                    'Received for loading to Elasticsearch {} Postgres rows modified after {}',
                    len(modified_rows),
                    saved_state,
                )

                data = [
                    {
                        '_id': row.id,
                        '_op_type': 'update',
                        'doc': {
                            'id': row.id,
                            'imdb_rating': row.rating,
                            'genre': row.genres_names,
                            'title': row.title,
                            'description': row.description,
                            'director': row.directors_names,
                            'actors_names': row.actors_names,
                            'writers_names': row.writers_names,
                            'actors': [dict(actor) for actor in row.actors],
                            'writers': [
                                dict(writer) for writer in row.writers
                            ],
                        },
                        'doc_as_upsert': True,
                    }
                    for row in modified_rows
                ]

                self.elk_conn.chunked_bulk(
                    actions=data,
                    chunk_size=self.elk_chunk_size,
                    index=self.elk_index,
                    raise_on_exception=True,
                )

        except GeneratorExit:
            logger.debug(
                'Loading of modified rows from Postgres to Elasticsearch finished'
            )
            if saved_state:
                self.state.set_state(str(saved_state))
