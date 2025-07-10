# rdf_extractor.py

from rdflib import Graph
import sys
import os

def detect_format(file_path):
    if file_path.endswith('.ttl'):
        return 'turtle'
    elif file_path.endswith('.nt'):
        return 'nt'
    elif file_path.endswith('.xml') or file_path.endswith('.rdf'):
        return 'xml'
    else:
        raise ValueError("Unsupported RDF format. Use .ttl, .nt, or .rdf/.xml")

def load_rdf(file_path):
    rdf_format = detect_format(file_path)
    g = Graph()
    g.parse(file_path, format=rdf_format)
    print(f"✅ Loaded {len(g)} triples from {file_path}")
    return g

def print_all_triples(graph, limit=20):
    print(f"\n🔍 Showing up to {limit} triples:\n")
    for i, (s, p, o) in enumerate(graph):
        print(f"{i+1}: {s} -- {p} --> {o}")
        if i + 1 >= limit:
            break

def run_sparql_query(graph, query):
    results = graph.query(query)
    print("\n📊 SPARQL Query Results:\n")
    for row in results:
        print(" | ".join(str(v) for v in row))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python rdf_extractor.py </Users/roopakkrishna/Downloads/dcterms.rdf>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    g = load_rdf("/Users/roopakkrishna/Downloads/dcterms.rdf")
    print_all_triples(g, limit=30)

    # Optional: Uncomment this to run a custom SPARQL query
    # sample_query = """
    # SELECT ?s ?p ?o
    # WHERE {
    #     ?s ?p ?o .
    # }
    # LIMIT 10
    # """
    # run_sparql_query(g, sample_query)
