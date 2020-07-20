from typing import Dict, Callable


class VersionHolder:

    def __init__(self, serializer_name: str, version_readers: Dict[int, Callable]):
        self.__serializer_name = serializer_name
        self.__version_readers = version_readers

    def get_reader(self, version):
        if version in self.__version_readers:
            return self.__version_readers[version]
        else:
            raise Exception('Unsupported version of \'{0}\' serializer: {1}'.format(self.__serializer_name, version))
