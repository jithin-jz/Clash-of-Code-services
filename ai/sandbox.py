import logging
import asyncio
import ast
import tempfile
import os
import shutil
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Security: Block dangerous imports and builtins
BLOCKED_IMPORTS = {'os', 'sys', 'subprocess', 'shutil', 'importlib', 'socket', 'requests', 'urllib', 'http', 'ftplib'}
BLOCKED_BUILTINS = {'exec', 'eval', 'compile', 'open', 'input'}

class SecurityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.unsafe_found = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name.split('.')[0] in BLOCKED_IMPORTS:
                self.unsafe_found.append(f"Importing '{alias.name}' is not allowed.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module and node.module.split('.')[0] in BLOCKED_IMPORTS:
            self.unsafe_found.append(f"Importing from '{node.module}' is not allowed.")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in BLOCKED_BUILTINS:
                self.unsafe_found.append(f"Calling function '{node.func.id}' is not allowed.")
        self.generic_visit(node)

def is_safe_code(code: str) -> Dict[str, Any]:
    try:
        tree = ast.parse(code)
        analyzer = SecurityAnalyzer()
        analyzer.visit(tree)
        
        if analyzer.unsafe_found:
             return {"safe": False, "error": "; ".join(analyzer.unsafe_found)}
        return {"safe": True, "error": None}
    except SyntaxError as e:
        return {"safe": False, "error": f"Syntax Error: {e}"}

async def ensure_python_runtime() -> bool:
    # Always true for local execution
    return True

async def verify_challenge(user_code: str, test_code: str) -> Dict[str, Any]:
    """
    Executes user code against test code locally in a subprocess.
    """
    # 1. Security Check
    security_check = is_safe_code(user_code)
    if not security_check["safe"]:
        return {
            "passed": False,
            "output": "Security Violation: Unsafe Code Detected",
            "error": security_check["error"]
        }

    # 2. Combine code
    full_code = f"{user_code}\n\n{test_code}"
    
    # 3. Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp_file:
        tmp_file_path = tmp_file.name
        tmp_file.write(full_code)

    try:
        # 4. Execute in Subprocess
        # Run with a short timeout (e.g., 5 seconds)
        proc = await asyncio.create_subprocess_exec(
            "python", tmp_file_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=5.0)
            output = stdout.decode().strip() + "\n" + stderr.decode().strip()
            exit_code = proc.returncode

            if exit_code == 0:
                return {"passed": True, "output": output, "error": None}
            else:
                return {"passed": False, "output": output, "error": "Tests Failed"}

        except asyncio.TimeoutError:
            proc.kill()
            return {"passed": False, "output": "Execution Timed Out", "error": "Timeout (5s limit)"}
            
    except Exception as e:
        logger.error(f"Local sandbox execution error: {e}")
        return {"passed": False, "output": "", "error": str(e)}
    finally:
        # Cleanup
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
