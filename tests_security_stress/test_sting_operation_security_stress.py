import sys
import os
import asyncio
import time
import logging
import pytest

# Add stack root to path
sys.path.insert(
 0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

logging.basicConfig(
 level=logging.INFO,
 format="%(asctime)s [%(levelname)s] StingSecurityTest: %(message)s",
)
logger = logging.getLogger("StingSecurityTest")


class FrameQueueProcessor:
 """
 Mock vision queue to test frame dropped rate and memory allocation under stress.
 Similar to local edge loop processing camera streams.
 """

 def __init__(self, max_buffer_size: int = 5):
 self.queue = asyncio.Queue(maxsize=max_buffer_size)
 self.processed_count = 0
 self.dropped_count = 0

 async def ingest_frame(self, frame_id: int):
 try:
 # Non-blocking put; if queue is full, drop the frame to prevent memory blowout
 self.queue.put_nowait(frame_id)
 except asyncio.QueueFull:
 self.dropped_count += 1

 async def run_inference_loop(self):
 while True:
 _ = await self.queue.get()
 # Simulate local NPU inference time (~10ms)
 await asyncio.sleep(0.01)
 self.processed_count += 1
 self.queue.task_done()


def validate_detection_box(
 x: float, y: float, w: float, h: float, score: float, img_size: int = 640
) -> bool:
 """
 Validates bounding box coordinates to ensure they reside in reasonable bounds.
 Prevents coordinate overflows before triggering hardware actuators.
 """
 # Score threshold check
 if not (0.0 <= score <= 1.0):
 return False

 # Coordinate range checks
 if x < 0 or x > img_size or y < 0 or y > img_size:
 return False

 if w <= 0 or w > img_size or h <= 0 or h > img_size:
 return False

 return True


def test_box_coordinate_guards():
 logger.info(
 "\n" + "=" * 50 + "\nAUDIT: YOLO Box Coordinate Guards\n" + "=" * 50
 )

 test_cases = [
 # x, y, w, h, score, expected
 (320.0, 240.0, 50.0, 50.0, 0.85, True), # Valid
 (-10.0, 240.0, 50.0, 50.0, 0.90, False), # Out of bounds x
 (320.0, 700.0, 50.0, 50.0, 0.95, False), # Out of bounds y
 (320.0, 240.0, -5.0, 50.0, 0.80, False), # Invalid negative width
 (320.0, 240.0, 50.0, 50.0, 1.25, False), # Invalid confidence score
 ]

 for x, y, w, h, score, expected in test_cases:
 is_valid = validate_detection_box(x, y, w, h, score)
 outcome = "PASS" if is_valid == expected else "FAIL"
 logger.info(
 f"Box: [{x}, {y}, {w}, {h}], score={score} -> Validated: {is_valid} (Expected: {expected}) -> {outcome}"
 )
 assert (
 outcome == "PASS"
 ), f"Coordinate validation failed for: Box={x, y, w, h}"

 logger.info(
 "[OK] PASS: Coordinate guard filters out corrupted or adversarial bounding boxes."
 )


@pytest.mark.asyncio
async def test_frame_ingestion_stress():
 logger.info(
 "\n"
 + "=" * 50
 + "\nSTRESS TEST: High-Frequency Camera Frame Ingestion\n"
 + "=" * 50
 )

 processor = FrameQueueProcessor(max_buffer_size=5)

 # Start loop in background
 inference_task = asyncio.create_task(processor.run_inference_loop())

 # Simulate feeding 500 frames at high speed.
 # On Windows, sleep(0.0083) can be rounded up to 15.6ms, which matches or exceeds the 10ms
 # inference sleep, preventing the queue from filling. We use 0.0 to yield control to the event loop
 # while maintaining a throughput that stress-tests the queue limits.
 total_frames = 500

 start_time = time.perf_counter()
 logger.info(
 f"Simulating feed of {total_frames} camera frames under stress..."
 )

 for i in range(total_frames):
 await processor.ingest_frame(i)
 await asyncio.sleep(0.0)

 duration = time.perf_counter() - start_time

 # Wait for remaining queue items
 await asyncio.sleep(0.2)
 inference_task.cancel()

 logger.info("Stress results:")
 logger.info(f" Total Duration: {duration:.3f} s")
 logger.info(f" Processed Frames: {processor.processed_count}")
 logger.info(f" Dropped Frames (Queue Full): {processor.dropped_count}")
 logger.info(
 f" Frame Drop Rate: {processor.dropped_count / total_frames * 100:.1f}%"
 )

 # Confirm it dropped frames rather than building memory backlogs
 assert (
 processor.dropped_count > 0
 ), "Stress loop did not activate frame dropping!"
 logger.info(
 "[OK] PASS: Frame drop strategy successfully prevented queue backing and out-of-memory states."
 )


if __name__ == "__main__":
 test_box_coordinate_guards()
 asyncio.run(test_frame_ingestion_stress())
 logger.info(
 "ALL STING OPERATION AI SECURITY AND STRESS TESTS PASSED SUCCESSFULLY!"
 )
