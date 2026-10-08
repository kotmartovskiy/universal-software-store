from dataclasses import dataclass
@dataclass(frozen=True)
class Platform:
    os_family:str; os_version:str|None; cpu_arch:str|None; abi:str|None=None
@dataclass(frozen=True)
class Package:
    os_family:str; os_version:str|None; architecture:str|None; fmt:str
@dataclass(frozen=True)
class Result:
    level:str; score:int; reason:str

def compare(p:Package,d:Platform)->Result:
    if p.os_family.lower()!=d.os_family.lower():
        return Result('unsupported',0,f'OS family mismatch: package={p.os_family}, device={d.os_family}')
    score=70
    reasons=[]
    if p.os_version and d.os_version:
        if p.os_version==d.os_version: score+=20; reasons.append('OS version exact')
        else: score+=5; reasons.append('OS family matches; version requires verification')
    else: reasons.append('OS version incomplete')
    if p.architecture and d.cpu_arch:
        if p.architecture.lower()==d.cpu_arch.lower(): score+=10; reasons.append('CPU architecture exact')
        else: return Result('unsupported',0,f'CPU architecture mismatch: package={p.architecture}, device={d.cpu_arch}')
    else: reasons.append('CPU architecture incomplete')
    level='native' if score>=95 else 'partial'
    return Result(level,min(score,100),'; '.join(reasons))
