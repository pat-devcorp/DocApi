class CustomDict:
    @staticmethod
    def has_only_primitive_types(dictionary):
        primitive_types = (int, float, str, bool)

        for value in dictionary.values():
            if not isinstance(value, primitive_types):
                return False

        return True
