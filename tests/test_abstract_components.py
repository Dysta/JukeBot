import unittest
from unittest.mock import AsyncMock, Mock

from jukebot.abstract_components import AbstractCollection, AbstractMap, AbstractRequest, AbstractService


class AbstractCollectionTest(unittest.TestCase):
    def test_empty_collection(self):
        collection = AbstractCollection(set=[])
        self.assertEqual(len(collection), 0)
        self.assertEqual(list(collection), [])
        self.assertNotIn("missing", collection)
        with self.assertRaises(IndexError):
            collection[0]

    def test_order_duplicates_and_indexing(self):
        collection = AbstractCollection(set=[3, 1, 3])
        self.assertEqual(len(collection), 3)
        self.assertEqual(list(collection), [3, 1, 3])
        self.assertEqual(collection[1], 1)
        self.assertEqual(collection[-1], 3)
        self.assertIn(3, collection)
        self.assertNotIn("3", collection)
        self.assertEqual(str(collection), "[3, 1, 3]")
        with self.assertRaises(IndexError):
            collection[3]

    def test_add_extends_left_collection_without_changing_right(self):
        left = AbstractCollection(set=[1, 2])
        right = AbstractCollection(set=[2, 3])
        self.assertIs(left + right, left)
        self.assertEqual(list(left), [1, 2, 2, 3])
        self.assertEqual(list(right), [2, 3])


class AbstractMapTest(unittest.TestCase):
    def test_mapping_operations(self):
        mapping = AbstractMap[str, int]()
        self.assertEqual(len(mapping), 0)
        mapping["first"] = 1
        mapping["second"] = 2
        mapping["first"] = 3
        self.assertEqual(mapping["first"], 3)
        self.assertEqual(len(mapping), 2)
        self.assertEqual(list(mapping), ["first", "second"])
        self.assertEqual(dict(mapping), {"first": 3, "second": 2})
        self.assertEqual(str(mapping), "{'first': 3, 'second': 2}")
        self.assertIn("first", mapping)
        self.assertNotIn(42, mapping)
        del mapping["first"]
        self.assertNotIn("first", mapping)

    def test_missing_keys(self):
        mapping = AbstractMap[str, int]()
        with self.assertRaises(KeyError):
            mapping["missing"]
        with self.assertRaises(KeyError):
            del mapping["missing"]
        self.assertIsNone(mapping.get("missing"))
        self.assertEqual(mapping.get("missing", 7), 7)
        self.assertEqual(len(mapping), 0)

    def test_inherited_mapping_methods(self):
        mapping = AbstractMap[str, int]()
        mapping.update({"first": 1, "second": 2})
        self.assertEqual(list(mapping.values()), [1, 2])
        self.assertEqual(list(mapping.items()), [("first", 1), ("second", 2)])
        self.assertEqual(mapping.setdefault("first", 99), 1)
        self.assertEqual(mapping.pop("second"), 2)
        mapping.clear()
        self.assertEqual(dict(mapping), {})

    def test_instances_are_independent_even_without_super_init(self):
        class NamedMap(AbstractMap[str, int]):
            def __init__(self, name):
                self.name = name

        first = NamedMap("first")
        second = NamedMap(name="second")
        self.assertEqual(first.name, "first")
        self.assertEqual(second.name, "second")
        first["key"] = 1
        self.assertNotIn("key", second)
        second["key"] = 2
        first.clear()
        self.assertEqual(second["key"], 2)

    def test_contains_does_not_trigger_lazy_getitem(self):
        class LazyMap(AbstractMap[str, int]):
            def __getitem__(self, k):
                if k not in self._collection:
                    self._collection[k] = 0
                return self._collection[k]

        mapping = LazyMap()
        self.assertNotIn("missing", mapping)
        self.assertEqual(len(mapping), 0)
        self.assertEqual(mapping["missing"], 0)
        self.assertIn("missing", mapping)


class StubRequest(AbstractRequest):
    async def setup(self):
        pass

    async def execute(self):
        self._result = "result"
        self._success = True

    async def terminate(self):
        pass


class AbstractRequestTest(unittest.IsolatedAsyncioTestCase):
    def test_base_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            AbstractRequest("query")

    async def test_lifecycle_and_public_state(self):
        request = StubRequest("query")
        request.setup = AsyncMock()
        request.terminate = AsyncMock()
        self.assertEqual(request.query, "query")
        self.assertIsNone(request.result)
        self.assertFalse(request.success)

        async with request as entered:
            self.assertIs(entered, request)
            request.setup.assert_awaited_once_with()
            request.terminate.assert_not_awaited()
            self.assertFalse(request.success)
            await request.execute()
            self.assertTrue(request.success)
            self.assertEqual(request.result, "result")

        request.terminate.assert_awaited_once_with()

    async def test_execution_failure_cleans_up_and_propagates(self):
        request = StubRequest("query")
        error = RuntimeError("execution failed")
        request.execute = AsyncMock(side_effect=error)
        request.terminate = AsyncMock()
        with self.assertRaises(RuntimeError) as caught:
            async with request:
                await request.execute()
        self.assertIs(caught.exception, error)
        request.terminate.assert_awaited_once_with()
        self.assertFalse(request.success)

    async def test_setup_failure_does_not_enter_context(self):
        request = StubRequest("query")
        request.setup = AsyncMock(side_effect=RuntimeError("setup failed"))
        request.terminate = AsyncMock()
        with self.assertRaisesRegex(RuntimeError, "setup failed"):
            async with request:
                self.fail("Context must not be entered after setup fails")
        request.terminate.assert_not_awaited()

    async def test_cleanup_failure_propagates(self):
        request = StubRequest("query")
        request.terminate = AsyncMock(side_effect=RuntimeError("cleanup failed"))
        with self.assertRaisesRegex(RuntimeError, "cleanup failed"):
            async with request:
                pass


class AbstractServiceTest(unittest.IsolatedAsyncioTestCase):
    async def test_base_call_requires_implementation(self):
        service = AbstractService(Mock())
        with self.assertRaises(NotImplementedError):
            await service()

    def test_context_preserves_service_and_bot(self):
        bot = Mock()
        service = AbstractService(bot)
        with service as entered:
            self.assertIs(entered, service)
            self.assertIs(entered.bot, bot)

    def test_context_does_not_suppress_errors(self):
        error = RuntimeError("service failed")
        with self.assertRaises(RuntimeError) as caught, AbstractService(Mock()):
            raise error
        self.assertIs(caught.exception, error)
