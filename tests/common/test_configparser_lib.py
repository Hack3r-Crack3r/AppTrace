import os
import unittest
from unittest.mock import patch
from configparser import NoOptionError
from common.configparser_lib import ConfigReader


class TestConfigReader(unittest.TestCase):

    def setUp(self):
        # Create a temporary config file for testing
        self.config_file = "test_config.ini"
        with open(self.config_file, "w") as f:
            f.write("[test]\n")
            f.write("foo = bar\n")
            f.write("baz = qux\n")

    def tearDown(self):
        # Remove the temporary config file
        os.remove(self.config_file)

    @patch("os.path.exists")
    @patch("configparser.ConfigParser.get")
    def test_getconfig(self, mock_get, mock_exists):
        # Mock the config file path to use the test config file
        mock_exists.return_value = True

        # Mock the ConfigParser.get method to read from the test config file
        def mock_configparser_get(section, setting):
            if section == "test":
                if setting == "foo":
                    return "bar"
                elif setting == "baz":
                    return "qux"
            raise NoOptionError(setting, section)
        mock_get.side_effect = mock_configparser_get

        # Test that getconfig() returns the correct value for an existing key
        val = ConfigReader.getconfig("test", "foo")
        self.assertEqual(val, "bar")

    @patch("os.path.exists")
    @patch("configparser.ConfigParser.get")
    def test_getconfig_default(self, mock_get, mock_exists):
        # Mock the config file path to use the test config file
        mock_exists.return_value = True

        # Mock the ConfigParser.get method to raise a NoOptionError for the nonexistent key
        mock_get.side_effect = NoOptionError("nonexistent", "test")

        # Test that getconfig() returns the default value for a non-existent key
        val = ConfigReader.getconfig("test", "nonexistent", "default")
        self.assertEqual(val, "default")

    @patch("os.path.exists")
    @patch("configparser.ConfigParser.get")
    def test_getconfig_section_default(self, mock_get, mock_exists):
        # Mock the config file path to use the test config file
        mock_exists.return_value = True

        # Mock the ConfigParser.get method to raise a NoOptionError for the nonexistent section
        mock_get.side_effect = NoOptionError("nonexistent", "nonexistent")

        # Test that getconfig() returns the default value for a non-existent section
        val = ConfigReader.getconfig("nonexistent", "nonexistent", "default")
        self.assertEqual(val, "default")

    @patch("os.path.exists")
    def test_getconfig_no_file(self, mock_exists):
        # Mock the config file path to not exist
        mock_exists.return_value = False

        # Test that getconfig() raises an exception when the config file does not exist
        with self.assertRaises(Exception):
            ConfigReader.getconfig("test", "foo")

    @patch("os.path.exists")
    def test_getconfig_no_option(self, mock_exists):
        # Mock the config file path to use the test config file
        mock_exists.return_value = True
