"""
09 — Nucleus -> quarks -> four interactions -> Standard Model counting.

Claims: proton = uud, neutron = udd; strong binds quarks/nucleus; EM binds
electrons->atoms->steel; weak changes identities (radioactivity); 4 fundamental
interactions; SM organizes known elementary particles + 3 interactions;
chart counts 12 matter + 4 gauge-boson types + Higgs = 17 named entries
(one box each for photon, gluon, W, Z).

Experiment: encode the chart as data and assert counts; check nucleon charges
(2/3+2/3-1/3=+1; 2/3-1/3-1/3=0); check interaction list length 4.
This is a bookkeeping benchmark: it fails loudly if anyone miscounts the SM.
"""
from fractions import Fraction


def run_benchmark():
    matter = [
        "up", "charm", "top",
        "down", "strange", "bottom",
        "electron", "muon", "tau",
        "e-neutrino", "mu-neutrino", "tau-neutrino",
    ]
    gauge_types = ["photon", "gluon", "W", "Z"]  # W counts W+/W- as one box per narrative
    higgs = ["Higgs"]
    total = len(matter) + len(gauge_types) + len(higgs)

    Q_up, Q_down = Fraction(2, 3), Fraction(-1, 3)
    Q_proton = 2 * Q_up + Q_down
    Q_neutron = Q_up + 2 * Q_down

    interactions = ["strong", "electromagnetic", "weak", "gravitational"]
    sm_interactions = ["strong", "electromagnetic", "weak"]  # SM covers 3; gravity separate

    passed = bool(
        len(matter) == 12
        and len(gauge_types) == 4
        and len(higgs) == 1
        and total == 17
        and Q_proton == 1
        and Q_neutron == 0
        and len(interactions) == 4
        and len(sm_interactions) == 3
    )
    return {
        "name": "standard_model",
        "matter_count": len(matter),
        "gauge_types": gauge_types,
        "gauge_type_count": len(gauge_types),
        "higgs_count": len(higgs),
        "total_named_entries": total,
        "proton_quarks": "uud",
        "neutron_quarks": "udd",
        "proton_charge": float(Q_proton),
        "neutron_charge": float(Q_neutron),
        "four_interactions": interactions,
        "sm_covers_three": sm_interactions,
        "pass": passed,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_benchmark(), indent=2))
