import logging
from typing import Dict, Any, Optional
import requests
from config import settings

logger = logging.getLogger(__name__)

PISTON_URL = settings.PISTON_URL

def ensure_python_runtime() -> bool:
    """
    Checks if Python 3.10 is installed in Piston, and installs it if missing.
    """
    try:
        # Check available runtimes
        resp = requests.get(f"{PISTON_URL}/api/v2/runtimes")
        if resp.status_code != 200:
            logger.error(f"Piston unavailable: {resp.status_code}")
            return False
            
        runtimes = resp.json()
        for r in runtimes:
            if r["language"] == "python" and "3.10" in r["version"]:
                return True
        
        # Install if missing
        logger.info("Installing Python 3.10 runtime in Piston...")
        install_resp = requests.post(f"{PISTON_URL}/api/v2/packages", json={
            "language": "python",
            "version": "3.10.0"
        })
        if install_resp.status_code == 200:
            logger.info("Python runtime installed successfully.")
            return True
        else:
            logger.error(f"Failed to install runtime: {install_resp.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error checking Piston runtime: {e}")
        return False

def verify_challenge(user_code: str, test_code: str) -> Dict[str, Any]:
    """
    Executes user code against test code safely using Piston.
    
    Args:
        user_code: The student's code.
        test_code: The test assertions.
        
    Returns:
        Dict: {"passed": bool, "output": str, "error": str}
    """
    # 1. Combine code and tests
    full_code = f"{user_code}\n\n{test_code}"
    
    # 2. Check/Ensure Runtime
    if not ensure_python_runtime():
         return {
            "passed": False, 
            "output": "Execution Environment Unavailable", 
            "error": "Sandbox not ready"
        }

    # 3. Execute via Piston API
    payload = {
        "language": "python",
        "version": "3.10.0",
        "files": [
            {
                "name": "challenge.py",
                "content": full_code
            }
        ],
        "stdin": "",
        "args": [],
        "compile_timeout": 10000,
        "run_timeout": 5000,
        "memory_limit": 128 * 1024 * 1024,
    }

    try:
        response = requests.post(f"{PISTON_URL}/api/v2/execute", json=payload, timeout=10)
        result = response.json()
        
        run_stage = result.get("run", {})
        stdout = run_stage.get("stdout", "")
        stderr = run_stage.get("stderr", "")
        output = stdout + stderr

        if response.status_code != 200:
             return {"passed": False, "output": output, "error": f"Piston Error {response.status_code}"}

        # If exit code is 0, tests passed (assuming normal unittest/assert behavior)
        exit_code = run_stage.get("run", {}).get("code", 0) if "run" in result else 1
        # Re-check run_stage keys, usually 'code' is directly in run_stage
        exit_code = run_stage.get("code", 0)

        if exit_code == 0:
            return {"passed": True, "output": output, "error": None}
        else:
             return {"passed": False, "output": output, "error": "Tests Failed"}
             
    except Exception as e:
        logger.error(f"Sandbox execution error: {e}")
        return {"passed": False, "output": "", "error": str(e)}
