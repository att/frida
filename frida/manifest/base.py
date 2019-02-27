""" Provides queries to Adapters as well as an interface to format the returned rows

Uses a "sealing" metaphor to prevent Manifests from being executed until every stated
binding has a value.
"""
import frida.database as fdb
import re

class Manifest:
    """
    Provide a query template and corresponding bindings that
    an Adapter can prepare and execute. Also provides a name-position map
    to format & return the result set as a dictionary (for use with JSON)
    """
    def __init__(self, name: str, tech_type: str, query_template: str, query_bindings: dict, return_format: dict):
        self.name = name
        self.tech_type = tech_type
        self.query_template = query_template
        self.query_bindings = query_bindings
        self.return_format = return_format

        self._sealed = False

    def seal(self) -> bool:
        """
        Seals a manifest, ensuring that every placeholder in the query_template
        has a corresponding binding. Adapters will only execute sealed manifests.
        Returns True or False, indicating the state of the seal.
        """
        # Empty lists are falsy, check first for minor optimization
        if self._sealed is False:
            if not self._get_unbound_bindings():
                self._sealed = True

        return self._sealed

    def _get_all_bindings(self) -> list:
        """
        Return a list of the binding placeholders in self.query_template
        """
        bindings = []
        matches = re.findall(r'{([a-zA-Z0-9]+)}', self.query_template)
        for match in matches:
            bindings.append(match)

        return bindings

    def _get_unbound_bindings(self) -> list:
        """
        Returns a list of the un-bound bindings in the query template.
        """
        bindings = self._get_all_bindings()
        if not bindings:
            unbound = []
        else:
            unbound = [key for key in bindings if key not in self.query_bindings]

        return unbound

    def add_bindings(self, **kwargs) -> None:
        """
        Adds query bindings to the Manifest - the bindings must be listed in
        the query template.
        """
        bindings = self._get_all_bindings()
        if not bindings:
            raise KeyError("No bindings in this Manifest")
        else:
            for key, value in kwargs.items():
                if key in bindings:
                    self.query_bindings[key] = value
                else:
                    raise KeyError("Binding {key} not found in Manifest query template".format(key=key))

    @property
    def tech_type(self):
        return self._tech_type

    @tech_type.setter
    def tech_type(self, tech_type):
        if tech_type not in fdb.DB_TECH_TYPES:
            raise ValueError("tech_type must be enumerated in frida.database.DB_TECH_TYPES.")
        self._tech_type = tech_type

    @tech_type.deleter
    def tech_type(self):
        del self._tech_type

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        self._name = value
        # Unseal manifest on changes
        self._sealed = False

    @name.deleter
    def name(self):
        del self._name

    @property
    def query_template(self) -> str:
        return self._query_template

    @query_template.setter
    def query_template(self, value):
        if not isinstance(value, str):
            raise TypeError("query_template must be a string")
        self._query_template = value
        # Unseal manifest on changes
        self._sealed = False

    @query_template.deleter
    def query(self):
        del self._query_template

    @property
    def query_bindings(self) -> str:
        return self._query_bindings

    @query_bindings.setter
    def query_bindings(self, value):
        if not isinstance(value, dict):
            raise TypeError("query_bindings must be a dict")
        self._query_bindings = value
        # Unseal manifest on changes
        self._sealed = False

    @query_bindings.deleter
    def query_bindings(self):
        del self._query_bindings

    @property
    def return_format(self) -> dict:
        return self._return_format

    @return_format.setter
    def return_format(self, value):
        if not isinstance(value, dict):
            raise TypeError("return_format must be a dict")
        self._return_format = value
        # Unseal manifest on changes
        self._sealed = False

    @return_format.deleter
    def return_format(self):
        del self._return_format
