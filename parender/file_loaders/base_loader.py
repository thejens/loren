class BaseLoader(object):

    @staticmethod
    def load(file_path, root_path, **kwargs) -> str:
        raise NotImplementedError()
