import copy
import unittest
from scripts.check_consumed_contracts import compare


class ConsumedContractsTests(unittest.TestCase):
    def setUp(self):
        self.document = {'paths': {'/used': {'get': {'responses': {'200': {'content': {
            'application/json': {'schema': {'$ref': '#/components/schemas/Result'}}}}}}}},
            'components': {'schemas': {'Result': {'type': 'object', 'required': ['state'],
                'properties': {'state': {'type': 'string', 'enum': ['OK', 'FAILED']},
                               'description': {'type': 'string'}}}}}}

    def test_unconsumed_paths_and_documentation_differences_are_ignored(self):
        producer = copy.deepcopy(self.document)
        producer['paths']['/unconsumed'] = {'delete': {'responses': {'204': {}}}}
        producer['components']['schemas']['Result']['description'] = 'Different annotation'
        self.assertEqual(compare(producer, self.document, ['/used']), (1, []))

    def test_types_required_enums_responses_and_named_description_field_are_checked(self):
        for mutation in ('type', 'required', 'enum', 'response', 'property'):
            producer = copy.deepcopy(self.document)
            schema = producer['components']['schemas']['Result']
            if mutation == 'type': schema['properties']['state']['type'] = 'integer'
            if mutation == 'required': schema['required'] = []
            if mutation == 'enum': schema['properties']['state']['enum'] = ['OK']
            if mutation == 'response': del producer['paths']['/used']['get']['responses']['200']
            if mutation == 'property': schema['properties']['description']['type'] = 'integer'
            with self.subTest(mutation=mutation):
                self.assertTrue(compare(producer, self.document, ['/used'])[1])

    def test_missing_consumed_operation_is_rejected(self):
        producer = copy.deepcopy(self.document)
        del producer['paths']['/used']['get']
        self.assertEqual(compare(producer, self.document, ['/used'])[1], ['GET /used'])
