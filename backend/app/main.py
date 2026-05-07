from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import Base, engine, SessionLocal
from app.models.agent import Agent
from app.models.column import Column_
from app.models.task import Task
from app.routers import agents, columns, tasks


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Column_).count() == 0:
            default_columns = [
                Column_(id="col-todo", name="待办", order=1.0),
                Column_(id="col-in-progress", name="进行中", order=2.0),
                Column_(id="col-in-review", name="审核中", order=3.0),
                Column_(id="col-done", name="已完成", order=4.0),
            ]
            db.add_all(default_columns)

        if db.query(Agent).count() == 0:
            default_agents = [
                Agent(id="f12a7462-778d-483a-974b-66114b4f1d44", name="Hermes-Assistant", role="协调者", description="集群协调者与全栈架构师", environment="macOS", status="working", avatar="🎯"),
                Agent(id="cd77f087-027d-49b6-a3b7-f01602efe63f", name="OpenClaw-Research", role="研究分析师", description="技术调研、信息收集、数据分析", environment="macOS", status="idle", avatar="🔬"),
                Agent(id="83fa22c4-8705-4e5e-96b5-d6a76930da24", name="Hermes-WSL", role="DevOps", description="基础设施与系统运维", environment="WSL", status="working", avatar="🛠️"),
                Agent(id="3844dfc6-41f9-4f58-a21b-20d4e0e792a3", name="ki mi", role="后端开发", description="API 设计、数据库、服务端逻辑", environment="Ubuntu", status="idle", avatar="⚙️"),
                Agent(id="9de36673-cb57-4048-a260-c3c40b76912b", name="v mo pen c la w", role="前端开发", description="UI/UX设计、React/Vue开发", environment="Ubuntu", status="idle", avatar="🎨"),
                Agent(id="72b03301-b3ff-406f-b549-df8b3ba01262", name="gemini", role="QA", description="测试用例、代码审查、Bug追踪", environment="macOS", status="idle", avatar="✅"),
                Agent(id="8eb3afe4-088b-4322-9f7a-86454adb6688", name="Claude-Architect", role="架构师", description="高级代码开发与复杂系统架构", environment="macOS", status="idle", avatar="🏗️"),
                Agent(id="af392c49-ce89-4433-998d-763a9257bd87", name="Claude-Builder", role="高级开发", description="WSL 高级开发与跨平台兼容性", environment="WSL", status="idle", avatar="🔧"),
                Agent(id="5f6f77e9-c868-47c0-ac44-971709e8ce4e", name="Kimi-Scripter", role="工具开发", description="macOS 本地工具链与自动化", environment="macOS", status="idle", avatar="🛠️"),
                Agent(id="a1b8fd4f-fa80-4c20-ae34-9f11a3e6f086", name="Kimi-Engineer", role="数据工程师", description="WSL 后端开发与大规模数据处理", environment="WSL", status="idle", avatar="📊"),
            ]
            db.add_all(default_agents)

        db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents.router)
app.include_router(tasks.router)
app.include_router(columns.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
