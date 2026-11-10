import os

import cv2

from angle_calculator import AngleCalculator
from form_analyzer import FormAnalyzer
from pose_extractor import PoseExtractor


class GymFormChecker:
    """Combines pose extraction, angle calculation and form rules."""

    def __init__(self, exercise="SQUAT"):
        if exercise not in FormAnalyzer.get_available_exercises():
            raise ValueError(
                f"Exercise {exercise} not supported. "
                f"Available: {FormAnalyzer.get_available_exercises()}"
            )
        self.exercise = exercise
        self.extractor = PoseExtractor()

    def analyze_frame(self, frame):
        """Return (annotated_frame, analysis_or_None)."""
        landmarks = self.extractor.extract_landmarks(frame)
        if not landmarks:
            return frame, None

        angles = AngleCalculator.get_multiple_angles(landmarks)
        analysis = FormAnalyzer.analyze_form(self.exercise, angles)
        analysis["angles"] = angles

        frame = self.extractor.draw_skeleton(frame, landmarks)
        frame = self._draw_overlay(frame, angles, analysis)
        return frame, analysis

    def _draw_overlay(self, frame, angles, analysis):
        h, w, _ = frame.shape
        is_good = analysis["is_good_form"]
        status = "GOOD FORM" if is_good else "FORM ISSUES"
        color = (0, 200, 0) if is_good else (0, 0, 220)

        cv2.putText(frame, self.exercise, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        cv2.rectangle(frame, (10, 42), (260, 78), color, -1)
        cv2.putText(frame, status, (20, 68),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        y = 105
        for name, value in angles.items():
            cv2.putText(frame, f"{name}: {value:.0f} deg", (10, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 200), 2)
            y += 24

        if analysis["issues"]:
            for issue in analysis["issues"][:2]:
                cv2.putText(frame, f"! {issue['joint']}", (10, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
                y += 22

        cv2.putText(frame, f"{w}x{h}", (w - 110, h - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        return frame

    @staticmethod
    def _create_writer(output_path, fps, size):
        for codec in ("avc1", "mp4v"):
            writer = cv2.VideoWriter(
                output_path, cv2.VideoWriter_fourcc(*codec), fps, size
            )
            if writer.isOpened():
                return writer
            writer.release()
        raise RuntimeError(f"Could not open video writer for {output_path}")

    def process_video(self, input_path, output_path="analyzed_output.mp4"):
        """Analyze a video file, write an annotated copy and return a report."""
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {input_path}")

        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0

        writer = self._create_writer(output_path, fps, (width, height))

        frames_processed = 0
        frames_with_pose = 0
        good_frames = 0
        issue_counts = {}
        all_tips = set()
        last_analysis = None

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frames_processed += 1
                annotated, analysis = self.analyze_frame(frame)

                if analysis is not None:
                    frames_with_pose += 1
                    last_analysis = analysis
                    if analysis["is_good_form"]:
                        good_frames += 1
                    for issue in analysis["issues"]:
                        issue_counts[issue["joint"]] = (
                            issue_counts.get(issue["joint"], 0) + 1
                        )
                    all_tips.update(analysis["tips"])
                else:
                    cv2.putText(annotated, "NO POSE DETECTED", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                writer.write(annotated)
        finally:
            cap.release()
            writer.release()

        return self._build_report(
            output_path=output_path,
            frames_processed=frames_processed,
            frames_with_pose=frames_with_pose,
            good_frames=good_frames,
            total_frames=total_frames,
            issue_counts=issue_counts,
            tips=all_tips,
            last_analysis=last_analysis,
        )

    def _build_report(self, output_path, frames_processed, frames_with_pose,
                      good_frames, total_frames, issue_counts, tips,
                      last_analysis):
        report = "\n" + "=" * 50 + "\n"
        report += f"Exercise: {self.exercise}\n"
        report += f"Frames analyzed: {frames_processed}"
        if total_frames:
            report += f" / {total_frames}"
        report += f"\nFrames with pose detected: {frames_with_pose}\n"

        if frames_with_pose:
            good_pct = good_frames / frames_with_pose * 100
            report += f"Frames with good form: {good_frames} ({good_pct:.1f}%)\n"
        else:
            report += "No pose was detected in this video.\n"

        report += "=" * 50 + "\n"

        if issue_counts:
            report += "\nIssues Found (most frequent first):\n"
            ranked = sorted(issue_counts.items(), key=lambda kv: -kv[1])
            for i, (joint, count) in enumerate(ranked, 1):
                report += f"{i}. {joint}: off-target in {count} frame(s)\n"
        elif frames_with_pose:
            report += "\nForm looks good across the analyzed frames.\n"

        if tips:
            report += "\nSuggestions to Improve:\n"
            for tip in sorted(tips):
                report += f"- {tip}\n"

        if last_analysis and last_analysis.get("angles"):
            report += "\nLast frame joint angles:\n"
            for name, value in last_analysis["angles"].items():
                report += f"- {name}: {value:.1f} deg\n"

        report += f"\nAnnotated video saved to: {os.path.abspath(output_path)}\n"
        return report


if __name__ == "__main__":
    import sys

    exercise = sys.argv[1].upper() if len(sys.argv) > 1 else "SQUAT"
    video = sys.argv[2] if len(sys.argv) > 2 else "input.mp4"

    checker = GymFormChecker(exercise)
    print(checker.process_video(video, "analyzed_output.mp4"))
