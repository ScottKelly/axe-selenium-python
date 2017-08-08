# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest
from selenium import webdriver
# from axe_selenium_python import Axe

def report(rule):
    # return json.dumps(rule, indent=4, sort_keys=True)
    string = '\n\n\nRule Violated:\n' + rule['id'] + ' - ' + rule['description'] + \
        '\n\tURL: ' + rule['helpUrl'] + \
        '\n\tImpact Level: ' + rule['impact'] + \
        '\n\tTags:'
    for tag in rule['tags']:
        string += ' ' + tag
    string += '\n\tElements Affected:'
    i = 1
    for node in rule['nodes']:
        for target in node['target']:
            string += '\n\t' + str(i) + ') Target: ' + target
            i += 1
        for item in node['all']:
            string += '\n\t\t' + item['message']
        for item in node['any']:
            string += '\n\t\t' + item['message']
        for item in node['none']:
            string += '\n\t\t' + item['message']
    string += '\n\n\n'
    return string

def make_test_case(data, rule, docstring):
    def test_accessibility_rule(self):
        self.assertTrue(rule not in data['violations']), report(data['violations'][rule])
    clsdict = {
                'test_accessibility_rule': test_accessibility_rule,
                '__doc__': docstring
              }
    return type('ATest', (unittest.TestCase,), clsdict)


class TestFactory(unittest.TestCase):


    def test_execute(self, driver):
        axe = Axe(driver)
        rules = axe.get_rules()
        data = axe.execute()
        for rule in rules:
            make_test_case(data, rule['ruleId'], rule['description'])
        assertTrue(data is not None)

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get('http://mozillians.org')
    unittest.main(driver)
