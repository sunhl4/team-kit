from {{package_name}}.models.duration import DurationNs, JobId, MakespanNs


def makespan(job: JobId, durations: list[DurationNs]) -> dict[str, str | int]:
    total = MakespanNs(sum(item.value for item in durations))
    return {
        "id": job.value,
        "summary": f"makespan_ns={total.value}",
        "makespan_ns": total.value,
    }
