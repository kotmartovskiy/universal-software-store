from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Platform:
    os_family: str
    os_version: str | None
    cpu_arch: str | None
    abi: str | None = None
    memory_mb: int | None = None
    runtimes: tuple[str, ...] = ()

@dataclass(frozen=True)
class Package:
    os_family: str
    os_version: str | None
    architecture: str | None
    fmt: str
    min_os_version: str | None = None
    max_os_version: str | None = None
    abi: str | None = None
    min_ram_mb: int | None = None
    runtime: str | None = None
    compatibility_layer: str | None = None
    emulator: str | None = None

@dataclass(frozen=True)
class Result:
    level: str
    score: int
    reason: str


def _version(v):
    if not v:
        return None
    nums = re.findall(r"\d+", v)
    return tuple(int(x) for x in nums) if nums else None


def _arch_relation(package_arch, device_arch):
    if not package_arch or not device_arch:
        return "unknown"
    p, d = package_arch.lower(), device_arch.lower()
    aliases = {"x86_64":"amd64", "x64":"amd64", "i386":"x86", "i486":"x86", "i586":"x86", "i686":"x86", "arm64":"aarch64"}
    p, d = aliases.get(p,p), aliases.get(d,d)
    if p == d:
        return "exact"
    if p in {"armv5","armv6","armv7","armhf"} and d in {"armv7","armv8","aarch64"}:
        return "conditional"
    if p == "x86" and d == "amd64":
        return "conditional"
    return "mismatch"


def compare(p: Package, d: Platform) -> Result:
    reasons = []
    if p.os_family.lower() != d.os_family.lower():
        if p.compatibility_layer or p.emulator:
            method = p.compatibility_layer or p.emulator
            return Result("assisted", 65, f"OS family differs; requires {method}")
        return Result("unsupported", 0, f"OS family mismatch: package={p.os_family}, device={d.os_family}")

    score = 70
    pv, dv = _version(p.os_version), _version(d.os_version)
    if pv and dv:
        if pv == dv:
            score += 15; reasons.append("OS version exact")
        elif ((not p.min_os_version or dv >= _version(p.min_os_version)) and (not p.max_os_version or dv <= _version(p.max_os_version))):
            score += 12; reasons.append("OS version inside supported range")
        elif p.min_os_version or p.max_os_version:
            return Result("unsupported", 0, "device OS is outside package supported range")
        else:
            score += 5; reasons.append("OS family matches; version requires verification")
    elif p.min_os_version or p.max_os_version:
        return Result("unsupported", 0, "package has OS range but device OS version is unknown")
    else:
        reasons.append("OS version incomplete")

    relation = _arch_relation(p.architecture, d.cpu_arch)
    if relation == "mismatch":
        return Result("unsupported", 0, f"CPU architecture mismatch: package={p.architecture}, device={d.cpu_arch}")
    if relation == "exact":
        score += 10; reasons.append("CPU architecture exact")
    elif relation == "conditional":
        score += 3; reasons.append("CPU architecture conditionally compatible")
    else:
        reasons.append("CPU architecture incomplete")

    if p.abi and d.abi:
        if p.abi.lower() == d.abi.lower():
            score += 5; reasons.append("ABI exact")
        elif p.compatibility_layer or p.emulator:
            reasons.append("ABI differs; compatibility mechanism required")
            score -= 10
        else:
            return Result("unsupported", 0, f"ABI mismatch: package={p.abi}, device={d.abi}")
    elif p.abi:
        reasons.append("ABI not known on device")

    if p.min_ram_mb and d.memory_mb:
        if d.memory_mb < p.min_ram_mb:
            return Result("unsupported", 0, f"insufficient RAM: requires {p.min_ram_mb} MB, device has {d.memory_mb} MB")
        reasons.append("RAM requirement satisfied")
    elif p.min_ram_mb:
        reasons.append("RAM requirement cannot be verified")

    if p.runtime:
        if p.runtime.lower() in {x.lower() for x in d.runtimes}:
            score += 3; reasons.append(f"runtime available: {p.runtime}")
        else:
            return Result("partial", max(40, min(score, 89)), f"runtime required: {p.runtime}; not confirmed")

    if p.emulator or p.compatibility_layer:
        method = p.compatibility_layer or p.emulator
        return Result("assisted", max(55, min(score, 94)), f"compatible with assistance: {method}; " + "; ".join(reasons))
    level = "native" if score >= 95 else "partial"
    return Result(level, min(score, 100), "; ".join(reasons))
