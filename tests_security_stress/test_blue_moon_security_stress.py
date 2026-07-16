import sys
import os
import asyncio
import time
import shutil
from pathlib import Path
import logging
import pytest

# Add stack root and Blue-Moon-Portal directory to path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../Blue-Moon-Portal")
    ),
)


def _ensure_blue_moon_paths() -> None:
    """Skip early when Blue-Moon portal modules are unavailable."""
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../Blue-Moon-Portal")
    )
    schema_candidates = [
        os.path.join(base_dir, "portal_schemas"),
        os.path.join(base_dir, "src", "portal_schemas"),
    ]
    core_candidates = [
        os.path.join(base_dir, "portal_core"),
        os.path.join(base_dir, "src", "portal_core"),
    ]
    if not any(os.path.isdir(p) for p in schema_candidates + core_candidates):
        pytest.skip(
            "Blue-Moon-Portal submodule content is required. "
            "Run: git submodule update --init --recursive",
            allow_module_level=False,
        )

# Clean up cached portal modules to avoid monorepo namespace conflicts
for mod in list(sys.modules.keys()):
    if mod.startswith("portal_schemas") or mod.startswith("portal_core"):
        del sys.modules[mod]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] BlueMoonSecurityTest: %(message)s",
)
logger = logging.getLogger("BlueMoonSecurityTest")


def test_pydantic_constraints():
    _ensure_blue_moon_paths()
    from portal_schemas.ai_models import (
        SensorReading,
        CropOptimizationPlan,
    )
    from pydantic import ValidationError

    logger.info(
        "\n"
        + "=" * 50
        + "\nAUDIT: Blue Moon Pydantic Schemas constraints\n"
        + "=" * 50
    )

    # 1. Test valid reading
    try:
        valid_reading = SensorReading(
            sensor_id="moisture_1",
            sensor_type="capacitive_moisture",
            value=65.4,
            unit="%",
        )
        logger.info(
            f"✓ Valid telemetry parsing works: id={valid_reading.sensor_id}, value={valid_reading.value}"
        )
    except ValidationError as e:
        logger.error(f"❌ Failed to parse valid telemetry: {e}")
        raise

    # 2. Test invalid reading (string passed to value float field)
    try:
        SensorReading(
            sensor_id="moisture_1",
            sensor_type="capacitive_moisture",
            value="malicious_string_value",  # should fail
            unit="%",
        )
        logger.error(
            "❌ SECURITY FAILURE: Accepted string value for numerical sensor telemetry!"
        )
        raise AssertionError("Pydantic constraint bypass!")
    except ValidationError:
        logger.info(
            "✓ PASS: Correctly blocked string input on float telemetry value."
        )

    # 3. Test invalid plan actions (Enum constraints)
    try:
        CropOptimizationPlan(
            plan_id="opt-001",
            pump_action="super_high",  # invalid enum
            lighting_action="normal",
            confidence_score=0.9,
            execution_window_minutes=15,
            requires_human_review=False,
        )
        logger.error(
            "❌ SECURITY FAILURE: Accepted invalid enum command ('super_high')!"
        )
        raise AssertionError("Pydantic enum constraint bypass!")
    except ValidationError:
        logger.info("✓ PASS: Correctly blocked invalid pump enum command.")

    # 4. Test boundary constraints (confidence score range 0.0 - 1.0)
    try:
        CropOptimizationPlan(
            plan_id="opt-002",
            pump_action="medium",
            lighting_action="dim",
            confidence_score=1.5,  # invalid confidence > 1.0
            execution_window_minutes=15,
            requires_human_review=False,
        )
        logger.error(
            "❌ SECURITY FAILURE: Accepted out-of-range confidence score (1.5)!"
        )
        raise AssertionError("Pydantic validation range bypass!")
    except ValidationError:
        logger.info(
            "✓ PASS: Correctly blocked out-of-bounds confidence score (>1.0)."
        )


@pytest.mark.asyncio
async def test_pruner_stress():
    _ensure_blue_moon_paths()
    from portal_core.media_pruner import MediaPruner

    logger.info(
        "\n"
        + "=" * 50
        + "\nSTRESS TEST: Media Storage Cleanup and Pruner Capacity\n"
        + "=" * 50
    )

    # Set up temporary directories
    temp_media_dir = Path("./temp_test_media")
    temp_logs_dir = Path("./temp_test_logs")
    temp_media_dir.mkdir(exist_ok=True)
    temp_logs_dir.mkdir(exist_ok=True)

    # Generate mock files (100 files of size 1KB)
    file_count = 100
    logger.info(
        f"Generating {file_count} dummy media files under {temp_media_dir}..."
    )

    # Set some files modification dates to be older than retention (e.g. 3 hours ago)
    retention_hours = 2
    for i in range(file_count):
        file_path = temp_media_dir / f"test_frame_{i}.jpg"
        file_path.write_bytes(b"A" * 1024)  # 1KB file

        # Modify time of half of the files to be older than the retention threshold
        if i % 2 == 0:
            mtime = time.time() - (retention_hours + 1) * 3600  # older
        else:
            mtime = time.time()  # fresh

        os.utime(str(file_path), (mtime, mtime))

    # Initialize pruner with strict thresholds
    pruner = MediaPruner(
        media_dir=str(temp_media_dir),
        sensor_logs_dir=str(temp_logs_dir),
        retention_hours=retention_hours,
        critical_disk_usage_pct=95.0,
    )

    initial_stats = pruner.get_storage_stats()
    logger.info(
        f"Initial storage count: {initial_stats['media_count']} files, size={initial_stats['total_size_mb']:.4f} MB"
    )

    # Run pruning cycle
    deleted = await pruner.prune_old_media()
    logger.info(f"Pruner cycle executed. Deleted: {deleted} files.")

    post_stats = pruner.get_storage_stats()
    logger.info(
        f"Post cleanup storage count: {post_stats['media_count']} files."
    )

    # Clean up temp directories
    shutil.rmtree(temp_media_dir)
    shutil.rmtree(temp_logs_dir)

    # Assertions
    assert deleted == 50, f"Expected 50 files deleted, but got {deleted}"
    assert (
        post_stats["media_count"] == 50
    ), f"Expected 50 files remaining, but got {post_stats['media_count']}"
    logger.info(
        "✓ PASS: Storage pruner successfully enforces storage lifecycle and releases disk space."
    )


if __name__ == "__main__":
    test_pydantic_constraints()
    asyncio.run(test_pruner_stress())
    logger.info(
        "ALL BLUE MOON PORTAL SECURITY AND STRESS TESTS PASSED SUCCESSFULLY!"
    )
