import asyncio
from unittest import TestCase

import asyncpg

from ..base import DBTestCase
from ..example_project.tables import Pokemon


class TestSelect(DBTestCase):

    def test_query_all_columns(self):
        self.insert_row()

        async def get_pokemon():
            return await Pokemon.select().execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertDictEqual(
            response[0],
            {'name': 'pikachu', 'trainer': 'ash', 'power': 1000}
        )

    def test_query_some_columns(self):
        self.insert_row()

        async def get_pokemon():
            return await Pokemon.select('name').execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertDictEqual(
            response[0],
            {'name': 'pikachu'}
        )

    def test_where_like(self):
        self.insert_rows()

        async def get_pokemon():
            return await Pokemon.select(
                'name'
            ).where(
                Pokemon.name.like('%chu')
            ).execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'pikachu'}, {'name': 'raichu'}]
        )

    def test_where_greater_than(self):
        self.insert_rows()

        async def get_pokemon():
            return await Pokemon.select(
                'name'
            ).where(
                Pokemon.power > 1000
            ).execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'raichu'}]
        )

    def test_where_greater_equal_than(self):
        self.insert_rows()

        async def get_pokemon():
            return await Pokemon.select(
                'name'
            ).where(
                Pokemon.power >= 1000
            ).execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'pikachu'}, {'name': 'raichu'}]
        )

    def test_where_less_than(self):
        self.insert_rows()

        async def get_pokemon():
            return await Pokemon.select(
                'name'
            ).where(
                Pokemon.power < 1000
            ).execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'weedle'}]
        )

    def test_where_less_equal_than(self):
        self.insert_rows()

        async def get_pokemon():
            return await Pokemon.select(
                'name'
            ).where(
                Pokemon.power <= 1000
            ).execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'pikachu'}, {'name': 'weedle'}]
        )

    def test_where_and(self):
        self.insert_rows()

        async def get_pokemon():
            return await Pokemon.select(
                'name'
            ).where(
                (Pokemon.power <= 1000) & (Pokemon.name.like('%chu'))
            ).execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'pikachu'}]
        )

    def test_where_or(self):
        self.insert_rows()

        async def get_pokemon():
            return await Pokemon.select(
                'name'
            ).where(
                (Pokemon.name == 'raichu') | (Pokemon.name == 'weedle')
            ).execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'raichu'}, {'name': 'weedle'}]
        )

    def test_multiple_where(self):
        """
        Test that chaining multiple where clauses works results in an AND.
        """
        self.insert_rows()

        query = Pokemon.select(
            'name'
        ).where(
            Pokemon.name == 'raichu'
        ).where(
            Pokemon.trainer == 'sally'
        )

        async def get_pokemon():
            return await query.execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'raichu'}]
        )
        self.assertTrue(
            'AND' in query.__str__()
        )

    def test_complex_where(self):
        """
        Test a complex where clause - combining AND, and OR.
        """
        self.insert_rows()

        async def get_pokemon():
            return await Pokemon.select(
                'name'
            ).where(
                ((Pokemon.power == 2000) & (Pokemon.trainer == 'sally')) |
                ((Pokemon.power == 10) & (Pokemon.trainer == 'gordon'))
            ).execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'raichu'}, {'name': 'weedle'}]
        )

    def test_limit(self):
        self.insert_rows()

        async def get_pokemon():
            return await Pokemon.select(
                'name'
            ).limit(
                1
            ).execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'pikachu'}]
        )

    def test_order_by_ascending(self):
        self.insert_rows()

        async def get_pokemon():
            return await Pokemon.select(
                'name'
            ).order_by(
                'name'
            ).limit(1).execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'pikachu'}]
        )

    def test_order_by_decending(self):
        self.insert_rows()

        async def get_pokemon():
            return await Pokemon.select(
                'name'
            ).order_by(
                '-name'
            ).limit(1).execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'weedle'}]
        )

    def test_count(self):
        self.insert_rows()

        async def get_pokemon():
            return await Pokemon.select().where(
                Pokemon.name == 'pikachu'
            ).count().execute()

        response = asyncio.run(get_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'count': 1}]
        )


class TestUpdate(DBTestCase):

    def test_update(self):
        self.insert_rows()

        async def update_pokemon():
            return await Pokemon.update(
                name='kakuna'
            ).where(
                Pokemon.name == 'weedle'
            ).execute()

        async def check_pokemon():
            return await Pokemon.select(
                'name'
            ).where(
                Pokemon.name == 'kakuna'
            ).execute()

        asyncio.run(update_pokemon())
        response = asyncio.run(check_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'name': 'kakuna'}]
        )


class TestDelete(DBTestCase):

    def test_delete(self):
        self.insert_rows()

        async def delete_pokemon():
            return await Pokemon.delete().where(
                Pokemon.name == 'weedle'
            ).execute()

        async def check_pokemon():
            return await Pokemon.select().where(
                Pokemon.name == 'weedle'
            ).count().execute()

        asyncio.run(delete_pokemon())
        response = asyncio.run(check_pokemon())
        print(f'response = {response}')

        self.assertEqual(
            response,
            [{'count': 0}]
        )


class TestCreate(DBTestCase):

    def setUp(self):
        """
        Need to override, otherwise table will be auto created.
        """
        pass

    def test_create_table(self):
        async def create_table():
            return await Pokemon.create().execute()

        async def count_rows():
            return await Pokemon.select(
                'name', 'trainer', 'power'
            ).count().execute()

        asyncio.run(create_table())

        # Just do a count to make sure the table was created ok.
        response = asyncio.run(count_rows())
        self.assertEqual(response[0]['count'], 0)


class TestMetaClass(TestCase):

    def test_tablename(self):
        self.assertEqual(Pokemon.Meta.tablename, 'pokemon')