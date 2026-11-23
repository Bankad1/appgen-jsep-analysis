import csv, collections, pathlib
HERE = pathlib.Path(__file__).parent
def rows(name):
    with open(HERE / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
def truthy(v):
    return str(v).strip().lower() in ("1", "true", "yes", "pass", "t")
def main():
    runs = rows("joined_runs.csv")
    req = rows("requirement_outcomes.csv")
    sp = {r["run_id"]: truthy(r["service_pass"]) for r in runs}
    mf = {r["run_id"]: truthy(r["model_full"]) for r in runs}
    both = sum(1 for k in sp if sp[k] and mf[k])
    service_only = sum(1 for k in sp if sp[k] and not mf[k])
    model_only = sum(1 for k in sp if not sp[k] and mf[k])
    neither = sum(1 for k in sp if not sp[k] and not mf[k])
    service_passes = sum(1 for k in sp if sp[k])
    print(f"projects total       : {len(runs)}  (expect 108)")
    print(f"both passed          : {both}  (expect 41)")
    print(f"service only         : {service_only}  (expect 44)")
    print(f"model only           : {model_only}  (expect 14)")
    print(f"neither              : {neither}  (expect 9)")
    print(f"disagreements        : {service_only + model_only}  (expect 58)")
    print(f"service passes       : {service_passes}  (expect 85)")
    pct = 100.0 * service_only / service_passes if service_passes else 0
    print(f"below-full of passes : {service_only}/{service_passes} = {pct:.1f}%  (expect 51.8%)")
    st = collections.Counter(r["status"].strip().upper() for r in req)
    passed = st.get("PASS", 0); failed = st.get("FAIL", 0)
    print(f"\nrequirement instances: {len(req)}  (expect 648)")
    print(f"  passed             : {passed}  (expect 556)")
    print(f"  failed             : {failed}  (expect 85)")
    print(f"  unassessable       : {len(req) - passed - failed}  (expect 7)")
    service_only_ids = {r["run_id"] for r in runs if truthy(r["service_pass"]) and not truthy(r["model_full"])}
    fails = collections.Counter()
    for r in req:
        if r["run_id"] in service_only_ids and r["status"].strip().upper() == "FAIL":
            fails[r["run_id"]] += 1
    dist = collections.Counter(fails.values())
    ge = lambda n: sum(1 for v in fails.values() if v >= n)
    print(f"\nservice-only projects by exact failed-check count: {dict(sorted(dist.items()))}")
    print(f"cumulative  >=1: {ge(1)}  >=2: {ge(2)}  >=3: {ge(3)}  (expect 44 / 18 / 5)")
    fam_fail = collections.Counter(); fam_assessed = collections.Counter()
    for r in req:
        fam = r["family"].strip(); s = r["status"].strip().upper()
        if s in ("PASS", "FAIL"): fam_assessed[fam] += 1
        if s == "FAIL": fam_fail[fam] += 1
    print("\nper-family failed/assessed:")
    for fam in sorted(fam_assessed):
        print(f"  {fam:8s} {fam_fail[fam]}/{fam_assessed[fam]}")
if __name__ == "__main__":
    main()
