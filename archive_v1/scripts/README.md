# GyroAuth PoC

A minimal proof-of-concept implementation of **GyroAuth** based on the idea:

> Authentication = State Convergence

This PoC demonstrates:

- observation (Slice) from raw state
- stability scoring over recent history
- trajectory tracking
- reference enrollment
- authentication by trajectory similarity + stability

## Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Main endpoints

- `POST /observe`
- `GET /stability/{session_id}`
- `POST /enroll`
- `POST /authenticate`
- `POST /reconverge`
- `GET /session/{session_id}`

## Demo flow

1. Send several `/observe` calls for a stable session.
2. Check `/stability/{session_id}`.
3. Call `/enroll` for the user.
4. Start a second session for the same user.
5. Send several similar observations.
6. Call `/authenticate`.

## Notes

This is a PoC, not a production authentication system.

It uses an in-memory store and intentionally simple math so the logic is easy to inspect and extend.

## Theory mapping

| Gyro Logic | PoC |
|---|---|
| Structure | raw state input |
| Slice | `slice_engine.py` feature extraction |
| Stability | `stability.py` |
| Identity | trajectory history |
| Convergence | trajectory similarity |
| Authentication | decision threshold |
