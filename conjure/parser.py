# Copyright (c) 2015 Canonical Ltd.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" Parses build specifications and composes build out tasks
"""

import toml
import os
import copy


class ParserException(Exception):
    """ Error in Parser
    """
    pass


class Parser:
    def __init__(self, buildcfg):
        """ init

        Arguments:
        buildcfg: Path to TOML build configuration
        """
        self.buildcfg = buildcfg
        self.buildopts = None

    def __parse_config(self):
        """ Parse TOML

        Parses a TOML configuration to provide options to the build tasks
        """
        if not os.path.exists(self.buildcfg):
            raise ParserException("Unable to load build "
                                  "instructions from {}".format(self.buildcfg))
        with open(self.buildcfg, "r") as fp:
            self.buildopts = toml.loads(fp.read())

    def __validate_config_options(self):
        """ Pull acceptable editable config options from
        the editable key and validate any overrides
        """
        opts = copy.copy(self.buildopts['config'])
        editable_set = set(opts['editable'])

        del opts['editable']
        additional_set = set(opts.keys())
        if not additional_set.issubset(editable_set):
            raise ParserException("Options specified that are not "
                                  "defined in the config.editable list")
