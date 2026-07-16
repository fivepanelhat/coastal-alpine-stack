"""
conftest.py - Root Pytest configuration for Coastal Alpine Stack monorepo.

Dynamically manages sys.path and sys.modules cache to prevent namespace
conflicts between Blue-Moon-Portal and AquaGuard-Portal during test execution.
"""

import os
import sys
import importlib

_portal_module_caches = {"Blue-Moon-Portal": {}, "AquaGuard-Portal": {}}
_active_portal = None


def pytest_collect_file(file_path, parent):
    """
    Hook run by pytest before collecting a test file.
    """
    _route_context(str(file_path))


def pytest_runtest_setup(item):
    """
    Hook run by pytest before executing a test.
    """
    _route_context(str(item.fspath))


def _route_context(path_str: str):
    path_lower = path_str.lower()
    if "blue-moon" in path_lower or "blue_moon" in path_lower:
        _setup_portal_context("Blue-Moon-Portal")
    elif "aquaguard" in path_lower:
        _setup_portal_context("AquaGuard-Portal")
    else:
        _clear_portal_context()


def _setup_portal_context(portal_name: str):
    global _active_portal
    if _active_portal == portal_name:
        return

    stack_root = os.path.dirname(os.path.abspath(__file__))

    # 1. Save current active portal's modules
    if _active_portal is not None:
        saved_cache = _portal_module_caches[_active_portal]
        saved_cache.clear()
        for mod_name in list(sys.modules.keys()):
            if (
                mod_name.startswith("portal_schemas")
                or mod_name.startswith("portal_core")
                or mod_name.startswith("tests")
            ):
                saved_cache[mod_name] = sys.modules[mod_name]
                del sys.modules[mod_name]

    # 2. Update sys.path
    sys.path = [
        p
        for p in sys.path
        if "Blue-Moon-Portal" not in p and "AquaGuard-Portal" not in p
    ]
    target_dir = os.path.join(stack_root, portal_name)
    sys.path.insert(0, target_dir)

    # 3. Restore target portal's modules
    target_cache = _portal_module_caches[portal_name]
    for mod_name, mod_obj in target_cache.items():
        sys.modules[mod_name] = mod_obj

    # 4. Invalidate caches
    sys.path_importer_cache.clear()
    importlib.invalidate_caches()

    _active_portal = portal_name


def _clear_portal_context():
    global _active_portal
    if _active_portal is None:
        return

    # Save current active portal's modules
    saved_cache = _portal_module_caches[_active_portal]
    saved_cache.clear()
    for mod_name in list(sys.modules.keys()):
        if (
            mod_name.startswith("portal_schemas")
            or mod_name.startswith("portal_core")
            or mod_name.startswith("tests")
        ):
            saved_cache[mod_name] = sys.modules[mod_name]
            del sys.modules[mod_name]

    # Remove from sys.path
    sys.path = [
        p
        for p in sys.path
        if "Blue-Moon-Portal" not in p and "AquaGuard-Portal" not in p
    ]

    sys.path_importer_cache.clear()
    importlib.invalidate_caches()
    _active_portal = None
