"""
Clean Day09 report generator
"""

import argparse
import json
import re
from collections import defaultdict, Counter
from datetime import datetime, timezone
from typing import Dict, List, Tuple


ISO_FMT = "%Y-%m-%dT%H:%M:%SZ"


def parse_line(line: str) -> Tuple[List[int], str, datetime]:
    parts = line.strip().split("\t")
    if len(parts) < 3:
        raise ValueError("Unexpected line format: " + line)
    subject = parts[2]
    timestamp_str = parts[-1]
    timestamp = datetime.strptime(timestamp_str, ISO_FMT).replace(tzinfo=timezone.utc)
    days = [int(m) for m in re.findall(r"day\s*0*([0-9]+)", subject, re.IGNORECASE)]
    m = re.search(r"by\s+(.+)$", subject, re.IGNORECASE)
    if m:
        name = m.group(1).strip()
    else:
        name = re.sub(r"day\s*[0-9]+", "", subject, flags=re.IGNORECASE).strip(" -:_")
    return days or [], name or "(unknown)", timestamp


def load_submissions(path: str) -> Dict[str, Dict[int, datetime]]:
    submissions: Dict[str, Dict[int, datetime]] = defaultdict(dict)
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            try:
                days, name, ts = parse_line(line)
            except Exception:
                continue
            for d in days:
                prev = submissions[name].get(d)
                if prev is None or ts < prev:
                    submissions[name][d] = ts
    return submissions


def infer_deadlines(submissions: Dict[str, Dict[int, datetime]]) -> Dict[int, datetime]:
    dates_per_day: Dict[int, List[datetime]] = defaultdict(list)
    for name, days in submissions.items():
        for d, ts in days.items():
            dates_per_day[d].append(ts)
    deadlines: Dict[int, datetime] = {}
    for d, tss in dates_per_day.items():
        earliest = min(tss)
        deadline = datetime(earliest.year, earliest.month, earliest.day, 23, 59, 59, tzinfo=timezone.utc)
        deadlines[d] = deadline
    return deadlines


def human(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def ascii_bar(pct: float, width: int = 40) -> str:
    filled = int(round(pct / 100 * width))
    return "[" + "#" * filled + " " * (width - filled) + "]"


def print_table(headers: List[str], rows: List[List[str]]):
    try:
        from tabulate import tabulate
        print(tabulate(rows, headers=headers, tablefmt="github"))
    except Exception:
        if not rows:
            print("(no rows)")
            return
        cols = list(zip(*([headers] + rows)))
        widths = [max(len(str(x)) for x in c) for c in cols]
        fmt = "  ".join("{:<%d}" % w for w in widths)
        print(fmt.format(*headers))
        for r in rows:
            print(fmt.format(*r))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", default="subjects.txt", help="subjects.txt path")
    p.add_argument("--milestones", nargs="*", type=int, default=[6, 7, 8], help="day numbers considered milestones")
    p.add_argument("--deadlines-file", help="optional JSON file mapping day->ISO timestamp (Z) for deadlines")
    args = p.parse_args()

    subs = load_submissions(args.file)
    students = sorted(subs.keys())
    all_days = sorted({d for days in subs.values() for d in days})

    if args.deadlines_file:
        with open(args.deadlines_file, encoding="utf-8") as fh:
            ddata = json.load(fh)
        deadlines = {int(k): datetime.strptime(v, ISO_FMT).replace(tzinfo=timezone.utc) for k, v in ddata.items()}
    else:
        deadlines = infer_deadlines(subs)

    print("\n**Summary**")
    print(f"Total students detected: {len(students)}")
    print(f"Days found in data: {', '.join(str(d) for d in all_days)}")

    print("\n**Missing Submissions (per day)**")
    rows = []
    for d in all_days:
        missing = [s for s in students if d not in subs[s]]
        rows.append([str(d), str(len(missing)), ", ".join(missing[:10]) + ("..." if len(missing) > 10 else "")])
    print_table(["Day", "Missing Count", "Examples"], rows)

    print("\n**Late Submissions**")
    late_rows = []
    for d in sorted(deadlines.keys()):
        dl = deadlines[d]
        for s in students:
            if d in subs[s]:
                ts = subs[s][d]
                if ts > dl:
                    late_rows.append([str(d), s, human(ts), human(dl), f"{(ts - dl).total_seconds()/3600:.1f}h late"])
    if late_rows:
        print_table(["Day", "Student", "Sub Time", "Deadline", "Offset"], late_rows)
    else:
        print("No late submissions detected using current deadlines.")

    print("\n**Timing Distribution (hours relative to deadline)**")
    buckets = [(-9999, -48), (-48, -24), (-24, -12), (-12, -6), (-6, -1), (-1, 0), (0, 1), (1, 6), (6, 24), (24, 48), (48, 9999)]
    bucket_labels = ["<-48h", "-48--24", "-24--12", "-12--6", "-6--1", "-1-0", "0-1", "1-6", "6-24", "24-48", ">48h"]
    counts = Counter()
    total_samples = 0
    for s in students:
        for d, ts in subs[s].items():
            dl = deadlines.get(d)
            if not dl:
                continue
            hours = (ts - dl).total_seconds() / 3600.0
            total_samples += 1
            for (lo, hi), label in zip(buckets, bucket_labels):
                if lo < hours <= hi:
                    counts[label] += 1
                    break

    rows = []
    for label in bucket_labels:
        cnt = counts[label]
        pct = (cnt / total_samples * 100) if total_samples else 0
        rows.append([label, str(cnt), f"{pct:.1f}%", ascii_bar(pct)])
    print_table(["Bucket", "Count", "Percent", "Bar"], rows)

    print("\n**Peak Activity Times (by time-of-day)**")
    tod_buckets = {
        "Late Night (00-05)": range(0, 6),
        "Morning (06-11)": range(6, 12),
        "Afternoon (12-17)": range(12, 18),
        "Evening (18-23)": range(18, 24),
    }
    tod_counts = Counter()
    hour_counts = Counter()
    for s in students:
        for d, ts in subs[s].items():
            h = ts.astimezone(timezone.utc).hour
            hour_counts[h] += 1
            for label, hrange in tod_buckets.items():
                if h in hrange:
                    tod_counts[label] += 1
                    break

    rows = []
    tot = sum(tod_counts.values())
    for label in tod_buckets.keys():
        cnt = tod_counts[label]
        pct = (cnt / tot * 100) if tot else 0
        rows.append([label, str(cnt), f"{pct:.1f}%", ascii_bar(pct)])
    print_table(["Time Window", "Count", "Percent", "Bar"], rows)

    print("\nSubmissions by hour (UTC):")
    hour_rows = [[str(h).zfill(2), str(hour_counts[h])] for h in range(24)]
    print_table(["Hour", "Count"], hour_rows)

    ms = args.milestones
    print(f"\n**Completion Rate for milestones: {ms}**")
    completed = [s for s in students if all(d in subs[s] for d in ms)]
    pct = (len(completed) / len(students) * 100) if students else 0
    print(f"Completed all {len(ms)} milestones: {len(completed)}/{len(students)} ({pct:.1f}%)")
    print(ascii_bar(pct))

    missing_any = [(s, [str(d) for d in ms if d not in subs[s]]) for s in students if not all(d in subs[s] for d in ms)]
    if missing_any:
        rows = [[s, ", ".join(miss)] for s, miss in missing_any]
        print_table(["Student", "Missing Milestones"], rows)
    else:
        print("All students completed the specified milestones.")


if __name__ == "__main__":
    main()
