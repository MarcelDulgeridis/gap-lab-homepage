"""Schema.org-Personenknoten (von Seitenmodulen und Generator gemeinsam genutzt)."""
from siteinfo import SITE, PARTNERS

DOMAIN = SITE["domain"]


def person_node(key, full=True):
    p = PARTNERS[key]
    node = {"@id": f"{DOMAIN}/ueber-uns#{key}"}
    if not full:
        return node
    node.update({
        "@type": "Person",
        "name": p["name"],
        "jobTitle": p["job_title"],
        "description": p["schema_desc"],
        "image": f"{DOMAIN}{p['img']}",
        "worksFor": {"@id": f"{DOMAIN}/#organization"},
        "url": f"{DOMAIN}/ueber-uns#{key}",
        "sameAs": p["same_as"],
        "knowsAbout": p["knows_about"],
    })
    return node


def person_nodes():
    return [person_node(k, full=True) for k in PARTNERS]
