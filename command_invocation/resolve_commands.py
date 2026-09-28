#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
DATA=json.loads(Path(__file__).with_name("COMMANDS.json").read_text())
COMMANDS={x["command"]:x for x in DATA["commands"]}; ALIASES=DATA.get("aliases",{})
PROFILE_TYPES={"profile_macro","fear_city_macro","fear_city_override_macro","elevation_macro"}
def parse(text):
    tokens=[ALIASES.get(t,t) for t in re.findall(r"/sc-[A-Za-z0-9-]+",text)]
    return tokens,[t for t in tokens if t not in COMMANDS]
def resolve(text):
    tokens,unknown=parse(text)
    if unknown:return {"status":"ERROR","error":"UNKNOWN_COMMAND","commands":unknown}
    profiles=[t for t in tokens if COMMANDS[t]["type"] in PROFILE_TYPES]
    if len(profiles)>1:return {"status":"ERROR","error":"PROFILE_CONFLICT","commands":profiles}
    selectors=[t for t in tokens if COMMANDS[t]["type"]=="profile_selector"]
    if len({COMMANDS[t]["expands_to"]["profile"] for t in profiles+selectors})>1:
        return {"status":"ERROR","error":"PROFILE_CONFLICT","commands":profiles+selectors}
    backdrops=sorted({t for t in tokens if COMMANDS[t]["type"]=="backdrop_preset"})
    if len(backdrops)>1:
        return {"status":"ERROR","error":"BACKDROP_PRESET_CONFLICT","commands":backdrops}
    if backdrops:
        bundle=COMMANDS[backdrops[0]]["expands_to"]
        conflicts=[]
        for t in tokens:
            c=COMMANDS[t]
            # Elevation is an inherited compound command. BD02 intentionally
            # selects T08 instead of its T02 default, independent of token order.
            if c["type"]=="diagnostic" or t=="/sc-rdr2-elevation":continue
            if any(k in bundle and bundle[k]!=v for k,v in c["expands_to"].items()):
                conflicts.append(t)
        if conflicts:return {"status":"ERROR","error":"BACKDROP_CONFIG_CONFLICT","commands":conflicts}
    config={
      "profile":None,"mode":None,"camera":None,"fear_city_identity":None,
      "preservation":None,"uncertainty":None,"explicit_fear_city_profile_override":False,
      "identity_lock":None,"occlusion_lock":None,"frontalization":None,
      "aspect_ratio":None,"street_presence":None
    };diagnostics=[]
    for t in tokens:
        c=COMMANDS[t]
        if c["type"]=="diagnostic":diagnostics.append(c["expands_to"]["action"])
        else:config.update(c["expands_to"])
    if backdrops:config.update(bundle)
    if not tokens:return {"status":"NO_CIL_COMMANDS","config":config}
    return {"status":"OK","commands":tokens,"config":config,"diagnostics":diagnostics}
if __name__=="__main__": print(json.dumps(resolve(" ".join(sys.argv[1:])),indent=2,ensure_ascii=False))
