from knowledge_engine import (
    load_services,
    load_schemes,
    search_services,
    search_schemes
)

services = load_services()
schemes = load_schemes()

print("")
print("======================================")
print(" GOVASSIST KNOWLEDGE BASE TEST")
print("======================================")
print("Services loaded :", len(services))
print("Schemes loaded  :", len(schemes))

print("")
print("SERVICE SEARCH: passport")
for item in search_services("passport"):
    print("-", item["name"])

print("")
print("SCHEME SEARCH: student scholarship")
for item in search_schemes("student scholarship"):
    print("-", item["name"])

print("")
print("KNOWLEDGE BASE STATUS: READY")
