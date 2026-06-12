import sys
import os
import asyncio
import time
import shutil
import json
from pathlib import Path
import logging
import pytest

# Add stack root and AquaGuard-Portal directory to path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../AquaGuard-Portal")
    ),
)

# Clean up cached portal modules to avoid monorepo namespace conflicts
for mod in list(sys.modules.keys()):
    if mod.startswith("portal_schemas") or mod.startswith("portal_core"):
        del sys.modules[mod]

from portal_schemas.compliance import (
    WaterSensorReading,
    WaterOptimizationPlan,
)
from portal_core.media_pruner import MediaPruner
from pydantic import ValidationError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] AquaGuardSecurityTest: %(message)s",
)
logger = logging.getLogger("AquaGuardSecurityTest")


def test_pydantic_constraints():
    logger.info(
        "\n"
        + "=" * 50
        + "\nAUDIT: AquaGuard Pydantic Schemas constraints\n"
        + "=" * 50
    )

    # 1. Test valid reading
    try:
        valid_reading = WaterSensorReading(
            sensor_id="ph_sensor_1", sensor_type="pH", value=7.32, unit="pH"
        )
        logger.info(
            f"✓ Valid telemetry parsing works: id={valid_reading.sensor_id}, value={valid_reading.value}"
        )
    except ValidationError as e:
        logger.error(f"❌ Failed to parse valid telemetry: {e}")
        raise

    # 2. Test invalid reading (string passed to value float field)
    try:
        WaterSensorReading(
            sensor_id="do_sensor_1",
            sensor_type="DO",
            value="invalid_str_payload",  # should fail
            unit="mg/L",
        )
        logger.error(
            "❌ SECURITY FAILURE: Accepted string value for float telemetry value!"
        )
        raise AssertionError("Pydantic type constraint bypass!")
    except ValidationError:
        logger.info(
            "✓ PASS: Correctly blocked string input on float telemetry value."
        )

    # 3. Test invalid plan actions (Enum constraints)
    try:
        WaterOptimizationPlan(
            plan_id="opt-9988",
            aeration_action="super_high",  # invalid enum
            pump_action="medium",
            valve_action="closed",
            confidence_score=0.9,
            execution_window_minutes=15,
            requires_human_review=False,
        )
        logger.error(
            "❌ SECURITY FAILURE: Accepted invalid enum command for aerator ('super_high')!"
        )
        raise AssertionError("Pydantic enum constraint bypass!")
    except ValidationError:
        logger.info("✓ PASS: Correctly blocked invalid aeration enum command.")

    # 4. Test boundary constraints (confidence score range 0.0 - 1.0)
    try:
        WaterOptimizationPlan(
            plan_id="opt-9989",
            aeration_action="high",
            pump_action="medium",
            valve_action="closed",
            confidence_score=-0.5,  # invalid confidence < 0.0
            execution_window_minutes=15,
            requires_human_review=False,
        )
        logger.error(
            "❌ SECURITY FAILURE: Accepted out-of-range confidence score (-0.5)!"
        )
        raise AssertionError("Pydantic validation range bypass!")
    except ValidationError:
        logger.info(
            "✓ PASS: Correctly blocked out-of-bounds confidence score (<0.0)."
        )


@pytest.mark.asyncio
async def test_pruner_stress():
    logger.info(
        "\n"
        + "=" * 50
        + "\nSTRESS TEST: AquaGuard Storage Cleanup and Pruner Retention\n"
        + "=" * 50
    )

    # Set up temporary directories
    temp_media_dir = Path("./temp_aquaguard_media")
    temp_logs_dir = Path("./temp_aquaguard_logs")
    temp_compliance_dir = Path("./temp_aquaguard_compliance")

    temp_media_dir.mkdir(exist_ok=True)
    temp_logs_dir.mkdir(exist_ok=True)
    temp_compliance_dir.mkdir(exist_ok=True)

    # Generate 100 dummy media files
    file_count = 100
    retention_hours = 2
    logger.info(
        f"Generating {file_count} dummy media files under {temp_media_dir}..."
    )
    for i in range(file_count):
        file_path = temp_media_dir / f"test_frame_{i}.jpg"
        file_path.write_bytes(b"A" * 1024)  # 1KB

        # Modify time of half of the files to be older than retention
        if i % 2 == 0:
            mtime = time.time() - (retention_hours + 1) * 3600
        else:
            mtime = time.time()
        os.utime(str(file_path), (mtime, mtime))

    # Generate a dummy compliance CSV/JSON that should NEVER be pruned
    compliance_json = (
        temp_compliance_dir / "audit_20260607_120000_aud-test.json"
    )
    compliance_json.write_text(
        json.dumps({"audit_id": "aud-test", "status": "compliant"}),
        encoding="utf-8",
    )

    # Set compliance file mod time to be very old (e.g. 10 days ago) to stress test retention protection
    old_time = time.time() - 10 * 24 * 3600
    os.utime(str(compliance_json), (old_time, old_time))

    # Initialize pruner
    pruner = MediaPruner(
        media_dir=str(temp_media_dir),
        sensor_logs_dir=str(temp_logs_dir),
        compliance_dir=str(temp_compliance_dir),
        retention_hours=retention_hours,
        critical_disk_usage_pct=95.0,
    )

    initial_stats = pruner.get_storage_stats()
    logger.info(
        f"Initial stats: media_count={initial_stats['media_count']}, compliance_count={initial_stats['compliance_count']}"
    )

    # Run pruning cycle
    deleted = await pruner.prune_old_media()
    logger.info(f"Pruner cycle executed. Deleted: {deleted} files.")

    post_stats = pruner.get_storage_stats()
    logger.info(
        f"Post cleanup stats: media_count={post_stats['media_count']}, compliance_count={post_stats['compliance_count']}"
    )

    # Clean up temp directories
    shutil.rmtree(temp_media_dir)
    shutil.rmtree(temp_logs_dir)
    shutil.rmtree(temp_compliance_dir)

    # Assertions
    assert deleted == 50, f"Expected 50 files deleted, but got {deleted}"
    assert (
        post_stats["media_count"] == 50
    ), f"Expected 50 files remaining, but got {post_stats['media_count']}"
    assert (
        post_stats["compliance_count"] == 1
    ), "❌ SECURITY FAILURE: Compliance reports were pruned!"
    logger.info(
        "✓ PASS: MediaPruner prunes old media files but preserves regional council compliance audits."
    )


if __name__ == "__main__":
    test_pydantic_constraints()
    asyncio.run(test_pruner_stress())
    logger.info(
        "ALL AQUAGUARD PORTAL SECURITY AND STRESS TESTS PASSED SUCCESSFULLY!"
    )
