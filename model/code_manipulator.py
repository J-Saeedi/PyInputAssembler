import re


class CodeManipulator:
    # codeAddress = None
    re_key = r"\s*(.+?)\s*=\s*\\?\s*.+#\s*\@\@(.+)\@\@"

    @classmethod
    def scan_variables(cls, codeAddress):
        if not codeAddress:
            raise FileNotFoundError
        with open(codeAddress) as f:
            code_text = str(f.read())
        result = re.findall(cls.re_key, code_text)
        # print(result)
        return result
