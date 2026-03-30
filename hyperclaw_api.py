# hyperclaw_api.py

from fastapi import FastAPI
from pydantic import BaseModel
import uuid, random, copy, json, os, asyncio

app = FastAPI()

POP_SIZE = 8
ELITE_K = 2
STATE_PATH = "./hyperclaw_state.json"

# ---------------------------
# Graph-based agent structure
# ---------------------------
def new_graph():
    return {
        "nodes": {
            "input": {"type": "io"},
            "planner": {"type": "llm", "prompt": "Plan the solution."},
            "executor": {"type": "llm", "prompt": "Execute the plan."},
            "output": {"type": "io"}
        },
        "edges": [
            ("input", "planner"),
            ("planner", "executor"),
            ("executor", "output")
        ]
    }

def init_agent():
    return {
        "id": str(uuid.uuid4()),
        "graph": new_graph(),
        "meta": {"strategy": "mutate graph + prompts"},
        "fitness": 0.0
    }

# ---------------------------
# Persistence
# ---------------------------
def save_state(pop, archive):
    with open(STATE_PATH, "w") as f:
        json.dump({"pop": pop, "archive": archive}, f)

def load_state():
    if not os.path.exists(STATE_PATH):
        return [init_agent() for _ in range(POP_SIZE)], []
    with open(STATE_PATH, "r") as f:
        data = json.load(f)
        return data["pop"], data["archive"]

POPULATION, ARCHIVE = load_state()

# ---------------------------
# Request schema
# ---------------------------
class ChatRequest(BaseModel):
    model: str
    messages: list

# ---------------------------
# Graph execution (OpenClaw-like)
# ---------------------------
def run_graph(agent, messages):
    graph = agent["graph"]
    data = messages[-1]["content"]

    for (src, dst) in graph["edges"]:
        node = graph["nodes"][dst]

        if node["type"] == "llm":
            data = f"[{dst}] {node['prompt']} → {data}"
        elif node["type"] == "tool":
            data = f"[tool:{dst}] processed({data})"

    return data

# ---------------------------
# Evaluation (replaceable)
# ---------------------------
def evaluate(output):
    # Placeholder: replace with real metrics (profit/tests/etc.)
    return len(output) % 10

# ---------------------------
# Mutation (STRUCTURAL)
# ---------------------------
def mutate(agent):
    a = copy.deepcopy(agent)
    g = a["graph"]

    # mutate prompt
    if random.random() < 0.4:
        node = random.choice(list(g["nodes"].values()))
        if "prompt" in node:
            node["prompt"] += random.choice([
                " Be concise.",
                " Think step-by-step.",
                " Optimize output."
            ])

    # add node
    if random.random() < 0.2:
        nid = f"node_{uuid.uuid4().hex[:4]}"
        g["nodes"][nid] = {
            "type": random.choice(["llm", "tool"]),
            "prompt": "New transformation node"
        }
        src = random.choice(list(g["nodes"].keys()))
        g["edges"].append((src, nid))

    # remove edge
    if random.random() < 0.2 and g["edges"]:
        g["edges"].pop(random.randrange(len(g["edges"])))

    a["id"] = str(uuid.uuid4())
    a["fitness"] = 0.0
    return a

# ---------------------------
# Crossover (graph merge)
# ---------------------------
def crossover(a, b):
    child = copy.deepcopy(a)

    # merge nodes
    for k, v in b["graph"]["nodes"].items():
        if random.random() < 0.5:
            child["graph"]["nodes"][k + "_b"] = v

    # merge edges
    child["graph"]["edges"] += random.sample(
        b["graph"]["edges"],
        k=min(len(b["graph"]["edges"]), 2)
    )

    child["id"] = str(uuid.uuid4())
    child["fitness"] = 0.0
    return child

# ---------------------------
# Selection
# ---------------------------
def select(pop):
    return sorted(pop, key=lambda x: x["fitness"], reverse=True)

# ---------------------------
# Async evaluation
# ---------------------------
async def eval_agent(agent, messages):
    output = run_graph(agent, messages)
    score = evaluate(output)
    return agent, score, output

async def evaluate_population(population, messages):
    tasks = [eval_agent(a, messages) for a in population]
    results = await asyncio.gather(*tasks)

    for agent, score, output in results:
        agent["fitness"] = score
        if score > 7:
            ARCHIVE.append(copy.deepcopy(agent))

# ---------------------------
# Evolution step
# ---------------------------
async def evolve(population, messages):
    await evaluate_population(population, messages)

    ranked = select(population)
    elites = ranked[:ELITE_K]

    new_pop = elites.copy()

    while len(new_pop) < POP_SIZE:
        if random.random() < 0.5:
            parent = random.choice(elites)
            child = mutate(parent)
        else:
            p1, p2 = random.sample(elites, 2)
            child = crossover(p1, p2)

        new_pop.append(child)

    return new_pop, elites[0]

# ---------------------------
# Meta² (evolving evolution)
# ---------------------------
def meta_meta_update():
    global ELITE_K

    if len(ARCHIVE) > 20:
        ELITE_K = min(ELITE_K + 1, POP_SIZE - 1)

# ---------------------------
# Main endpoint
# ---------------------------
@app.post("/v1/chat/completions")
async def chat(req: ChatRequest):
    global POPULATION

    POPULATION, best = await evolve(POPULATION, req.messages)
    meta_meta_update()

    output = run_graph(best, req.messages)

    save_state(POPULATION, ARCHIVE)

    return {
        "id": str(uuid.uuid4()),
        "object": "chat.completion",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": output
            }
        }],
        "debug": {
            "best_fitness": best["fitness"],
            "archive_size": len(ARCHIVE),
            "elite_k": ELITE_K,
            "population": len(POPULATION)
        }
    }
