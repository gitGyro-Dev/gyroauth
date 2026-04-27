# GyroAuth v2 — FastAPI PoC

## 🧭 Purpose
Demonstrates working GyroAuth v2 authentication under deviation.

---

## ■ How to Run
pip install -r requirements.txt
uvicorn app.main:app --reload

http://127.0.0.1:8000/docs

---

## ■ Important
/authenticate requires:
- session_id
- prior /observe

---

## ■ Flow

1. /observe (stable)
2. /authenticate → AUTH_STABLE
3. /observe (drift)
4. /authenticate → RECONVERGING
5. /observe (recovery)
6. /authenticate → AUTH_STABLE
7. /observe (attack)
8. /authenticate → AUTH_FAIL

---

## 🔴 Final
Authentication = stability over time
