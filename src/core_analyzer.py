import ast
import os
from typing import Dict, Set, Any, List

class AnalyzeError(Exception):
    pass

class CoreAnalyzer:
    """
    CoreAnalyzer promotes structural perception from a standalone script to a 
    formal organ of the reflective harness.
    """
    
    def __init__(self):
        self.io_patterns = {
            "open", "gzip.open", "bz2.open", "lzma.open",
            "csv.reader", "csv.writer", "csv.DictReader", "csv.DictWriter",
            "json.load", "json.dump", "json.loads", "json.dumps",
            "pickle.load", "pickle.dump", "pickle.loads", "pickle.dumps",
            "pandas.read_csv", "pandas.read_json", "pandas.read_excel",
            "pandas.read_parquet", "pandas.read_feather", "pandas.read_hdf",
            "pandas.read_sql", "pandas.read_html", "pandas.read_xml",
            "pandas.to_csv", "pandas.to_json", "pandas.to_excel",
            "pandas.to_parquet", "pandas.to_feather", "pandas.to_hdf",
            "pandas.to_sql", "pandas.to_html", "pandas.to_xml",
            "torch.load", "torch.save", "torch.load_state_dict", "torch.save_state_dict",
            "torch.utils.data.DataLoader",
            "numpy.load", "numpy.save", "numpy.loadtxt", "numpy.savetxt",
            "numpy.fromfile", "numpy.tofile", "numpy.genfromtxt",
            "Path.open", "Path.read_text", "Path.write_text",
            "Path.read_bytes", "Path.write_bytes", "Path.mkdir",
            "Path.rmdir", "Path.unlink", "Path.touch",
            "io.open", "io.StringIO", "io.BytesIO", "io.TextIOWrapper",
            "shutil.copy", "shutil.copy2", "shutil.copyfile",
            "shutil.copytree", "shutil.move", "shutil.rmtree",
            "zipfile.ZipFile", "zipfile.PyZipFile", "zipfile.open",
            "tarfile.open", "tarfile.TarFile",
            "sqlite3.connect", "sqlalchemy.create_engine",
            "requests.get", "requests.post", "requests.put", "requests.delete",
            "urllib.request.urlopen", "urllib.request.urlretrieve",
            "configparser.ConfigParser.read", "configparser.ConfigParser.write",
            "yaml.safe_load", "yaml.dump", "yaml.safe_dump",
            "toml.load", "toml.dump", "toml.loads", "toml.dumps",
            "PIL.Image.open", "PIL.Image.save", "cv2.imread", "cv2.imwrite",
            "librosa.load", "librosa.output.write_wav",
            "sklearn.model_selection.load_svmlight_file",
            "joblib.load", "joblib.dump",
            "h5py.File", "h5py.Group.create_dataset", "h5py.Dataset.read",
            "openpyxl.load_workbook", "openpyxl.Workbook.save",
            "xml.etree.ElementTree.parse", "xml.etree.ElementTree.write",
            "lxml.etree.parse", "lxml.etree.write",
            "PyPDF2.PdfReader", "PyPDF2.PdfWriter.write",
            "rarfile.RarFile", "rarfile.RarFile.extract",
            "boto3.client", "google.cloud.storage.Client",
            "azure.storage.blob.BlobServiceClient",
            "streamlit.file_uploader", "streamlit.download_button",
            "matplotlib.pyplot.savefig", "matplotlib.pyplot.imsave",
            "plotly.io.write_html", "plotly.io.write_image",
            "seaborn.savefig",
            "altair.save", "altair.renderer.save"
        }

    def analyze(self, file_path: str) -> Dict[str, Any]:
        """Performs surgical AST analysis and returns semantically tagged results."""
        imports: Dict[str, Set[str]] = {}
        alias_map: Dict[str, str] = {}
        io_call_count: int = 0
        function_usage: Dict[str, Set[str]] = {}
        io_operations: List[str] = []

        if not os.path.exists(file_path):
            raise AnalyzeError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        if not source.strip():
            return {"file_info": {"empty": True, "path": file_path}, "imports": {}, "io_call_count": 0}

        tree = ast.parse(source, filename=file_path)

        def _record_import(module, stmt):
            imports.setdefault(module, set()).add(stmt)
            function_usage.setdefault(module, set())

        def _record_function_usage(module, func_name):
            function_usage.setdefault(module, set()).add(func_name)
            if any(p in f"{module}.{func_name}" for p in self.io_patterns):
                nonlocal io_call_count
                io_call_count += 1
                io_operations.append(f"{module}.{func_name}")

        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    real_mod = alias.name
                    _record_import(real_mod, f"import {real_mod}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    real_name = alias.name
                    _record_import(module or "<local>", f"from {module} import {real_name}")
                    _record_function_usage(module or "<local>", real_name)
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                # Basic scan for IO function calls
                func = node.value.func
                if isinstance(func, ast.Attribute):
                    full_name = f"{getattr(func.value, 'id', 'obj')}.{func.attr}"
                    _record_function_usage("local", full_name)
        
        # Result categorization
        category = "compute_bound"
        if io_call_count > 0:
            category = "io_heavy"
        
        return {
            "imports": {k: list(v) for k, v in imports.items()},
            "io_call_count": io_call_count,
            "function_usage": {k: list(v) for k, v in function_usage.items()},
            "io_operations": io_operations,
            "file_info": {"path": file_path, "size": len(source), "category": category}
        }
