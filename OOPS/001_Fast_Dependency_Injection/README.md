Dependency Injection (DI) decouples the creation of a dependency from its use. Instead of a class or function instantiating its collaborators directly, the needed instances are provided (injected) from the outside. This keeps code modular, easier to test, and easier to replace implementations (e.g., swapping a real service for a mock).

Core benefits
- Looser coupling: consumers depend on interfaces/protocols, not concrete implementations.
- Testability: swap in fakes/mocks without touching production code paths.
- Composability: wire behaviors in one place (composition root) instead of scattering `new`/constructors.

Common injection styles
- Constructor injection: dependencies arrive via `__init__` arguments; preferred for required collaborators.
- Setter/property injection: assign dependencies after construction; useful for optional collaborators.
- Function/parameter injection: pass dependencies directly to functions; great for pure functions and FastAPI dependencies.

Python examples (without frameworks)
```python
class EmailSender:
	def send(self, to, body):
		...


class WelcomeService:
	def __init__(self, sender: EmailSender):
		self.sender = sender

	def welcome(self, user):
		self.sender.send(user.email, "Welcome!")


# Composition root: choose concrete implementations here
sender = EmailSender()
service = WelcomeService(sender)
```

FastAPI dependency injection
- FastAPI uses function/parameter injection with dependency declarations (`Depends`).
- Dependencies can return simple values, classes, database sessions, etc.
- Scopes (`request`, `session`, `singleton` via caching) control lifetime of injected objects.

Example
```python
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

app = FastAPI()


def get_db() -> Session:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def get_service(db: Session = Depends(get_db)):
	return WelcomeService(db=db)


@app.post("/welcome")
def create_welcome(user: UserIn, service = Depends(get_service)):
	return service.welcome(user)
```

Key FastAPI patterns
- Use small, composable dependency functions; avoid heavy global state.
- Prefer constructor injection inside services; expose services via dependency functions.
- Leverage `Depends` with `yield` for setup/teardown (DB sessions, clients).
- For tests, override dependencies with `app.dependency_overrides` to inject fakes.
