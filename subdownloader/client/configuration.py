# -*- coding: utf-8 -*-
# Copyright (c) 2019 SubDownloader Developers - See COPYING - GPLv3

import configparser
from enum import Enum
import logging
from pathlib import Path

from subdownloader.languages.language import Language

log = logging.getLogger('subdownloader.client.configuration')


class SettingsError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class KeepCaseConfigParser(configparser.ConfigParser):
    def optionxform(self, option):
        return option


class Settings(object):
    def __init__(self, path):
        self._cfg = KeepCaseConfigParser()
        self._path = path
        self._dirty = False

    def get_path_store(self):
        return self._path

    def set_path_store(self, path):
        if self._path.resolve() == path.resolve():
            return
        self._path = path
        self.reload()

    def _key_to_section_option(self, key):
        try:
            section, option = key.split('.', 1)
        except ValueError:
            raise KeyError(key)
        return section, option

    def _load_str(self, section_path):
        if isinstance(section_path, Enum):
            raise RuntimeError('Settings key should not be an enum. Did you forget ".value"?')
        try:
            section, option = section_path
        except TypeError:
            raise KeyError(section_path)
        try:
            return self._cfg.get(section, option)
        except (configparser.NoOptionError, configparser.NoSectionError):
            raise KeyError(section, option)

    def remove_key(self, section_path):
        try:
            return self._cfg.remove_option(*section_path)
        except (configparser.NoOptionError, configparser.NoSectionError, TypeError):
            pass

    def get_str(self, section_path, default):
        try:
            return self._load_str(section_path)
        except KeyError:
            return default

    def set_str(self, section_path, value):
        try:
            section, option = section_path
        except ValueError:
            raise KeyError(section_path)
        try:
            self._cfg.add_section(section)
        except configparser.DuplicateSectionError:
            pass
        self._cfg.set(section, option, value)
        self._dirty = True

    def get_language(self, key, default=None):
        # FIXME: test parsing language settings (+invalid)
        try:
            xxx = self._load_str(key)
            return Language.from_xxx(xxx)
        except KeyError:
            return default

    def set_language(self, key, lang):
        if lang is None:
            lang_str = ''
        else:
            lang_str = lang.xxx()
        self.set_str(key, lang_str)

    def get_languages(self, key, default=None):
        try:
            xxxs = self._load_str(key)
            return [Language.from_xxx(lang_str) for lang_str in xxxs.split(',') if lang_str]
        except KeyError:
            return default

    def set_languages(self, section_path, langs):
        self.set_str(section_path, ','.join(l.xxx() for l in langs))

    def get_int(self, key, default=None):
        # FIXME: test parsing ints settings (+invalid)
        try:
            return int(self._load_str(key))
        except KeyError:
            return default

    def set_int(self, key, value):
        self.set_str(key, str(value))

    def get_ints(self, key, default=None):
        # FIXME: test parsing ints settings (+invalid)
        try:
            return list(int(v) for v in self._load_str(key).split(','))
        except KeyError:
            return default

    def set_ints(self, key, values):
        self.set_str(key, ','.join(str(v) for v in values))

    def get_bool(self, key, default=None):
        # FIXME: test parsing bool settings (+invalid)
        try:
            text = self._load_str(key).lower()
            if text in ('0', 'false', 'no', ):
                return False
            elif text in ('1', 'true', 'yes', ):
                return True
            else:
                raise ValueError(text)
        except KeyError:
            return default

    def set_bool(self, key, value):
        self.set_str(key, '1' if value else '0')

    def get_path(self, section_path, default=Path()):
        try:
            return Path(self._load_str(section_path))
        except KeyError:
            return default

    def set_path(self, key, value):
        self.set_str(key, str(value))

    def get_list(self, key, default=None):
        base_key = '{}.{}'.format(*key)
        size_path = (base_key, 'size', )
        size = self.get_int(size_path, None)
        if size is None:
            return default
        result = list()
        for elem_i_index in range(size):
            elem_i_path = (base_key, str(elem_i_index), )
            elem_i = self.get_str(elem_i_path, None)
            if elem_i is None:
                return default
            result.append(elem_i)
        return result

    def set_list(self, key, value):
        base_key = '{}.{}'.format(*key)
        size_path = (base_key, 'size', )
        self.set_int(size_path, len(value))
        for elem_i_index, elem_i in enumerate(value):
            elem_i_path = (base_key, str(elem_i_index), )
            self.set_str(elem_i_path, str(elem_i))

    def clear(self):
        self._cfg.clear()

    def reload(self):
        self.clear()
        log.debug('Reading settings from {} ...'.format(self._path))
        if not self._path.exists():
            log.debug('... settings file does not exists. Skip read.')
        else:
            result = self._cfg.read(str(self._path))
            log.debug('... reading finished')
            if not result:
                raise SettingsError('Failed to read {}'.format(self._path))

        self._dirty = False

    def write(self):
        try:
            log.debug('Writing settings to {} ...'.format(self._path))
            with open(str(self._path), 'w') as f:
                self._cfg.write(f)
            log.debug('... writing finished')
        except PermissionError:
            log.warning('... Writing failed. No permission.')
        self._dirty = False
